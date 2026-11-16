from fastapi import APIRouter, Depends, UploadFile, File
from ...services.ai.vision_service import VisionService, get_vision_service
from ...services.diary_service import DiaryService, get_diary_service
from ...services.storage.s3_client import S3Client, get_s3
from ...schemas.product import ProductNutritionResponse

router = APIRouter(
    prefix="/scales",
    tags=["Scales"]
)

@router.get("/teapot")
async def scale_teapot():
    return {"messsage": "Scale is teapot!"}

@router.post("/identify_product")
async def identify_product(
    photo: UploadFile = File(...),
    vision_service: VisionService = Depends(get_vision_service),
    s3: S3Client = Depends(get_s3)) -> ProductNutritionResponse:

    pass

@router.post("/save_to_diary")
async def save_to_diary(
    diary_service: DiaryService = Depends(get_diary_service)
):
    pass