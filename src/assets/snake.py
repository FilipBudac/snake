from typing import Final

from PIL import ImageTk, Image

from src.assets.asset import Asset


class Snake(Asset):

    SNAKE_PATH: Final = '../assets/snake.png'
    SNAKE_TAG: Final = 'snake_tag'

    def __init__(self):
        super().__init__()
        self.positions = [(100, 100), (80, 100), (60, 100)]
        self.movement_step = 20
        self.speed = 100
        self.direction = 39

    def load_image(self):
        self.image = ImageTk.PhotoImage(Image.open(self.SNAKE_PATH))

    def draw(self, game):
        for x, y in self.positions:
            game.create_image(x, y, image=self.image, tag=self.SNAKE_TAG)

    def increase_speed(self):
        self.speed -= 2

    def grow(self, game):
        new_position = self.positions[-1]
        self.positions.append(new_position)
        game.create_image(*new_position, image=self.image, tag=self.SNAKE_TAG)

    def update(self, game):
        snake_parts = game.find_withtag(self.SNAKE_TAG)

        for snake_part, position in zip(snake_parts, self.positions):
            game.coords(snake_part, position)
