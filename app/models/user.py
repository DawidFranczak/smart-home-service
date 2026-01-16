from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    home_id: int
