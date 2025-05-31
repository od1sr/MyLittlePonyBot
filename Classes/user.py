from __future__ import annotations
from pydantic import BaseModel, field_validator, Field
from .enums import Goal

class UserProfile(BaseModel):
        
    user_id: int = Field(..., description="ID пользователя")
    weight: float = Field(..., description="Вес")
    height: float = Field(..., description="Рост")
    age: int = Field(..., description="Возраст")
    gender: str = Field(..., description="Пол") # 'm'/'f'
    goal: Goal = Field(..., description="Цель")
    activity: bool = Field(..., description="Активный образ жизни")

    @field_validator("weight")
    @classmethod
    def validate_weight(cls, v: str|float):
        if isinstance(v, str):
            v = float(v.replace(',', '.'))

        if v <= 0:
            raise ValueError("Weight must be greater than 0")

        return v
    
    @field_validator("height")
    @classmethod
    def validate_height(cls, v: float|str):
        if isinstance(v, str):
            v = float(v.replace(',', '.'))

        if v <= 0:
            raise ValueError("Height must be greater than 0")

        if v > 300:
            raise ValueError("Height must be less than 300")

        return v
    
    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int|str):
        v = int(v)

        if v <= 0:
            raise ValueError("Age must be greater than 0")

        if v > 150:
            raise ValueError("Age must be less than 150")

        return v
    
    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str):
        if v not in ['m', 'f', 'м', 'ж']:
            raise ValueError("Gender must be 'm' or 'f'")

        return 'm' if v in ['m', 'м'] else 'f'
    
class UserRation(BaseModel):
    user_id: int
    ration: str