from abc import ABC, abstractmethod


class Attacker(ABC):

    @abstractmethod
    def attack(self, unit: 'Unit') -> None:
        pass


class Moveable(ABC):

    @abstractmethod
    def move(self, x: int, y: int) -> None:
        pass



class GameObject(ABC):
    def __init__(self, obj_id: int, name: str, x: int, y: int):
        self._id = obj_id
        self._name = name
        self._x = x
        self._y = y

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def _set_position(self, x: int, y: int) -> None:
        self._x = x
        self._y = y


class Building(GameObject, ABC):

    def __init__(self, obj_id: int, name: str, x: int, y: int, built: bool = False):
        super().__init__(obj_id, name, x, y)
        self._built = built

    def is_built(self) -> bool:
        return self._built

    def build(self) -> None:
        self._built = True


class Unit(GameObject, ABC):

    def __init__(self, obj_id: int, name: str, x: int, y: int, hp: float):
        super().__init__(obj_id, name, x, y)
        self._hp = hp

    def is_alive(self) -> bool:
        self._hp > 0

    def get_hp(self) -> float:
        return self._hp

    def receive_damage(self, damage: float) -> None:
        self._hp -= damage
        if self._hp < 0:
            self._hp = 0


class Archer(Unit, Attacker, Moveable):

    def __init__(self, obj_id: int, name: str, x: int, y: int, hp: float, attack_power: float):
        super().__init__(obj_id, name, x, y, hp)
        self._attack_power = attack_power

    def attack(self, unit: Unit) -> None:
        if self.is_alive():
            print(f"Лучник {self.get_name()} атакует {unit.get_name()} нанеся {self._attack_power} урона.")
            unit.receive_damage(self._attack_power)
        else:
            print(f"Лучник {self.get_name()} мертв и не может атаковать.")

    def move(self, x: int, y: int) -> None:
        self._set_position(x, y)
        print(f"Лучник {self.get_name()} переместился в точку ({x}, {y}).")


class Fort(Building, Attacker):

    def __init__(self, obj_id: int, name: str, x: int, y: int, built: bool = False, attack_power: float = 25.0):
        super().__init__(obj_id, name, x, y, built)
        self._attack_power = attack_power

    def attack(self, unit: Unit) -> None:
        if self.is_built():
            print(f"Крепость {self.get_name()} стреляет из пушек по {unit.get_name()}!")
            unit.receive_damage(self._attack_power)
        else:
            print(f"Крепость {self.get_name()} еще не достроена и не может стрелять!")


class MobileHouse(Building, Moveable):

    def __init__(self, obj_id: int, name: str, x: int, y: int, built: bool = True):
        super().__init__(obj_id, name, x, y, built)

    def move(self, x: int, y: int) -> None:
        self._set_position(x, y)
        print(f"Дом на колесах {self.get_name()} переехал на координаты ({x}, {y}).")
