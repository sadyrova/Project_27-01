from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import client_kb

class FSMAdmin(StatesGroup):
    name = State()
    direction = State()
    age = State()
    group = State()
    submit = State()

async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        await FSMAdmin.name.set()
        await message.answer("Как зовут?", reply_markup=client_kb.cancel_markup)
    else:
        await message.answer("Пиши в группу!")

async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = message.from_user.username
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Направление?")

async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMAdmin.next()
    await message.answer("Сколько лет?", reply_markup=client_kb.cancel_markup)

async def load_age(message: types.Message, state: FSMContext):
    if not  message.text.isdigit():
        await message.answer("Пиши числами!")
    elif int(message.text) < 16 or int(message.text) >40:
        await message.answer("Возрастное ограничение")
    else:
        async with state.proxy() as data:
            data['age'] = message.text
    await FSMAdmin.next()
    await message.answer("Какая группа?", reply_markup=client_kb.cancel_markup)

async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await FSMAdmin.next()
    await message.answer("Все верно?")


async def submit(message: types.Message, state: FSMContext):
    if message.text=="Да":
        await state.finish()
    elif message.text=="Нет":
        await state.finish()
    else:
        await message.answer("Нормально, пиши!")

async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.answer("Отменено")

def register_handlers_fsm_admin_mentor(dp:Dispatcher):
    dp.register_message_handler(cancel_reg, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_reg,
                                Text(equals="cancel", ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(submit, state=FSMAdmin.submit)