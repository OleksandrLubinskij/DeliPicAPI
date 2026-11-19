from typing import List

from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel, Field
from fastapi import Depends, UploadFile
from .geminy_ai_client import get_ai
from ...core.exceptions import ServiceUnavailable, InvalidPhoto, RecognitionFailed

class FoodInfo(BaseModel):
    product_name: str = Field(description="Назва продукту на фото")
    calories_per_100g: float = Field(description="Орієнтовна калорійність на 100 грамів")
    proteins_per_100g: float = Field(description="Орієнтовна кількість білків на 100 грамів")
    carbohydrates_per_100g: float = Field(description="Орієнтовна кількість вуглеводів на 100 грамів")
    fats_per_100g: float = Field(description="Орієнтовна кількість жирів на 100 грамів")

class VisionService:
    def __init__(self, client: genai.Client):
        self.client = client

    async def read_photo_bytes(self, product_photo: UploadFile) -> tuple[bytes, str]:
        mime_type = product_photo.content_type or "image/jpeg"
        if not mime_type.startswith("image/"):
            raise InvalidPhoto("Invalid file type! Expected an image.")

        await product_photo.seek(0)
        photo_bytes = await product_photo.read()
        if not photo_bytes:
            raise InvalidPhoto("Uploaded photo file is empty!")

        return photo_bytes, mime_type
    
    async def define_product(self, product_photo: UploadFile) -> FoodInfo:
        photo_bytes, mime_type = await self.read_photo_bytes(product_photo)

        try:
            response = await self.client.aio.models.generate_content(
                # model="gemini-3.6-flash",
                model="gemma-4-31b-it",
                contents=[
                    "Визнач продукт на фотографії та вкажи його орієнтовну калорійність, а також кількість білків, вуглеводів і жирів на 100 грамів.",
                    types.Part.from_bytes(
                        data=photo_bytes,
                        mime_type=mime_type
                    )
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=FoodInfo,
                ),
            )
            if not response.parsed:
                raise RecognitionFailed("Failed to parse product info from the photo")
            
            return response.parsed
        except APIError as e:
            print(f"Error |||  {e}")
            raise ServiceUnavailable("Geminy Vision service unavailable!(define product)")

    async def get_photo_embedding(self, product_photo: UploadFile) -> List[float]:
        photo_bytes, mime_type = await self.read_photo_bytes(product_photo)

        try:
            result = await self.client.aio.models.embed_content(
                model="gemini-embedding-2",
                contents=[
                    types.Part.from_bytes(
                        data=photo_bytes,
                        mime_type=mime_type,
                    ),
                ],
                config=types.EmbedContentConfig(output_dimensionality=512),
            )
            
            if not result.embeddings:
                raise RecognitionFailed("Empty embeddings returned from Gemini API")
                
            return result.embeddings[0].values

        except APIError as e:
            print(f"Gemini API error during embedding: {e}")
            raise ServiceUnavailable("Gemini Vision service unavailable! (get embedding)")

async def get_vision_service(client: genai.Client = Depends(get_ai)):
    return VisionService(client)