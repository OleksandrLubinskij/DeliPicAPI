from uuid import uuid4

from .product_service import ProductService
from .ai.vision_service import VisionService
from .storage.s3_client import S3Client
from ..schemas.product import ProductNutritionResponse, ProductModel
from fastapi import UploadFile
from ..core.dependencies import CurrentUserId

async def recognize_or_create_product(
    file: UploadFile,
    product_service: ProductService,
    vision_service: VisionService,
    s3: S3Client,
    current_user: CurrentUserId,
) -> ProductNutritionResponse:

    await file.seek(0)
    photo_embedding = await vision_service.get_photo_embedding(product_photo=file)
    product = await product_service.fetch_by_embedding(embedding=photo_embedding)
    if product:
        return product
    else:
        await file.seek(0)
        vision_response = await vision_service.define_product(product_photo=file)
        await file.seek(0)
        photo_bytes = await file.read()

        ext = file.filename.split(".")[-1] if file.filename and "." in file.filename else "jpg"
        unique_filename = f"product-{uuid4()}.{ext}"

        await s3.upload_file(file_data=photo_bytes,
                             object_name=unique_filename)
        s3_public_url = await s3.get_public_url()
        new_product = ProductModel(user_id=current_user,
                                name=vision_response.product_name,
                                calories=vision_response.calories_per_100g,
                                proteins=vision_response.proteins_per_100g,
                                carbohydrates=vision_response.carbohydrates_per_100g,
                                fats=vision_response.fats_per_100g,
                                photo_path=f"{s3_public_url}/{unique_filename}",
                                photo_vector=photo_embedding,
                                is_accepted=False)
        
        new_product_instance = await product_service.register(new_data=new_product)
                                   
        return new_product_instance