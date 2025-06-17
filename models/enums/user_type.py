from enum import Enum


class UserType(str, Enum):
    user = "User",
    company = "Company"