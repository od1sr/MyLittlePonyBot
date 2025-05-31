from aiogram import Router, Bot
from aiogram.types import Message, User
from aiogram.fsm.context import FSMContext
from Classes.user import UserProfile, UserRation
from ..states import UserProfileStates
from .. import localizations as lc
from ..keyboards import ProfileKeyboards
from aiogram import F
from aiogram.types import Message, CallbackQuery
from Classes.enums import Goal
from db.services import *
from db.session import async_session
from src.ai_base.ai import generate_ration_for_week
from ..utils import safe_send_text, safe_send_ration_for_week_response

user_router = Router()

@user_router.callback_query(F.data == "edit_profile")
async def edit_profile_callback(call: CallbackQuery, state: FSMContext, event_from_user: User):
    async with async_session() as session:
        profile = await load_user_profile(event_from_user.id, session)

    await show_profile(call.message.edit_text, state, profile)

@user_router.message(F.text == "📝 Мои данные")
async def edit_profile_command(message: Message, state: FSMContext, event_from_user: User):
    async with async_session() as session:
        profile = await load_user_profile(event_from_user.id, session)
    
    if profile is None:
        await state.set_state(UserProfileStates.weight)
        await state.update_data(user_id=event_from_user.id)
        await message.answer(lc.UserProfile.enter_weight, parse_mode='HTML')
    else:
        await show_profile(message.answer, state, profile)

async def show_profile(send_func, state: FSMContext, profile: UserProfile):
    '''
    Общая функция для отображения профиля пользователя ("Мои данные")
    '''

    await state.clear()

    text = ''

    if profile is None:
        return False

    for field_name, field in UserProfile.model_fields.items():
        if field_name not in "user_id":
            field_value = getattr(profile, field_name)

            if field_name == "goal":
                field_value = field_value.description
            elif field_name == "gender":
                field_value = 'Мужской' if field_value == 'm' else 'Женский'
            elif field_name == "activity":
                field_value = 'Да' if field_value else 'Нет'

            text += f"<b>{field.description}</b>: {field_value}\n"
    
    await send_func(lc.UserProfile.main.format(text), reply_markup=ProfileKeyboards.EditProfileKb(), parse_mode="HTML")
    
    return True

@user_router.message(UserProfileStates.weight)
async def enter_weight(message: Message, state: FSMContext):
    try:
        weight = UserProfile.validate_weight(message.text)
        await state.update_data(weight=weight)

        await message.answer(lc.UserProfile.enter_height, parse_mode='HTML')
        await state.set_state(UserProfileStates.height)
    except ValueError:
        await message.answer(lc.invalid_value_error_message)

@user_router.message(UserProfileStates.height)
async def enter_height(message: Message, state: FSMContext):
    try:
        height = UserProfile.validate_height(message.text)
        await state.update_data(height=height)

        await message.answer(lc.UserProfile.enter_age, parse_mode='HTML')
        await state.set_state(UserProfileStates.age)
    except ValueError:
        await message.answer(lc.invalid_value_error_message)

@user_router.message(UserProfileStates.age)
async def enter_age(message: Message, state: FSMContext):
    try:
        age = UserProfile.validate_age(message.text)
        await state.update_data(age=age)

        await message.answer(
            lc.UserProfile.enter_gender, reply_markup=ProfileKeyboards.EditGenderKb(False), parse_mode='HTML')
        await state.set_state(UserProfileStates.gender)
    except ValueError:
        await message.answer(lc.invalid_value_error_message)

@user_router.callback_query(F.data.startswith("edit_profile;gender;"), UserProfileStates.gender)
async def choose_gender(call: CallbackQuery, state: FSMContext):
    gender = UserProfile.validate_gender(call.data.split(";")[2])
    await state.update_data(gender=gender)

    await call.message.edit_text(
        lc.UserProfile.enter_goal, reply_markup=ProfileKeyboards.EditGoalKb(False), parse_mode='HTML')
    await state.set_state(UserProfileStates.goal)

@user_router.callback_query(F.data.startswith("edit_profile;goal;"), UserProfileStates.goal)
async def choose_goal(call: CallbackQuery, state: FSMContext, event_from_user: User):
    goal = Goal.from_index(int(call.data.split(";")[2]))
    await state.update_data(goal=goal)

    await call.message.edit_text(
        lc.UserProfile.enter_activity, reply_markup=ProfileKeyboards.EditActivityKb(False), parse_mode='HTML')
    await state.set_state(UserProfileStates.activity)

@user_router.callback_query(F.data.startswith("edit_profile;activity;"), UserProfileStates.activity)
async def choose_activity(call: CallbackQuery, state: FSMContext, event_from_user: User, bot: Bot):
    activity = int(call.data.split(";")[2])
    await state.update_data(activity=activity)

    profile = UserProfile(**await state.get_data())
    
    await state.clear()

    async with async_session() as session:
        await save_user_profile(profile, session)

    await show_profile(call.message.edit_text, state, profile)
    ration = generate_ration_for_week(
        profile.weight, 
        profile.height, 
        profile.age, 
        'мужской' if profile.gender == 'm' else 'женский', 
        profile.goal.description, 
        activity
    )

    await safe_send_ration_for_week_response(lambda text: bot.send_message(event_from_user.id, text), "Ваш рацион:\n" + ration,
        parse_mode='markdown')

    async with async_session() as session:
        await save_user_ration(UserRation(user_id = event_from_user.id, ration = ration), session)
    
    

@user_router.message(F.text == "🥩 мой рацион")
async def my_diet(message: Message):
    async with async_session() as session:
        ration = await load_user_ration(message.from_user.id, session)
    
    if ration is None:
        await message.answer("У вас еще нет рациона питания")
        return
    text = f"Ваш рацион:\n{ration.ration}"

    await safe_send_ration_for_week_response(message.answer, text, parse_mode='markdown')


@user_router.message(F.text == "📊 Моя динамика")
async def my_dynamics(message: Message):
    await message.answer("Ваша динамика:") # TODO: добавить график

@user_router.callback_query(F.data == "edit_profile;goal")
async def edit_goal_callback(call: CallbackQuery, state: FSMContext, event_from_user: User):
    async with async_session() as session:
        profile = await load_user_profile(event_from_user.id, session)

    