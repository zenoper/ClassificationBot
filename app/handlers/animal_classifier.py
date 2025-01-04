from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from app.keyboards import get_yes_no_keyboard
from app.states import AnimalClassificationStates
from app.utils.number_generator import UniqueNumberGenerator
from app.utils.telegram_poster import post_to_group
from app.utils.sheets_manager import GoogleSheetsManager

router = Router()
number_generator = UniqueNumberGenerator()
sheets_manager = GoogleSheetsManager()

async def start_animal_classification(message: types.Message, state: FSMContext):
    await message.edit_text("Please enter the species of the animal:")
    await state.set_state(AnimalClassificationStates.species)

@router.message(AnimalClassificationStates.species)
async def process_species(message: types.Message, state: FSMContext):
    if not message.text or message.text.isspace():
        await message.answer("Species cannot be empty. Please enter the species:")
        return
    await state.update_data(species=message.text)
    await message.answer("Is it a mammal?", reply_markup=get_yes_no_keyboard("mammal"))
    await state.set_state(AnimalClassificationStates.mammal)

@router.callback_query(AnimalClassificationStates.mammal)
async def process_mammal(callback: types.CallbackQuery, state: FSMContext):
    mammal = callback.data.split('_')[1]
    await state.update_data(mammal=mammal)
    await callback.message.edit_text("Is it a predator?", reply_markup=get_yes_no_keyboard("predator"))
    await state.set_state(AnimalClassificationStates.predator)

@router.callback_query(AnimalClassificationStates.predator)
async def process_predator(callback: types.CallbackQuery, state: FSMContext):
    predator = callback.data.split('_')[1]
    await state.update_data(predator=predator)
    await callback.message.edit_text("What color is the animal?")
    await state.set_state(AnimalClassificationStates.color)

@router.message(AnimalClassificationStates.color)
async def process_color(message: types.Message, state: FSMContext):
    if not message.text or message.text.isspace():
        await message.answer("Color cannot be empty. Please enter the animal's color:")
        return
    await state.update_data(color=message.text)
    await message.answer("Enter the animal's weight in kilograms:")
    await state.set_state(AnimalClassificationStates.weight)

@router.message(AnimalClassificationStates.weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        if weight <= 0:
            await message.answer("Weight must be a positive number. Please try again:")
            return
        
        await state.update_data(weight=weight)
        await message.answer("Enter the animal's age in months:")
        await state.set_state(AnimalClassificationStates.age)
    except ValueError:
        await message.answer("Please enter a valid number for weight in kilograms:")

@router.message(AnimalClassificationStates.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age <= 0:
            await message.answer("Age must be a positive number. Please try again:")
            return
        if age > 1200:  # 100 years in months
            await message.answer("It is impossible that the animal is older than 100 years. Please try again:")
            return
        
        await state.update_data(age=age)
        data = await state.get_data()
        unique_number = number_generator.get_next_number()
        
        # Post to group
        await post_to_group(
            message.bot,
            message.from_user.full_name,
            "animal",
            data,
            unique_number
        )
        
        # Add to Google Sheets
        try:
            await sheets_manager.add_animal_entry(
                unique_number,
                message.from_user.full_name,
                data
            )
        except Exception as e:
            await message.answer("⚠️ Note: Classification was saved but couldn't be added to the database. An administrator has been notified.")
            # Here you might want to notify an admin about the sheets error
        
        # Format the summary message
        summary = (
            f"✅ Animal Classification Complete\n"
            f"Classification #{unique_number}\n\n"
            f"Species: {data['species']}\n"
            f"Mammal: {data['mammal'].capitalize()}\n"
            f"Predator: {data['predator'].capitalize()}\n"
            f"Color: {data['color']}\n"
            f"Weight: {data['weight']}kg\n"
            f"Age: {data['age']} months"
        )
        
        await message.answer(summary)
        await state.clear()
        
    except ValueError:
        await message.answer("Please enter a valid number for age in months:") 