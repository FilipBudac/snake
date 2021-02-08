from enum import Enum
from abc import abstractmethod


class AssetsEnum(Enum):
    SNAKE = 0
    FOOD = 1
    BOARD = 2


class Asset:

    def __init__(self):
        self.image = None

    @abstractmethod
    def load_image(self):
        pass

    @abstractmethod
    def draw(self, game):
        pass

    @abstractmethod
    def update(self, game):
        pass
