from typing import Annotated
from fastapi import Depends, Header

# То тимчасово, поки не зробимо норм авторизацію і аутентифікацію, не смійтеся з мене 
async def get_current_user_id(
    x_user_id: Annotated[int | None, Header()] = None
) -> int:
    return x_user_id if x_user_id is not None else 2

CurrentUserId = Annotated[int, Depends(get_current_user_id)]