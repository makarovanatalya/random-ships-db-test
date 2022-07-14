from pathlib import Path
from random import choice

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.db_schema import Engines, Hulls, Model, Ships, Weapons
from src.models.builder import (EngineBuilder, HullBuilder, ShipBuilder,
                                WeaponBuilder)

# оставила путь к БД и подключение здесь, можно будет добавлять различные генераторы данных, используя одну схему
# если бы требовалась БД, стоило бы сделать отдельный конфиг + makefile для удобного запуска локальной базки

MAIN_DB_PATH = Path(Path.cwd().parent.parent, 'main.db')
MAIN_DB_ENGINE = create_engine(f'sqlite:///{MAIN_DB_PATH}')


Session = sessionmaker()
Session.configure(bind=MAIN_DB_ENGINE)


def db_filler(count_ships, count_weapons, count_hulls, count_engines):
    session = Session()

    for i in range(count_weapons):
        weapon = WeaponBuilder().random_build()
        weapon_transaction = Weapons(weapon.weapon,
                                     weapon.reload_speed,
                                     weapon.rotational_speed,
                                     weapon.diameter,
                                     weapon.power_volley,
                                     weapon.count)
        session.add(weapon_transaction)
    session.commit()

    for i in range(count_hulls):
        hull = HullBuilder().random_build()
        hull_transaction = Hulls(hull.hull,
                                 hull.armor,
                                 hull.type,
                                 hull.capacity)
        session.add(hull_transaction)
    session.commit()

    for i in range(count_engines):
        engine = EngineBuilder().random_build()
        engine_transaction = Engines(engine.engine,
                                     engine.power,
                                     engine.type)
        session.add(engine_transaction)
    session.commit()

    weapons = session.query(Weapons.weapon).all()
    hulls = session.query(Hulls.hull).all()
    engines = session.query(Engines.engine).all()

    for i in range(count_ships):
        weapon = choice(weapons)[0]
        hull = choice(hulls)[0]
        engine = choice(engines[0])

        ship = ShipBuilder().manual_build(weapon, hull, engine)
        ship_transaction = Ships(ship.ship,
                                 ship.weapon,
                                 ship.hull,
                                 ship.engine)
        session.add(ship_transaction)
    session.commit()

    session.close()


if __name__ == "__main__":
    Model.metadata.create_all(MAIN_DB_ENGINE)
    db_filler(count_ships=200, count_weapons=20, count_hulls=5, count_engines=6)
