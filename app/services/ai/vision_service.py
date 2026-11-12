from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from fastapi import Depends, UploadFile
from .geminy_ai_client import get_ai
from ...core.exceptions import ServiceUnavailable

class FoodInfo(BaseModel):
    product_name: str = Field(description="Назва продукту на фото")
    calories_per_100g: float = Field(description="Орієнтовна калорійність на 100 грамів")
    proteins_per_100g: float = Field(description="Орієнтовна кількість білків на 100 грамів")
    carbohydrates_per_100g: float = Field(description="Орієнтовна кількість вуглеводів на 100 грамів")
    fats_per_100g: float = Field(description="Орієнтовна кількість жирів на 100 грамів")

class VisionService:
    def __init__(self, client: genai.Client):
        self.client = client

    async def define_product(self, product_photo: UploadFile) -> FoodInfo:
        product_photo_bytes = await product_photo.read()
        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[
                    "Визнач продукт на фотографії та вкажи його орієнтовну калорійність, а також кількість білків, вуглеводів і жирів на 100 грамів.",
                    types.Part.from_bytes(
                        data=product_photo_bytes,
                        mime_type=product_photo.content_type or "image/jpeg"
                    )
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=FoodInfo,
                ),
            )
            return response.parsed
        except Exception as e:
            raise ServiceUnavailable("Geminy Vision service unavailable!")

async def get_vision_service(client: genai.Client = Depends(get_ai)):
    return VisionService(client)