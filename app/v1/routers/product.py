from fastapi import APIRouter, Depends, Form, File, UploadFile
from typing import Annotated, List
from ...services.product_service import get_product_service, ProductService
from ...schemas.product import ProductModel, ProductUpdate, FullProductResponse
from ...services.storage.s3_client import get_s3, S3Client
from ...services.ai.vision_service import get_vision_service, VisionService
router = APIRouter(
    prefix="/product",
    tags=["Product"]
)

@router.get("/teapot")
async def product_teapot():
    return {"messsage": "Product is teapot!"}

@router.get("/")
async def read_all_records(
    limit: int = 10,
    offset: int = 0,
    is_accept_state: bool | None = None,
    diary_service: ProductService = Depends(get_product_service)
) -> List[FullProductResponse]:
    
    return await diary_service.fetch_all(offset=offset,
                                         limit=limit,
                                         is_accept_state=is_accept_state)

@router.get("/{id}")
async def read_record(
    id: int,
    fields: str | None = None,
    include_embedding: bool = False,
    diary_service: ProductService = Depends(get_product_service)
) -> FullProductResponse:
    
    if fields:
        fields = fields.split(",")
        return await diary_service.fetch_by_id(id=id,
                                           fields=fields,
                                           include_embedding=include_embedding)
    else:
        return await diary_service.fetch_by_id(id=id,
                                               include_embedding=include_embedding)

@router.post("/")
async def create_record(
    diary_data: Annotated[ProductModel, Form(...)],
    file: UploadFile = File(...),
    diary_service: ProductService = Depends(get_product_service),
    s3_service: S3Client = Depends(get_s3),
    vision_service: VisionService = Depends(get_vision_service)
) -> FullProductResponse:
    
    # await file.seek(0)
    # photo_embedding = await vision_service.get_photo_embedding(product_photo=file)
    # await s3_service.
    result = await diary_service.register(new_data=diary_data)
    return result

@router.patch("/{id}")
async def update_record(
    id: int,
    diary_new_data: ProductUpdate,
    diary_service: ProductService = Depends(get_product_service)
) -> FullProductResponse:

    result = await diary_service.update(id=id,
                                        new_data=diary_new_data)
    return result

@router.delete("/{id}")
async def delete_record(
    id: int,
    diary_service: ProductService = Depends(get_product_service)
) -> bool:
    
    return await diary_service.remove(id=id)