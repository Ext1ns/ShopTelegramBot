import os

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.enums import ParseMode
from aiogram.utils.formatting import Bold, as_marked_section
from sqlalchemy.ext.asyncio import AsyncSession


from custom_filters.chat import MyFilter
from keyboards.reply_keyboard import start_keyboard
from database.query import orm_get_products
private_router = Router()
private_router.message.filter(MyFilter(['private']))


@private_router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        'Привет, добро пожаловать в магазин Ext1ns1 !',
        reply_markup=start_keyboard(
            'Меню',
            'О создателе бота',
            'Способы оплаты',
            'Способы доставки',
            placeholder='Что вас заинтересовало ?',
            sizes=(2,),
        )
    )


@private_router.message(or_f(Command('menu'), (F.text.lower() == 'меню')))
# @private_router.message(Command('menu'))
async def menu_command(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.img,
            caption=f"<strong>{product.name}\
                                </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
        )
    await message.answer('Меню:')


@private_router.message(or_f(Command('about'), (F.text.lower() == 'о создателе бота')))
@private_router.message(Command('about'))
async def about_command(message: types.Message):
    about = as_marked_section(
        Bold('О создателе бота:'),
        'Создатель бота: Саламов Г.А.',
        'Бот разработан в рамках проектной работы Яндекс Лицея',
        'GitHub: https://github.com/Ext1ns')
    await message.answer(about.as_html())


@private_router.message(or_f(Command('payment'), (F.text.lower() == 'способы оплаты')))
@private_router.message(Command('payment'))
async def payment_command(message: types.Message):
    pay = as_marked_section(
        Bold('Способы оплаты:'),
        'Оплата картой в боте',
        'При получении курьеру, карта/наличные',
        marker='\U00002714 '
    )
    await message.answer(pay.as_html())


@private_router.message(or_f(Command('shipping'), (F.text.lower() == 'способы доставки')))
@private_router.message(Command('shipping'))
async def shipping_command(message: types.Message):
    deliver = as_marked_section(
        Bold('Способы доставки:'),
        'СДЭК',
        'Почта России',
        'Авито доставка',
        marker='\U0001F4E6'
    )
    await message.answer(deliver.as_html())
