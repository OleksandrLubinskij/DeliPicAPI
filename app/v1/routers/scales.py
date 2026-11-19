from fastapi import APIRouter, Depends, UploadFile, File
from ...services.product_service import ProductService, get_product_service
from ...services.ai.vision_service import VisionService, get_vision_service
from ...services.diary_service import DiaryService, get_diary_service
from ...services.storage.s3_client import S3Client, get_s3
from ...schemas.product import ProductNutritionResponse
from ...services.product_lookup import recognize_or_create_product
from ...core.dependencies import CurrentUserId, get_current_user_id
router = APIRouter(
    prefix="/scales",
    tags=["Scales"]
)

@router.get("/teapot")
async def scale_teapot():
    return {"messsage": "Scale is teapot!"}

@router.post("/identify_product")
async def identify_product(
    current_user: CurrentUserId,
    file: UploadFile = File(...),
    product_service: ProductService = Depends(get_product_service),
    vision_service: VisionService = Depends(get_vision_service),
    s3: S3Client = Depends(get_s3)):
    # ) -> ProductNutritionResponse:

    return await recognize_or_create_product(file=file,
                                             product_service=product_service,
                                             vision_service=vision_service,
                                             s3=s3,
                                             current_user=current_user)


@router.post("/save_to_diary")
async def save_to_diary(
    diary_service: DiaryService = Depends(get_diary_service)
):
    pass