from fastapi import status

class BaseError(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail: str = "Internal server error"
    def __init__(self, error_detail: str | None = None):
        self.error_detail = error_detail or self.default_detail
        super().__init__(self.error_detail)

class NotFoundError(BaseError):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not found!"


class ServiceUnavailable(BaseError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Service is temporarily unavailable"


class InvalidPhoto(BaseError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid photo provided"


class RecognitionFailed(BaseError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Failed to recognize content"

class AuthenticationFailed(BaseError):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Incorrect login or password"

class UserAlreadyExists(BaseError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User already exists"

class InvalidCredentials(BaseError):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid or expired token"

class YouAreOrdinaryMortal(BaseError):
    status_code = status.HTTP_403_FORBIDDEN,
    default_detail = "You are an ordinary mortal. Admin rights required."