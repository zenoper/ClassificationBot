from datetime import datetime
from aiogram import Bot
import config as Config

async def post_to_group(bot: Bot, user_full_name: str, being_type: str, data: dict, unique_number: str):
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Start building the message
    message = (
        f"#{unique_number}\n"
        f"{current_date}\n"
        f"Initiated by: {user_full_name}\n"
        f"Specie: {being_type.capitalize()}\n\n"
    )
    
    # Add all the classification data
    if being_type == "human":
        message += (
            f"Gender: {data['gender'].capitalize()}\n"
            f"Age: {data['age']}\n"
            f"Nationality: {data['nationality']}\n"
            f"Education: {data['education'].capitalize()}\n"
            f"Eye Color: {data['eye_color']}\n"
            f"Hair Color: {data['hair_color']}\n"
            f"Height: {data['height']}cm"
        )
    elif being_type == "animal":
        message += (
            f"Species: {data['species']}\n"
            f"Mammal: {data['mammal'].capitalize()}\n"
            f"Predator: {data['predator'].capitalize()}\n"
            f"Color: {data['color']}\n"
            f"Weight: {data['weight']}kg\n"
            f"Age: {data['age']} months"
        )
    elif being_type == "alien":
        message += f"Humanoid: {data['humanoid'].capitalize()}\n"
        if data['humanoid'] == 'yes':
            message += (
                f"Race: {data['race']}\n"
                f"Skin Color: {data['skin_color']}\n"
                f"Dangerous: {data['dangerous'].capitalize()}\n"
                f"Has Reason: {data['has_reason'].capitalize()}\n"
            )
        message += f"Weight: {data['weight']}kg"
    
    # Post to the group
    await bot.send_message(Config.GROUP_CHAT_ID, message) 