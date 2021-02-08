import random
from typing import Final
from PIL import Image, ImageTk
from src.assets.asset import Asset


class Food(Asset):

    FOOD_PATH: Final = '../assets/food.png'
    FOOD_TAG: Final = 'food_tag'

    def __init__(self):
        super().__init__()
        self.position = (50, 500)

    def load_image(self):
        self.image = ImageTk.PhotoImage(Image.open(self.FOOD_PATH))

    def draw(self, game):
        game.create_image(*self.position, image=self.image, tag=self.FOOD_TAG)

    def generate_food(self, game, width, height):
        x = random.randrange(20, width - 20, 20)
        y = random.randrange(20, height - 20, 20)
        self.position = (x, y)

        self.update(game)

    def check_collision(self, x, y) -> bool:
        collided = False

        if (self.position[0] - 20 < x < self.position[0] + 20) and (self.position[1] - 20 < y < self.position[1] + 20):
            collided = True

        return collided

    def update(self, game):
        game.coords(game.find_withtag(self.FOOD_TAG), *self.position)
