from aiogram.fsm.state import State, StatesGroup

class UserProfileStates(StatesGroup):
    weight = State()
    age = State()
    height = State()
    gender = State()
    goal = State()
    activity = State()

    edit_weight = State()
    edit_age = State()
    edit_height = State()
    edit_gender = State()
    edit_goal = State()