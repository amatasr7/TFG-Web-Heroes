from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    email: str
    is_admin: bool = False


class UserCreate(UserBase):
    password: str = ""


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    is_admin: bool | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
