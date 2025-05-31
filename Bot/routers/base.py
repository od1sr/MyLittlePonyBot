from aiogram import Router, F
from aiogram.filters import Command
from ..keyboards import MainKeyboard
from .. import localizations as lc
from aiogram.types import Message, User
from db.session import async_session
from Classes.user import UserProfile
from db.services import load_user_profile
from src.ai_base.ai import request_with_gemini
from ..utils import safe_send_text

base_router = Router()
prompts_router = Router()

@base_router.message(Command("start"))
async def start(message: Message, event_from_user: User):
    await message.answer(lc.start_message.format(event_from_user.full_name), reply_markup=MainKeyboard())

@prompts_router.message(F.text)
async def send_prompt_to_ai(message: Message, event_from_user: User):
    async with async_session() as session:
        profile = await load_user_profile(event_from_user.id, session)
    
    text = ''
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

    prompt = message.text + "\n(Обо мне:\n" + text + ")"

    response = request_with_gemini(prompt)

    await safe_send_text(message.answer, response)