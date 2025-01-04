from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from app.keyboards import get_yes_no_keyboard, get_race_keyboard
from app.states import AlienClassificationStates
from app.utils.number_generator import UniqueNumberGenerator
from app.utils.telegram_poster import post_to_group
from app.utils.sheets_manager import GoogleSheetsManager

router = Router()
number_generator = UniqueNumberGenerator()
sheets_manager = GoogleSheetsManager()

async def start_alien_classification(message: types.Message, state: FSMContext):
    await message.edit_text("Is it a humanoid?", reply_markup=get_yes_no_keyboard("humanoid"))
    await state.set_state(AlienClassificationStates.humanoid)

@router.callback_query(AlienClassificationStates.humanoid)
async def process_humanoid(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    humanoid = callback.data.split('_')[1]
    await state.update_data(humanoid=humanoid)
    
    if humanoid == "yes":
        await callback.message.edit_text("Select the race:", reply_markup=get_race_keyboard())
        await state.set_state(AlienClassificationStates.race)
    else:
        await callback.message.edit_text("Enter the weight in kilograms:")
        await state.set_state(AlienClassificationStates.weight)

@router.callback_query(AlienClassificationStates.race)
async def process_race(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    race = callback.data.split('_')[1].upper()
    await state.update_data(race=race)
    await callback.message.edit_text("Enter the skin color:")
    await state.set_state(AlienClassificationStates.skin_color)

@router.message(AlienClassificationStates.skin_color)
async def process_skin_color(message: types.Message, state: FSMContext):
    if not message.text or message.text.isspace():
        await message.answer("Skin color cannot be empty. Please enter the skin color:")
        return
    await state.update_data(skin_color=message.text)
    await message.answer("Is it dangerous?", reply_markup=get_yes_no_keyboard("dangerous"))
    await state.set_state(AlienClassificationStates.dangerous)

@router.callback_query(AlienClassificationStates.dangerous)
async def process_dangerous(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    dangerous = callback.data.split('_')[1]
    await state.update_data(dangerous=dangerous)
    await callback.message.edit_text("Does it have reason?", reply_markup=get_yes_no_keyboard("reason"))
    await state.set_state(AlienClassificationStates.has_reason)

@router.callback_query(AlienClassificationStates.has_reason)
async def process_has_reason(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    has_reason = callback.data.split('_')[1]
    await state.update_data(has_reason=has_reason)
    await callback.message.edit_text("Enter the weight in kilograms:")
    await state.set_state(AlienClassificationStates.weight)

@router.message(AlienClassificationStates.weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        if weight <= 0:
            await message.answer("Weight must be a positive number. Please try again:")
            return
        if weight > 1000:  # assuming max 1000kg for aliens
            await message.answer("Weight seems too high. Please try again:")
            return
        
        await state.update_data(weight=weight)
        data = await state.get_data()
        unique_number = number_generator.get_next_number()
        
        # Post to group
        await post_to_group(
            message.bot,
            message.from_user.full_name,
            "alien",
            data,
            unique_number
        )
        
        # Add to Google Sheets
        try:
            await sheets_manager.add_alien_entry(
                unique_number,
                message.from_user.full_name,
                data
            )
        except Exception as e:
            await message.answer("⚠️ Note: Classification was saved but couldn't be added to the database. An administrator has been notified.")
            # Here you might want to notify an admin about the sheets error
        
        # Format the summary message
        summary = f"✅ Alien Classification Complete\n"
        summary += f"Classification #{unique_number}\n\n"
        summary += f"Humanoid: {data['humanoid'].capitalize()}\n"
        
        if data['humanoid'] == 'yes':
            summary += (
                f"Race: {data['race']}\n"
                f"Skin Color: {data['skin_color']}\n"
                f"Dangerous: {data['dangerous'].capitalize()}\n"
                f"Has Reason: {data['has_reason'].capitalize()}\n"
            )
        
        summary += f"Weight: {data['weight']}kg"
        
        await message.answer(summary)
        await state.clear()
        
    except ValueError:
        await message.answer("Please enter a valid number for weight in kilograms:") 