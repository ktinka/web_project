from flask import Flask
from data import db_session
from data.characters_table import Character

app = Flask(__name__)


def search_characters(user_id):
    db_session.global_init("db/characters.db")
    db_sess = db_session.create_session()
    characters_info = {}
    for character in db_sess.query(Character).filter(Character.user_id == user_id):
        characters_info[character.id] = {"Имя": character.c_name,
                                         "Класс": character.c_class,
                                         "Раса": character.c_race,
                                         "Характеристики": character.c_characteristics,
                                         "Предыстория": character.c_about}
    return characters_info


def out_beautify_char(chars):
    return (f"\n\tСила: {chars[0]}; Модификатор: {calculate_mod(int(chars[0]))} \n"
            f"\tТелосложение: {chars[1]}; Модификатор: {calculate_mod(int(chars[1]))} \n"
            f"\tЛовкость: {chars[2]}; Модификатор: {calculate_mod(int(chars[2]))} \n"
            f"\tИнтеллект: {chars[3]}; Модификатор: {calculate_mod(int(chars[3]))} \n"
            f"\tМудрость: {chars[4]}; Модификатор: {calculate_mod(int(chars[4]))} \n"
            f"\tХаризма: {chars[5]}; Модификатор: {calculate_mod(int(chars[5]))}")


def out_beautify_all(character_info):
    return (f"Имя: {character_info["Имя"]} \n"
            f"\nКласс: {character_info["Класс"]} \n"
            f"\nРаса: {character_info["Раса"]} \n"
            f"\nХарактеристики: {out_beautify_char(character_info["Характеристики"].split(";"))} \n"
            f"\nПредыстория: {character_info["Предыстория"]} \n")


def out_chars_without_mod(chars):
    line = ""
    for key, value in chars.items():
        line += f"{key}: {value[0]} \n"
    return line


def calculate_mod(n):
    mod = (n - 10) // 2
    return mod


def save_character(user_id, c_name, c_class, c_race, c_characteristics, c_about):
    char_list = []
    for key, value in c_characteristics.items():
        char_list.append(str(value[0]))
    db_session.global_init("db/characters.db")
    ch1 = Character()
    ch1.user_id = user_id
    ch1.c_name = c_name
    ch1.c_class = c_class
    ch1.c_race = c_race
    ch1.c_characteristics = ";".join(char_list)  # отдельная функция
    ch1.c_about = c_about
    db_sess = db_session.create_session()
    db_sess.add(ch1)
    db_sess.commit()

