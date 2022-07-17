from random import choice

from config import MAIN_DB_PATH
from src.db.helpers import get_db_connect
from src.db.schema import Engines, Hulls, Model, Ships, Weapons
from src.models.builder import (EngineBuilder, HullBuilder, ShipBuilder,
                                WeaponBuilder)


def db_filler(count_ships, count_weapons, count_hulls, count_engines):
    session, db_engine = get_db_connect(MAIN_DB_PATH)
    Model.metadata.create_all(db_engine)

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
        engine = choice(engines)[0]

        ship = ShipBuilder().manual_build(weapon, hull, engine)
        ship_transaction = Ships(ship.ship,
                                 ship.weapon,
                                 ship.hull,
                                 ship.engine)
        session.add(ship_transaction)
    session.commit()

    session.close()


if __name__ == '__main__':
    db_filler(count_ships=200, count_weapons=20, count_hulls=5, count_engines=6)
