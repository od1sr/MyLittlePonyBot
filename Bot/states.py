from aiogram.fsm.state import State, StatesGroup

class UserProfileStates(StatesGroup):
    weight = State()
    age = State()
    height = State()
    gender = State()
    goal = State()