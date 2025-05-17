import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_TOKEN
from info import classes_info, races_info

from search_characters import search_characters, out_beautify_all, save_character, out_chars_without_mod

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

char_keyboard = [[KeyboardButton(text='Вперёд!')]]
char_kb = ReplyKeyboardMarkup(keyboard=char_keyboard, resize_keyboard=True, one_time_keyboard=True)

save_keyboard = [[KeyboardButton(text='Сохранить персонажа')]]
save_kb = ReplyKeyboardMarkup(keyboard=save_keyboard, resize_keyboard=True, one_time_keyboard=True)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

# создаем маршрутизатор
dp = Dispatcher()

c_info = {}
nul_chars = {"Сила": [],
             "Телосложение": [],
             "Ловкость": [],
             "Интеллект": [],
             "Мудрость": [],
             "Харизма": []}


def nul_c_info():
    global c_info
    c_info = {"characteristics": {"Сила": [],
                                  "Телосложение": [],
                                  "Ловкость": [],
                                  "Интеллект": [],
                                  "Мудрость": [],
                                  "Харизма": []},
              "name": "",
              "class": "",
              "race": "",
              "about": ""}


nul_c_info()

char_values = [8, 10, 12, 13, 14, 15]
c_char_growth = []


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


@dp.message(Command('start'))
@dp.message(F.text == 'На главную')
async def start(message: types.Message):
    await message.reply("Привет! Я помогу тебе разобраться с листом персонажа в D&D!\n"
                        "Для начала скажи, нужно ли тебе узнать подробнее об этой игре или "
                        "сразу приступим к делу?\n"
                        "Кстати, ты можешь всегда \n"
                        "нажать 'Хватит', и я с тобой попрощаюсь ^^", reply_markup=start_kb)
    nul_c_info()


@dp.callback_query(F.data == "back_home")
async def start_2(call: CallbackQuery):
    await call.answer()
    await call.message.answer("Привет! Я помогу тебе разобраться с листом персонажа в D&D!\n"
                              "Для начала скажи, нужно ли тебе узнать подробнее об этой игре или "
                              "сразу приступим к делу?\n"
                              "Кстати, ты можешь всегда \n"
                              "нажать 'Хватит', и я с тобой попрощаюсь ^^", reply_markup=start_kb)


@dp.message(F.text == 'Хватит')
async def stop(message: types.Message):
    await message.reply("Пока-пока!")


@dp.message(Command('help'))
async def help(message: types.Message):
    nul_c_info()
    await message.reply("Я бот, призванный помочь новичкам в днд.")


@dp.message(F.text == 'Правила игры')
async def rules(message: types.Message):
    nul_c_info()
    await message.reply("Dungeons and Dragons (D&D) — коллаборативная "
                        "ролевая игра о приключениях в фэнтезийном мире. "
                        "Партия в D&D разворачивается под управлением гейм-мастера,"
                        " который создаёт игровой мир, ведёт приключение, "
                        "определяет правила, направляет взаимодействие "
                        "игроков по ходу сценария. \n\n"
                        "В D&D каждый игрок придумывает себе персонажа,"
                        " от лица которого он будет играть, заполняя лист со слабыми "
                        "и сильными сторонами героя. Этот лист я и помогу "
                        "тебе составить!", reply_markup=standard_kb)


characters_dict = {}


@dp.message(F.text == 'Мои персонажи')
async def my_characters(message: Message):
    global characters_dict
    nul_c_info()
    characters_dict = search_characters(message.from_user.id)
    if characters_dict == {}:
        await message.answer("Пока что их нет.", reply_markup=standard_kb)
    else:
        await message.answer('Вот:', reply_markup=create_char_inline_kb(characters_dict))


@dp.callback_query(F.data.startswith('char_'))
async def print_characters(call: CallbackQuery):
    await call.answer()
    char_id = int(call.data.replace('char_', ''))
    msg_text = out_beautify_all(characters_dict[char_id])
    await call.message.answer(msg_text, reply_markup=create_char_inline_kb(characters_dict))


@dp.message(F.text == 'Создать персонажа')
async def c_create(message: types.Message):
    nul_c_info()
    await message.reply("Начнём с имени")


@dp.message(F.text == 'Воин')
@dp.message(F.text == 'Варвар')
@dp.message(F.text == 'Колдун')
@dp.message(F.text == 'Паладин')
@dp.message(F.text == 'Следопыт')
@dp.message(F.text == 'Монах')
async def c_class(message: types.Message):
    global c_info
    c_info["class"] = message.text
    await message.reply(classes_info[message.text] + "\n\n\nТеперь выберите расу:", reply_markup=race_kb)


@dp.message(F.text == 'Человек')
@dp.message(F.text == 'Тифлинг')
@dp.message(F.text == 'Эльф')
@dp.message(F.text == 'Гном')
@dp.message(F.text == 'Драконорожденный')
@dp.message(F.text == 'Полуорк')
async def c_race(message: types.Message):
    global c_info
    c_info["race"] = message.text
    await message.reply(races_info[message.text] + "\n\n\nКакая у него/неё история?")


@dp.message(F.text == 'Вперёд!')
async def c_chars_start(message: types.Message):
    global c_info
    c_info["characteristics"] = nul_chars
    await message.reply("У каждого персонажа есть 6 характеристик: сила, телосложение, ловкость, "
                        "интеллект, мудрость и харизма. Подумай, какие из них наиболее важны "
                        "для твоего и напиши мне отдельными сообщениями "
                        "выбранные в порядке увеличения значимости"
                        "(следи за тем, чтобы они не повторялись): \n")


@dp.message(F.text == 'Сохранить персонажа')
async def c_save(message: types.Message):
    global c_info
    global name
    global c_char_growth
    await message.reply("Сохранил!", reply_markup=standard_kb)
    save_character(message.from_user.id, c_info["name"], c_info["class"],
                   c_info["race"], c_info["characteristics"], c_info["about"])
    name = ""
    nul_c_info()
    c_char_growth = []


@dp.message(F.text == 'Сила')
@dp.message(F.text == 'сила')
@dp.message(F.text == 'Телосложение')
@dp.message(F.text == 'телосложение')
@dp.message(F.text == 'Ловкость')
@dp.message(F.text == 'ловкость')
@dp.message(F.text == 'Интеллект')
@dp.message(F.text == 'интеллект')
@dp.message(F.text == 'Мудрость')
@dp.message(F.text == 'мудрость')
@dp.message(F.text == 'Харизма')
@dp.message(F.text == 'харизма')
async def c_chars(message: types.Message):
    global c_char_growth
    if len(c_char_growth) < 6:
        c_char_growth.append(message.text.capitalize())
        await message.reply("Выбрано: " + message.text)
    if len(c_char_growth) == 6:
        for char_i in range(len(c_char_growth)):
            c_info["characteristics"][c_char_growth[char_i]] = [char_values[char_i]]
        await message.reply(f"Ваши характеристики: \n{out_chars_without_mod(c_info["characteristics"])}",
                            reply_markup=save_kb)


@dp.message()
async def story(message: Message):
    global c_info
    text = message.text
    if c_info["name"] and c_info["about"]:
        await message.reply("Проверьте правильность написания, пожалуйста")
    elif c_info["name"] and not c_info["about"]:
        c_info["about"] = text
        await message.reply(f"Круто! А теперь переходим к "
                            f"самому интересному.", reply_markup=char_kb)
    else:
        name = text
        c_info["name"] = name
        await message.reply(f"Какого класса {name}?", reply_markup=class_kb)


if __name__ == '__main__':
    asyncio.run(main())

