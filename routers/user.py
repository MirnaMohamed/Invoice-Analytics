from typing import List

from fastapi import APIRouter

from models.enums.user_type import UserType
from models.user import User

router = APIRouter()


#@router.get("/{task_id}", summary="Get task", response_model=TaskRead)
#async def get(*, service: TaskServiceDep, task_id: str):
#    return await service.get_by_id(task_id)
db : List[User] = [
    User(first_name="Mirna", last_name="Atallah", user_type=UserType.user),
    User(first_name="Margret", last_name="Jones", user_type=UserType.company)
]

@router.get("/users", response_model=List[User])
def get_users():
    return db