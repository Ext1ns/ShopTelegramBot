from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from typing import Tuple

# Генерация клавиатур
"""
Параметры request_contact и request_location должны быть индексами аргументов кнопок для нужных кнопок
        start_keyboard(
            "Меню",
            "О создателе бота",
            "Способы оплаты",
            "Способы доставки",
            "Отправить номер телефона",
            "placeholder='Что заинтересовало ?'",
            "request_contact=4",
            "sizes=(2, 2, 1)"
        )
"""
def start_keyboard(
        *buttons: str,
        placeholder: str = None,
        requests_contact: int = None,
        requests_location: int = None,
        sizes: tuple = (2,),
):
    keyboard = ReplyKeyboardBuilder()
    for i, text in enumerate(buttons, start=0):
        if requests_contact and requests_contact == index:
            keyboard.add(KeyboardButton(text=text, requests_contact=True))
        elif requests_location and requests_location == index:
            keyboard.add(KeyboardButton(text=text, requests_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))
    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)

