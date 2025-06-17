from uuid import UUID, uuid4

from pydantic import BaseModel

from models.enums.user_type import UserType


class User(BaseModel):
    id: UUID = uuid4()
    first_name : str
    last_name : str
    user_type: UserType
