from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
from keyboards.client_kb import start_markup

# @dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Hello world!", reply_markup="start_markup")


# @dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    photo = open('media/dog.jpg', 'rb')
    await message.answer_photo(photo=photo, caption="Сам разбирайся!")

    # await bot.send_photo(
    #   message.from_user.id,
    #   photo=photo,
    #   caption="Сам разбирайся!"
    # )


# @dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("NEXT", callback_data="button_1")
    markup.add(button_1)

    question = "Какой национальный цветок Японии?"
    answer = [
        "Фиалка",
        "Роза",
        "Сакура",
        "Сирень",

    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="Стыдно не знать",
        open_period=5,
        reply_markup=markup
    )

# @dp.message_handler(commands=['dice'])
async def on_message(message: types.Message):
    await bot.send_message(message.from_user.id, f"Привет {message.from_user.username}! начинаем игру!")

    bot_data = await bot.send_dice(message.from_user.id)
    bot_data = bot_data['dice']['value']

    user_data = await bot.send_dice(message.from_user.id)
    user_data = user_data['dice']['value']

    if bot_data> user_data:
        await bot.send_message(message.from_user.id, "Вы проиграли!")
    elif bot_data < user_data:
        await bot.send_message(message.from_user.id, "Вы победили!")
    else:
        await bot.send_message(message.from_user.id, "Ничья!")

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(on_message, commands=['dice'])