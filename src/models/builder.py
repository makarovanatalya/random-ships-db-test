from random import randint


class BuilderBaseClass:
    _id_counter = 0

    @classmethod
    def _inc(cls):
        cls._id_counter += 1
        return cls._id_counter

    def __init__(self):
        self._id = self._inc()


class ShipBuilder(BuilderBaseClass):

    def __init__(self):
        super().__init__()
        self.ship = f'Ship-{self._id}'

        self.engine = None
        self.hull = None
        self.weapon = None

    def manual_build(self, weapon, hull, engine):
        self.weapon = weapon
        self.hull = hull
        self.engine = engine

        return self


class WeaponBuilder(BuilderBaseClass):

    def __init__(self):
        super().__init__()
        self.weapon = f'Weapon-{self._id}'

        self.reload_speed = None
        self.rotational_speed = None
        self.diameter = None
        self.power_volley = None
        self.count = None

    def random_build(self):
        self.reload_speed = randint(1, 20)
        self.rotational_speed = randint(1, 20)
        self.diameter = randint(1, 20)
        self.power_volley = randint(1, 20)
        self.count = randint(1, 20)

        return self


class HullBuilder(BuilderBaseClass):

    def __init__(self):
        super().__init__()
        self.hull = f'Hull-{self._id}'

        self.armor = None
        self.type = None
        self.capacity = None

    def random_build(self):
        self.armor = randint(1, 20)
        self.type = randint(1, 20)
        self.capacity = randint(1, 20)

        return self


class EngineBuilder(BuilderBaseClass):

    def __init__(self):
        super().__init__()
        self.engine = f'Engine-{self._id}'

        self.power = None
        self.type = None

    def random_build(self):
        self.power = randint(1, 20)
        self.type = randint(1, 20)

        return self
