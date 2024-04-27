from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from custom_filters.chat import MyFilter, IsAdmin
from keyboards.reply_keyboard import start_keyboard
from database.query import orm_add_product, orm_get_products

admin_router = Router()
admin_router.message.filter(MyFilter(['private']), IsAdmin())

ADMIN_KEYBOARD = start_keyboard(
    'Добавить товар',
    'Ассортимент',
    placeholder='Выберите действие',
    sizes=(2,),
)

@admin_router.message(Command('admin'))
async def add_command(message: types.Message):
    await message.answer('Что будете делать ?', reply_markup=ADMIN_KEYBOARD)

@admin_router.message(F.text == 'Ассортимент')
async def list_of_products_command(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.img,
            caption=f"<strong>{product.name}\
                                </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
        )
    await message.answer('Вот список товаров')



# Машина состояний

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    img = State()

    txts = {
        'AddProduct:name': 'Введите название товара заново',
        'AddProduct:description': 'Введите описание товара заново',
        'AddProduct:price': 'Введите стоимость товара заново',
        'AddProduct:img': 'Это последний шаг...',
    }


@admin_router.message(StateFilter(None), F.text == "Добавить товар")
async def add_product_command(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)

# * - Любое состояние пользователя
@admin_router.message(StateFilter('*'), Command("Отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler_command(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state is None:
        return
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KEYBOARD)


@admin_router.message(StateFilter('*'), Command("Назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def cancel_handler_command(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state == AddProduct.name:
        await message.answer('Предыдущего шага нет, введите название товара или напишите "отмена"')
        return

    past = None
    for step in AddProduct.__all_states__:
        if step.state == curr_state:
            await state.set_state(past)
            await message.answer(f'Вы вернулись к прошлому шагу \n {AddProduct.txts[past.state]}')
            return
        past = step

@admin_router.message(AddProduct.name, F.text)
async def add_name_command(message: types.Message, state: FSMContext):
    if len(message.text) > 100:
        await message.answer('Название не должно превышать 100 символов. Введите название снова')
        return

    await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.name)
async def add_name_command_error(message: types.Message, state: FSMContext):
    await message.answer('Введены не допустимые данные, введите текст названия для товара')


@admin_router.message(AddProduct.description, F.text)
async def add_description_command(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара")
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.description)
async def add_description_command_error(message: types.Message, state: FSMContext):
    await message.answer('Введены не допустимые данные, введите текст для описания товара')

@admin_router.message(AddProduct.price, F.text)
async def add_price_command(message: types.Message, state: FSMContext):
    try:
        float(message.text)
    except ValueError:
        await message.answer('Введите правильное значение цены')
        return

    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.img)

@admin_router.message(AddProduct.price)
async def add_price_command_error(message: types.Message, state: FSMContext):
    await message.answer('Введены не допустимые данные, введите цену для товара')

# [-1] - фото, с самым большим разрешением
@admin_router.message(AddProduct.img, F.photo)
async def add_image_command(message: types.Message, state: FSMContext, session: AsyncSession):

    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        await orm_add_product(session, data)
        await message.answer("Товар успешно добавлен", reply_markup=ADMIN_KEYBOARD)
        await state.clear()
    except Exception as e:
        await message.answer(
            f'Ошибка \n{str(e)}\n Я тут не виноват, думайте сами', reply_markup=ADMIN_KEYBOARD)
        await state.clear()

@admin_router.message(AddProduct.img)
async def add_image_command_error(message: types.Message, state: FSMContext):
    await message.answer("Отправьте фото товара")