from fastapi import Depends, Response
from fastapi.security import APIKeyCookie
from ..core.security import create_access_token, decode_access_token
from ..schemas.user import UserCreate, UserLogin, UserOut
from ..services.user_service import UserService, get_user_service
from ..core.exceptions import InvalidCredentials, UserAlreadyExists, AuthenticationFailed

cookie_scheme = APIKeyCookie(name="access_token")


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def register(self, new_user_data: UserCreate) -> UserOut:
        existing_user = await self.user_service.get_user_by_login(new_user_data.login)
        if existing_user:
            raise UserAlreadyExists()
        return await self.user_service.register(new_user_data)

    async def login(self, response: Response, user_data: UserLogin) -> dict:
        user = await self.user_service.authenticate(
            login=user_data.login,
            password=user_data.password
        )
        if not user:
            raise AuthenticationFailed()

        access_token = create_access_token({
            "sub": user.login,
            "role": user.role.value
        })

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="lax",
            secure=False
        )
        return {"message": "Successful login"}

    def logout(self, response: Response) -> dict:
        response.delete_cookie(
            key="access_token",
            httponly=True,
            samesite="lax",
            secure=False
        )
        return {"message": "Logged out successfully"}


async def get_current_user(
    token: str = Depends(cookie_scheme),
    user_service: UserService = Depends(get_user_service),
) -> UserOut:
    credentials_exception = InvalidCredentials()

    payload = decode_access_token(token)
    if not payload or not (login := payload.get("sub")):
        raise credentials_exception

    user = await user_service.get_user_by_login(login=login)
    if not user:
        raise credentials_exception

    return UserOut.model_validate(user)


def get_auth_service(
    user_service: UserService = Depends(get_user_service)
) -> AuthService:
    return AuthService(user_service=user_service)