from sqlalchemy.ext.asyncio import AsyncSession
from db.models import UserProfileDB, UserRationDB
from Classes.user import UserProfile, UserRation

async def save_user_profile(profile: UserProfile, session: AsyncSession):
    db_obj = await session.get(UserProfileDB, profile.user_id)

    if db_obj:
        db_obj.weight = profile.weight
        db_obj.height = profile.height
        db_obj.age = profile.age
        db_obj.gender = profile.gender
        db_obj.goal = profile.goal
        db_obj.activity = profile.activity
    else:
        db_obj = UserProfileDB(
            user_id=profile.user_id,
            weight=profile.weight,
            height=profile.height,
            age=profile.age,
            gender=profile.gender,
            goal=profile.goal,
            activity=profile.activity
        )
        session.add(db_obj)

    await session.commit()

async def load_user_profile(user_id: int, session: AsyncSession) -> UserProfile | None:
    db_obj = await session.get(UserProfileDB, user_id)
    if db_obj:
        return UserProfile.model_validate({
            "user_id": db_obj.user_id,
            "weight": db_obj.weight,
            "height": db_obj.height,
            "age": db_obj.age,
            "gender": db_obj.gender,
            "goal": db_obj.goal,
            "activity": db_obj.activity
        })
    
    return None

async def save_user_ration(ration: UserRation, session: AsyncSession):
    db_obj = await session.get(UserRationDB, ration.user_id)

    if db_obj:
        db_obj.ration = ration.ration
    else:
        db_obj = UserRationDB(
            user_id=ration.user_id,
            ration=ration.ration
        )
        session.add(db_obj)

    await session.commit()

async def load_user_ration(user_id: int, session: AsyncSession) -> UserRation | None:
    db_obj = await session.get(UserRationDB, user_id)
    if db_obj:
        return UserRation.model_validate({
            "user_id": db_obj.user_id,
            "ration": db_obj.ration,
        })
    
    return None