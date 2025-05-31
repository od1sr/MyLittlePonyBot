from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    KeyboardButton, 
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Classes.user import UserProfile
from Classes.enums import Goal

def MainKeyboard() -> ReplyKeyboardMarkup:
    '''Главное меню (после /start)'''

    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="📝 Мои данные")], # профиль
            [KeyboardButton(text="🥩 мой рацион")], # план питания
            [KeyboardButton(text="📊 Моя динамика")] # график веса по дням
        ]   
    )

    return kb

class ProfileKeyboards:

    @staticmethod
    def EditProfileKb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        
        for field_name, field in UserProfile.model_fields.items():
            if field_name != "user_id":
                kb.button(text=field.description, callback_data=f"edit_profile;{field_name}")
        
        kb.adjust(2)

        return kb.as_markup()
    
    @staticmethod
    def BackToEditProfileBtn() -> InlineKeyboardButton:
        return InlineKeyboardButton(text="⬅️ Назад", callback_data="edit_profile")

    @staticmethod
    def EditGenderKb(with_back_btn: bool = True) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.button(text="Мужской", callback_data="edit_profile;gender;m")
        kb.button(text="Женский", callback_data="edit_profile;gender;f")
        
        if with_back_btn:
            kb.add(ProfileKeyboards.BackToEditProfileBtn())

        return kb.as_markup()
    
    @staticmethod
    def EditGoalKb(with_back_btn: bool = True) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for goal in Goal: # перебираем все возможные цели (сброс\набор веса, ЗОЖ) и под каждую делаем кнопку
            kb.button(text=goal.description, callback_data=f"edit_profile;goal;{goal.index}")

        if with_back_btn:
            kb.add(ProfileKeyboards.BackToEditProfileBtn())

        return kb.as_markup()
    
    @staticmethod
    def RebuildMyRationBtn() -> InlineKeyboardButton:
        return InlineKeyboardButton(text="🥩 Перестроить мой рацион", callback_data="rebuild_ration")
    
    @staticmethod
    def EditActivityKb(with_back_btn: bool = True) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.button(text="Да", callback_data="edit_profile;activity;1")
        kb.button(text="Нет", callback_data="edit_profile;activity;0")

        if with_back_btn:
            kb.add(ProfileKeyboards.BackToEditProfileBtn())

        return kb.as_markup()