from typing import Annotated
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..core.security import decode_access_token
from ..services.user_service import UserService, get_user_service
from ..schemas.user import UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# То тимчасово, поки не зробимо норм авторизацію і аутентифікацію, не смійтеся з мене 
async def get_current_user_id(
    x_user_id: Annotated[int | None, Header()] = None
) -> int:
    return x_user_id if x_user_id is not None else 2

CurrentUserId = Annotated[int, Depends(get_current_user_id)]
