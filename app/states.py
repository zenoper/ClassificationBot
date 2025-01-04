from aiogram.fsm.state import StatesGroup, State


class ClassificationStates(StatesGroup):
    choosing_type = State()


class HumanClassificationStates(StatesGroup):
    gender = State()
    age = State()
    nationality = State()
    education = State()
    eye_color = State()
    hair_color = State()
    height = State()


class AnimalClassificationStates(StatesGroup):
    species = State()
    mammal = State()
    predator = State()
    color = State()
    weight = State()
    age = State()


class AlienClassificationStates(StatesGroup):
    humanoid = State()
    race = State()
    skin_color = State()
    dangerous = State()
    has_reason = State()
    weight = State()