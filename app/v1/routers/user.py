from typing import List
from fastapi import APIRouter, Depends, Response
from ...core.security import create_access_token
from ...services.user_service import get_user_service, UserService
from ...services.auth_sevice import AuthService, get_auth_service
from ...schemas.user import UserCreate, UserUpdate, UserOut, UserLogin
from ...schemas.base_response import StatusResonse
from ...schemas.token import Token
from ...core.exceptions import AuthenticationFailed
router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/teapot")
async def user_teapot():
    return {"messsage": "User is teapot!"}

@router.get("/")
async def read_all_records(
    limit: int = 10,
    offset: int = 0,
    user_service: UserService = Depends(get_user_service)
) -> List[UserOut]:
    return await user_service.fetch_all(offset=offset,
                                         limit=limit)

@router.get("/{id}")
async def read_record(
    id: int,
    user_service: UserService = Depends(get_user_service)
) -> UserOut | None:
        
        return await user_service.fetch_by_id(id=id)

@router.post("/register")
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
) -> UserOut:
    return await auth_service.register(new_user_data=user_data)

@router.post("/login")
async def login(
    response: Response,
    form_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.login(response=response,
                                    user_data=form_data)

@router.post("/logout")
async def logout(
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
):
     return auth_service.logout(response=response)

@router.patch("/{id}")
async def update_record(
    id: int,
    diary_new_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
) -> UserOut:
    result = await user_service.update(id=id,
                                        new_data=diary_new_data)
    return result

@router.delete("/{id}")
async def delete_record(
    id: int,
    user_service: UserService = Depends(get_user_service)
) -> StatusResonse:
    await user_service.remove(id=id)
    return StatusResonse(id=id)