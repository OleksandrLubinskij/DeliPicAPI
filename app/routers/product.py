from fastapi import APIRouter

router = APIRouter(
    prefix="/product",
    tags=["Product"]
)

@router.get("/")
async def product_teapot():
    return {"messsage": "Product is teapot!"}