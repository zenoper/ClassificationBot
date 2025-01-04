from mailbox import Message

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_being_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Human", callback_data="type_human"),
                InlineKeyboardButton(text="Animal", callback_data="type_animal"),
                InlineKeyboardButton(text="Alien", callback_data="type_alien"),
            ]
        ]
    )

def get_gender_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Male", callback_data="gender_male"),
                InlineKeyboardButton(text="Female", callback_data="gender_female"),
            ]
        ]
    )

def get_education_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Higher", callback_data="education_higher"),
                InlineKeyboardButton(text="School", callback_data="education_school"),
            ]
        ]
    )

def get_yes_no_keyboard(callback_prefix: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yes", callback_data=f"{callback_prefix}_yes"),
                InlineKeyboardButton(text="No", callback_data=f"{callback_prefix}_no"),
            ]
        ]
    )

def get_race_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="X", callback_data="race_x"),
                InlineKeyboardButton(text="Y", callback_data="race_y"),
                InlineKeyboardButton(text="Z", callback_data="race_z"),
            ]
        ]
    )