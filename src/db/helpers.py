from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.schema import Ships


def get_db_connect(db_path):
    db_engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker()
    Session.configure(bind=db_engine)
    session = Session()

    return session, db_engine


# функция для получения списка названий кораблей (для использования в параметризации тестов)
def get_ships_names(db_path):
    session, _ = get_db_connect(db_path)

    ships_names = []
    for ship in session.query(Ships.ship).all():
        ships_names.append(ship[0])

    session.close()

    return ships_names
