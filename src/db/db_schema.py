from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()


class Ships(Model):
    __tablename__ = 'ships'

    ship = Column(String(50), primary_key=True)
    weapon = Column(String(50), ForeignKey('weapons.weapon'))
    hull = Column(String(50), ForeignKey('hulls.hull'))
    engine = Column(String(50), ForeignKey('engines.engine'))

    def __init__(self, ship, weapon, hull, engine):
        self.ship = ship
        self.weapon = weapon
        self.hull = hull
        self.engine = engine


class Weapons(Model):
    __tablename__ = 'weapons'

    weapon = Column(String(50), primary_key=True)
    reload_speed = Column(Integer)
    rotational_speed = Column(Integer)
    diameter = Column(Integer)
    power_volley = Column(Integer)
    count = Column(Integer)

    def __init__(self, weapon, reload_speed, rotational_speed, diameter, power_volley, count):
        self.weapon = weapon
        self.reload_speed = reload_speed
        self.rotational_speed = rotational_speed
        self.diameter = diameter
        self.power_volley = power_volley
        self.count = count


class Hulls(Model):
    __tablename__ = 'hulls'

    hull = Column(String(50), primary_key=True)
    armor = Column(Integer)
    type = Column(Integer)
    capacity = Column(Integer)

    def __init__(self, hull, armor, type, capacity):
        self.hull = hull
        self.armor = armor
        self.type = type
        self.capacity = capacity


class Engines(Model):
    __tablename__ = 'engines'

    engine = Column(String(50), primary_key=True)
    power = Column(Integer)
    type = Column(Integer)

    def __init__(self, engine, power, type):
        self.engine = engine
        self.power = power
        self.type = type
