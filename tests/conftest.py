from os import remove
from random import choice, randint

import pytest

from src.db.generator import get_db_connect
from src.db.helpers import get_ships_names
from src.db.schema import Engines, Hulls, Model, Ships, Weapons
from tests.config import MAIN_DB_PATH, TEST_DB_PATH


@pytest.fixture(scope='session')
def get_data_from_main_db():
    session, _ = get_db_connect(MAIN_DB_PATH)

    # получаем данные для работы с ними в тестовой БД
    original_weapons = session.query(Weapons).all()
    original_hulls = session.query(Hulls).all()
    original_engines = session.query(Engines).all()
    original_ships = session.query(Ships).all()

    data_from_main_db = (original_weapons, original_hulls, original_engines, original_ships)

    # получаем и обрабатываем данные для более удобной работы с ними в тестах
    complete_ships_data = session.query(Ships, Weapons, Hulls, Engines).join(Weapons, Hulls, Engines).all()
    data_for_test_cases = prepare_test_data(complete_ships_data)

    yield data_from_main_db, data_for_test_cases

    session.close()


@pytest.fixture(scope='session')
def make_test_db_and_get_data_for_cases(get_data_from_main_db):
    session, db_engine = get_db_connect(TEST_DB_PATH)
    Model.metadata.create_all(db_engine)

    # для каждой из таблиц составляющих:
    # подготавливаем транзакцию из данных, полученных из оригинальной БД, и заменяем в ней одно из значений на рандомное
    # складываем значения названий комплектующих в отдельные списки для рандомной замены значения в кораблях
    original_weapons, original_hulls, original_engines, original_ships = get_data_from_main_db[0]

    for_ships_randomization = {
        'weapon': [],
        'hull': [],
        'engine': []
    }

    for engine in original_engines:
        for_ships_randomization['engine'].append(engine.engine)

        test_db_engine_transaction = Engines(engine.engine, engine.power, engine.type)
        test_db_engine_transaction.change_random_attribute(randint(1, 20))
        session.add(test_db_engine_transaction)
    session.commit()

    for hull in original_hulls:
        for_ships_randomization['hull'].append(hull.hull)

        test_db_hull_transaction = Hulls(hull.hull, hull.armor, hull.type, hull.capacity)
        test_db_hull_transaction.change_random_attribute(randint(1, 20))
        session.add(test_db_hull_transaction)
    session.commit()

    for weapon in original_weapons:
        for_ships_randomization['weapon'].append(weapon.weapon)

        test_db_weapon_transaction = Weapons(weapon.weapon, weapon.reload_speed, weapon.rotational_speed,
                                             weapon.diameter, weapon.power_volley, weapon.count)
        test_db_weapon_transaction.change_random_attribute(randint(1, 20))
        session.add(test_db_weapon_transaction)
    session.commit()

    # для кораблей выбираем значение для замены из подготовленного словаря комплектующих
    for ship in original_ships:
        test_db_ship_transaction = Ships(ship.ship, ship.weapon, ship.hull, ship.engine)

        part_for_change = choice(tuple(for_ships_randomization.keys()))
        value_for_change = choice(for_ships_randomization[part_for_change])
        test_db_ship_transaction.change_attribute(part_for_change, value_for_change)
        session.add(test_db_ship_transaction)
    session.commit()

    # получаем и обрабатываем данные для более удобной работы с ними в тестах
    complete_ships_data = session.query(Ships, Weapons, Hulls, Engines).join(Weapons, Hulls, Engines).all()
    data_for_test_cases = prepare_test_data(complete_ships_data)

    original_data_for_test_cases = get_data_from_main_db[1]

    yield original_data_for_test_cases, data_for_test_cases

    # отключаемся и удаляем БД
    session.close()
    remove(TEST_DB_PATH)


def prepare_test_data(list_rows):
    data_for_test_cases = {}
    for row in list_rows:
        ship_data = row[0]
        weapon_data = row[1]
        hull_data = row[2]
        engine_data = row[3]

        data_for_test_cases[ship_data.ship] = {}

        data_for_test_cases[ship_data.ship]['weapon'] = {
            'reload_speed': weapon_data.reload_speed,
            'rotational_speed': weapon_data.rotational_speed,
            'diameter': weapon_data.diameter,
            'power_volley': weapon_data.power_volley,
            'count': weapon_data.count,
        }

        data_for_test_cases[ship_data.ship]['hull'] = {
            'armor': hull_data.armor,
            'type': hull_data.type,
            'capacity': hull_data.capacity,
        }

        data_for_test_cases[ship_data.ship]['engine'] = {
            'power': engine_data.power,
            'type': engine_data.type,
        }

        data_for_test_cases[ship_data.ship]['components'] = {
            'weapon': ship_data.weapon,
            'hull': ship_data.hull,
            'engine': ship_data.engine,
        }

    return data_for_test_cases


def pytest_generate_tests(metafunc):
    metafunc.parametrize('ships_name', get_ships_names(MAIN_DB_PATH))
