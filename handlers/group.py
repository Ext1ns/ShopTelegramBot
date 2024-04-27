from aiogram import types, Router, F, Bot
from aiogram.filters import Command


from custom_filters.chat import MyFilter
from general.must_delete_words import del_words


group_router = Router()
group_router.message.filter(MyFilter(['group', 'supergroup']))
group_router.edited_message.filter(MyFilter(['group', 'supergroup']))

@group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()


@group_router.message()
async def clean_func(message: types.Message):
    if delete_words.intersection(message.text.lower().split()):
        await message.answer(f'{message.from_user.first_name}, А-та-та, аккуратнее. Забаню ;)')
        await message.delete()