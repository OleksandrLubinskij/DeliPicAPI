from fastapi import APIRouter, Depends
from ..services.product_service import get_product_service, ProductService
from ..schemas.product import ProductModel, ProductUpdate 

router = APIRouter(
    prefix="/product",
    tags=["Product"]
)

@router.get("/teapot")
async def product_teapot():
    return {"messsage": "Product is teapot!"}

@router.get("/")
async def read_all_records(limit: int = 10,
                offset: int = 0,
                diary_service: ProductService = Depends(get_product_service)):
    return await diary_service.fetch_all(offset=offset,
                                         limit=limit)

@router.get("/{id}")
async def read_record(id: int,
                  fields: str | None = None,
                  diary_service: ProductService = Depends(get_product_service)):
    if fields:
        fields = fields.split(",")
        return await diary_service.fetch_by_id(id=id,
                                           fields=fields)
    else:
        return await diary_service.fetch_by_id(id=id)

@router.post("/")
async def create_record(diary_data: ProductModel,
                        diary_service: ProductService = Depends(get_product_service)):
    result = await diary_service.register(new_data=diary_data)
    return result

@router.patch("/{id}")
async def update_record(id: int,
                diary_new_data: ProductUpdate,
                diary_service: ProductService = Depends(get_product_service)):
    result = await diary_service.update(id=id,
                                        new_data=diary_new_data)
    return result

@router.delete("/{id}")
async def delete_record(id: int,
                  diary_service: ProductService = Depends(get_product_service)):
    return await diary_service.remove(id=id)