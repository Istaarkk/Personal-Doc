import math
from abc import ABC, abstractmethod


class Vehicule:
    def __init__(self, porte: int = 2):
        self.porte = porte


class Animal:
    def __init__(self, patte: int = 4, queue: bool = False):
        self.patte = patte
        self.queue = queue


class Deplacement(ABC):
    @property
    @abstractmethod
    def x(self):
        pass

    @x.setter
    @abstractmethod
    def x(self, value):
        pass

    @property
    @abstractmethod
    def y(self):
        pass

    @y.setter
    @abstractmethod
    def y(self, value):
        pass

    @property
    @abstractmethod
    def z(self):
        pass

    @z.setter
    @abstractmethod
    def z(self, value):
        pass

    @abstractmethod
    def move_to(self, x: float, y: float, z: float, zone: str):
        pass


class Volant(Deplacement):
    def __init__(self):
        self._x = 0
        self._y = 0
        self._z = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def move_to(self, x: float, y: float, z: float, zone: str = '') -> str:
        if z <= 0:
            raise ValueError("z doit être > 0 pour voler")
        self.x, self.y, self.z = x, y, z
        return f"se déplace vers {x}, {y}, {z} en volant"


class Courant(Deplacement):
    def __init__(self):
        self._x = 0
        self._y = 0
        self._z = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def move_to(self, x: float, y: float, z: float, zone: str) -> str:
        if z != 0 or zone != 'terre':
            raise ValueError("z doit être 0 et zone 'terre'")
        self.x, self.y = x, y
        return f"se déplace vers {x}, {y} en courant"


class Marchant(Deplacement):
    def __init__(self):
        self._x = 0
        self._y = 0
        self._z = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def move_to(self, x: float, y: float, z: float, zone: str) -> str:
        if z != 0 or zone != 'terre':
            raise ValueError("z doit être 0 et zone 'terre'")
        self.x, self.y = x, y
        return f"se déplace vers {x}, {y} en marchant"


class Roulant(Deplacement):
    def __init__(self):
        self._x = 0
        self._y = 0
        self._z = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def move_to(self, x: float, y: float, z: float, zone: str) -> str:
        if z != 0 or zone != 'terre':
            raise ValueError("z doit être 0 et zone 'terre'")
        self.x, self.y = x, y
        return f"se déplace vers {x}, {y} en roulant"


class Flottant(Deplacement):
    def __init__(self):
        self._x = 0
        self._y = 0
        self._z = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def move_to(self, x: float, y: float, z: float, zone: str) -> str:
        if z != 0 or zone != 'mer':
            raise ValueError("z doit être 0 et zone 'mer'")
        self.x, self.y = x, y
        return f"se déplace vers {x}, {y} en flottant"


class Nageant(Deplacement):
    def __init__(self):
        self._x = 0
        self._y = 0
        self._z = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def move_to(self, x: float, y: float, z: float, zone: str) -> str:
        if z >= 0 or zone != 'mer':
            raise ValueError("z doit être < 0 et zone 'mer'")
        self.x, self.y, self.z = x, y, z
        return f"se déplace vers {x}, {y}, {z} en nageant"


class Humain(Marchant, Courant, Nageant, Flottant):
    def __init__(self):
        Marchant.__init__(self)
        Courant.__init__(self)
        Nageant.__init__(self)
        Flottant.__init__(self)
        self.patte = 2

    def move_to(self, x: float, y: float, z: float, zone: str) -> str:
        distance = math.sqrt(x ** 2 + y ** 2)
        if zone == "mer":
            if z < 0:
                return Nageant.move_to(self, x, y, z, zone)
            return Flottant.move_to(self, x, y, z, zone)
        if 2.0 <= distance <= 10.0:
            return Courant.move_to(self, x, y, z, zone)
        return Marchant.move_to(self, x, y, z, zone)

class VoitureSansPermis(Vehicule, Roulant):
    def __init__(self, porte: int = 2):
        Vehicule.__init__(self, porte)
        Roulant.__init__(self)


class Berline(Vehicule, Roulant):
    def __init__(self, porte: int = 5):
        Vehicule.__init__(self, porte)
        Roulant.__init__(self)


class Moto(Vehicule, Roulant):
    def __init__(self, porte: int = 0):
        Vehicule.__init__(self, porte)
        Roulant.__init__(self)


class Hors_Bord(Vehicule, Flottant):
    def __init__(self, porte: int = 0):
        Vehicule.__init__(self, porte)
        Flottant.__init__(self)


class Spitfire(Vehicule, Volant):
    def __init__(self, porte: int = 0):
        Vehicule.__init__(self, porte)
        Volant.__init__(self)


class Canard(Animal, Volant, Marchant, Courant, Nageant, Flottant):
    def __init__(self, patte: int = 2, queue: bool = True):
        Animal.__init__(self, patte, queue)
        Volant.__init__(self)
        Marchant.__init__(self)
        Courant.__init__(self)
        Nageant.__init__(self)
        Flottant.__init__(self)

    def move_to(self, x: float, y: float, z: float, zone: str) -> str:
        distance = math.sqrt(x ** 2 + y ** 2)
        if zone == "mer":
            if z < 0:
                return Nageant.move_to(self, x, y, z, zone)
            return Flottant.move_to(self, x, y, z, zone)
        if 2.0 <= distance <= 10.0:
            return Courant.move_to(self, x, y, z, zone)
        if zone == "terre" and z == 0:
            return Marchant.move_to(self, x, y, z, zone)
        if z > 0:
            return Volant.move_to(self, x, y, z, zone)
        raise ValueError("Mouvement impossible")


class Poisson(Animal, Nageant, Flottant):
    def __init__(self, patte: int = 0, queue: bool = True):
        Animal.__init__(self, patte, queue)
        Nageant.__init__(self)
        Flottant.__init__(self)


class Cygne(Animal, Volant, Flottant):
    def __init__(self, patte: int = 2, queue: bool = True):
        Animal.__init__(self, patte, queue)
        Volant.__init__(self)
        Flottant.__init__(self)

    def move_to(self, x: float, y: float, z: float, zone: str) -> str:
        if zone == "mer":
            return Flottant.move_to(self, x, y, z, zone)
        if z > 0:
            return Volant.move_to(self, x, y, z, zone)
        raise ValueError("Le cygne ne se déplace pas sur terre")
