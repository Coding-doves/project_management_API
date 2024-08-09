from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    username:str
    firstname:str
    lastname:str


class CreateUser(UserBase):
    passwd:str


class User(UserBase):
    id:Optional[int]
    active:bool

    class Config:
        orm_mode=True


class Token(BaseModel):
    access_token: str
    token_type: str


class TaskBase(BaseModel):
    title: str
    description: str = None
    completed: bool = False


class Task(TaskBase):
    id: Optional[int]
    owner_id: int

    class Config:
        orm_mode = True

