from pydantic import BaseModel


class Languages(BaseModel):
    language: str
    level: str


class UserCreate(BaseModel):
    email: str
    firstname: str
    lastname: str
    password: str
    birthday: str
    gender: str
    country: str
    languages: list[Languages]
