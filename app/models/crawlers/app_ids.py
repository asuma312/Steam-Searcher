from pydantic import BaseModel, Field
from typing import List

class AppId(BaseModel):
    appid: int = Field(...)
    name: str = Field(..., max_length=500)
    @classmethod
    def from_dict(cls, data: dict) -> "AppId":
        return cls.model_validate(data)

class AppList(BaseModel):
    apps: List[AppId] = Field(...)

    @classmethod
    def from_dict(cls, data: dict) -> "AppList":
        return cls.model_validate(data)

class AppIdResponse(BaseModel):
    applist: AppList = Field(...)
    @classmethod
    def from_dict(cls, data: dict) -> "AppIdResponse":
        return cls.model_validate(data)