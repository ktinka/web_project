from flask import Flask
from data import db_session
from data.characters_table import Character

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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


def out_beautify(character_info):
    return (f"Имя: {character_info["Имя"]} \n"
            f"Класс: {character_info["Класс"]} \n"
            f"Раса: {character_info["Раса"]} \n"
            f"Характеристики: {character_info["Характеристики"]} \n"
            f"Предыстория: {character_info["Предыстория"]} \n")

def main():
    db_session.global_init("db/characters.db")
    # app.run()
    """db_sess = db_session.create_session()
    db_sess.add(ch1)
    db_sess.commit()"""


if __name__ == '__main__':
    main()
