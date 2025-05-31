from sqlalchemy.ext.asyncio import AsyncSession
from db.models import UserProfileDB
from Classes.UserProfile import UserProfile

async def save_user_profile(profile: UserProfile, session: AsyncSession):
    db_obj = await session.get(UserProfileDB, profile.user_id)

    if db_obj:
        db_obj.weight = profile.weight
        db_obj.height = profile.height
        db_obj.age = profile.age
        db_obj.gender = profile.gender
        db_obj.goal = profile.goal
    else:
        db_obj = UserProfileDB(
            user_id=profile.user_id,
            weight=profile.weight,
            height=profile.height,
            age=profile.age,
            gender=profile.gender,
            goal=profile.goal
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
        })
    
    return None