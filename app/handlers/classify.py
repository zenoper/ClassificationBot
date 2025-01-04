from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from app.keyboards import get_being_type_keyboard
from app.states import ClassificationStates
from app.handlers.human_classifier import start_human_classification
from app.handlers.animal_classifier import start_animal_classification
from app.handlers.alien_classifier import start_alien_classification

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    welcome_text = (
        "👋 Welcome to the Being Classification Bot!\n\n"
        "In order to start the classification process, please use the /classify command."
    )
    await message.answer(welcome_text)

@router.message(Command("classify"))
async def cmd_classify(message: types.Message, state: FSMContext):
    await message.answer("What type of being?", reply_markup=get_being_type_keyboard())
    await state.set_state(ClassificationStates.choosing_type)

@router.callback_query(ClassificationStates.choosing_type)
async def process_being_type(callback: types.CallbackQuery, state: FSMContext):
    being_type = callback.data.split('_')[1]
    await state.update_data(being_type=being_type)
    
    if being_type == "human":
        await start_human_classification(callback.message, state)
    elif being_type == "animal":
        await start_animal_classification(callback.message, state)
    elif being_type == "alien":
        await start_alien_classification(callback.message, state)
    else:
        await callback.message.edit_text(f"You selected: {being_type.capitalize()}")
        await state.clear()