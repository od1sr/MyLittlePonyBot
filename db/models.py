from sqlalchemy import (
    Column, Integer, BigInteger, Float, String, Text, Enum as SQLAEnum, Boolean)
from db.base import Base
from Classes.enums import Goal


class UserProfileDB(Base):
    __tablename__ = "user_profiles"

    user_id = Column(BigInteger, primary_key=True)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    goal = Column(SQLAEnum(Goal, name="goal_enum"), nullable=False)
    activity = Column(Boolean, nullable=False)

class UserRationDB(Base):
    __tablename__ = "user_rations"

    user_id = Column(BigInteger, primary_key=True)
    ration = Column(Text, nullable=False)
