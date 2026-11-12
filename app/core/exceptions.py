class BaseError(Exception):
    def __init__(self, error_detail: str | None = None):
        self.error_detail = error_detail

class NotFoundError(BaseError):
    pass

class ServiceUnavailable(BaseError):
    def __init__(self, error_detail = None):
        super().__init__(error_detail)