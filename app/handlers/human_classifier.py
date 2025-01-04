from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from app.keyboards import get_gender_keyboard, get_education_keyboard
from app.states import HumanClassificationStates
from app.utils.number_generator import UniqueNumberGenerator
from app.utils.telegram_poster import post_to_group
from app.utils.sheets_manager import GoogleSheetsManager

router = Router()
number_generator = UniqueNumberGenerator()
sheets_manager = GoogleSheetsManager()

async def start_human_classification(message: types.Message, state: FSMContext):
    await message.edit_text("Please select your gender:", reply_markup=get_gender_keyboard())
    await state.set_state(HumanClassificationStates.gender)

@router.callback_query(HumanClassificationStates.gender)
async def process_gender(callback: types.CallbackQuery, state: FSMContext):
    gender = callback.data.split('_')[1]
    await state.update_data(gender=gender)
    await callback.message.edit_text("Please enter your age:")
    await state.set_state(HumanClassificationStates.age)

@router.message(HumanClassificationStates.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age <= 0:
            await message.answer("Age must be a positive number. Please try again:")
            return
        if age > 120:
            await message.answer("It is impossible that you are older than 120 years. Please try again:")
            return
        
        await state.update_data(age=age)
        await message.answer("Please enter your nationality:")
        await state.set_state(HumanClassificationStates.nationality)
    except ValueError:
        await message.answer("Please enter a valid number for age:")

@router.message(HumanClassificationStates.nationality)
async def process_nationality(message: types.Message, state: FSMContext):
    if not message.text or message.text.isspace():
        await message.answer("Nationality cannot be empty. Please enter your nationality:")
        return
    await state.update_data(nationality=message.text)
    await message.answer("Select your education level:", reply_markup=get_education_keyboard())
    await state.set_state(HumanClassificationStates.education)

@router.callback_query(HumanClassificationStates.education)
async def process_education(callback: types.CallbackQuery, state: FSMContext):
    education = callback.data.split('_')[1]
    await state.update_data(education=education)
    await callback.message.edit_text("Please enter your eye color:")
    await state.set_state(HumanClassificationStates.eye_color)

@router.message(HumanClassificationStates.eye_color)
async def process_eye_color(message: types.Message, state: FSMContext):
    if not message.text or message.text.isspace():
        await message.answer("Eye color cannot be empty. Please enter your eye color:")
        return
    await state.update_data(eye_color=message.text)
    await message.answer("Please enter your hair color:")
    await state.set_state(HumanClassificationStates.hair_color)

@router.message(HumanClassificationStates.hair_color)
async def process_hair_color(message: types.Message, state: FSMContext):
    if not message.text or message.text.isspace():
        await message.answer("Hair color cannot be empty. Please enter your hair color:")
        return
    await state.update_data(hair_color=message.text)
    await message.answer("Please enter your height in centimeters:")
    await state.set_state(HumanClassificationStates.height)

@router.message(HumanClassificationStates.height)
async def process_height(message: types.Message, state: FSMContext):
    try:
        height = int(message.text)
        if height <= 0:
            await message.answer("Height must be a positive number. Please try again:")
            return
        if height > 300:
            await message.answer("It is impossible that you are taller than 300 cm. Please try again:")
            return
        
        await state.update_data(height=height)
        data = await state.get_data()
        unique_number = number_generator.get_next_number()
        
        # Post to group
        await post_to_group(
            message.bot,
            message.from_user.full_name,
            "human",
            data,
            unique_number
        )
        
        # Add to Google Sheets
        try:
            await sheets_manager.add_human_entry(
                unique_number,
                message.from_user.full_name,
                data
            )
        except Exception as e:
            await message.answer("⚠️ Note: Classification was saved but couldn't be added to the database. An administrator has been notified.")
            # Here you might want to notify an admin about the sheets error
        
        # Format the summary message
        summary = (
            f"✅ Human Classification Complete\n"
            f"Classification #{unique_number}\n\n"
            f"Gender: {data['gender'].capitalize()}\n"
            f"Age: {data['age']}\n"
            f"Nationality: {data['nationality']}\n"
            f"Education: {data['education'].capitalize()}\n"
            f"Eye Color: {data['eye_color']}\n"
            f"Hair Color: {data['hair_color']}\n"
            f"Height: {data['height']}cm"
        )
        
        await message.answer(summary)
        await state.clear()
        
    except ValueError:
        await message.answer("Please enter a valid number for height in centimeters:") 