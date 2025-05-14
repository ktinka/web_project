import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_TOKEN

from search_characters import search_characters, out_beautify

start_keyboard = [[KeyboardButton(text='Правила игры'), KeyboardButton(text='Создать персонажа')],
                  [KeyboardButton(text="Мои персонажи")], [KeyboardButton(text="Хватит")]]
start_kb = ReplyKeyboardMarkup(keyboard=start_keyboard, resize_keyboard=True, one_time_keyboard=True)

standard_keyboard = [[KeyboardButton(text='На главную')], [KeyboardButton(text="Хватит")]]
standard_kb = ReplyKeyboardMarkup(keyboard=standard_keyboard, resize_keyboard=True, one_time_keyboard=True)

class_keyboard = [[KeyboardButton(text='Воин'), KeyboardButton(text='Варвар')],
                  [KeyboardButton(text='Колдун'), KeyboardButton(text='Паладин')],
                  [KeyboardButton(text='Следопыт'), KeyboardButton(text='Монах')]]
class_kb = ReplyKeyboardMarkup(keyboard=class_keyboard, resize_keyboard=True, one_time_keyboard=True)

race_keyboard = [[KeyboardButton(text='Человек'), KeyboardButton(text='Тифлинг')],
                 [KeyboardButton(text='Эльф'), KeyboardButton(text='Гном')],
                 [KeyboardButton(text='Драконорожденный'), KeyboardButton(text='Полуорк')]]
race_kb = ReplyKeyboardMarkup(keyboard=race_keyboard, resize_keyboard=True, one_time_keyboard=True)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

# создаем маршрутизатор
dp = Dispatcher()

c_info = {}

name = ""


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


def create_char_inline_kb(characters) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    # Добавляем кнопки вопросов
    for key, value in characters.items():
        builder.row(
            InlineKeyboardButton(
                text=value["Имя"],
                callback_data=f'char_{key}'
            )
        )
    # Добавляем кнопку "На главную"
    builder.row(
        InlineKeyboardButton(
            text='На главную',
            callback_data='back_home'
        )
    )
    # Настраиваем размер клавиатуры
    builder.adjust(1)
    return builder.as_markup()


@dp.callback_query(F.data == "На главную")
@dp.message(Command('start'))
@dp.message(F.text == 'На главную')
async def start(message: types.Message):
    await message.reply("Привет! Я помогу тебе разобраться с листом персонажа в D&D!\n"
                        "Для начала скажи, нужно ли тебе узнать подробнее об этой игре или "
                        "сразу приступим к делу?\n"
                        "Кстати, ты можешь всегда \n"
                        "нажать 'Хватит', и я с тобой попрощаюсь ^^", reply_markup=start_kb)


@dp.message(F.text == 'Хватит')
async def stop(message: types.Message):
    await message.reply("Пока-пока!")


@dp.message(Command('help'))
async def help(message: types.Message):
    await message.reply("Я бот, призванный помочь новичкам в днд.")


@dp.message(F.text == 'Правила игры')
async def address(message: types.Message):
    await message.reply("Rules of the game Dungeons & Dragons", reply_markup=standard_kb)


characters_dict = {}


@dp.message(F.text == 'Мои персонажи')
async def my_characters(message: Message):
    global characters_dict
    characters_dict = search_characters(message.from_user.id)
    if characters_dict == {}:
        await message.answer("Пока что их нет.", reply_markup=standard_kb)
    else:
        await message.answer('Вот:', reply_markup=create_char_inline_kb(characters_dict))


@dp.callback_query(F.data.startswith('char_'))
async def print_characters(call: CallbackQuery):
    await call.answer()
    char_id = int(call.data.replace('char_', ''))
    char_data = characters_dict[char_id]["Имя"]
    msg_text = out_beautify(characters_dict[char_id])
    await call.message.answer(msg_text, reply_markup=create_char_inline_kb(characters_dict))


@dp.message(F.text == 'Создать персонажа')
async def c_create(message: types.Message):
    await message.reply("Начнём с имени")


@dp.message(F.text == 'Воин')
async def c_class(message: types.Message):
    c_info["Класс"] = message
    await message.reply("Информация о классе 'Воин'\n"
                        "Теперь выберите расу", reply_markup=race_kb)


@dp.message(F.text == 'Человек')
async def c_class(message: types.Message):
    c_info["Раса"] = message
    await message.reply("Информация о расе 'Человек'\n"  # всё брать из info_about... -> JSON
                        "Какая у него/неё история?")


@dp.message()  # попробовать потом сделать через FSM
async def process_class(message: Message):
    global name
    text = message.text
    if name:
        await message.reply(f"Круто! А теперь переходим к "
                            f"самому интересному.")
    else:
        name = text
        await message.reply(f"Какого класса {name}?", reply_markup=class_kb)


if __name__ == '__main__':
    asyncio.run(main())  # начинаем принимать сообщения
