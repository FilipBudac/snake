import random
from abc import abstractmethod
from tkinter import Canvas, Frame, ALL
from tkinter.tix import Tk
from typing import List, Final, Any
from PIL import Image, ImageTk
from enum import Enum


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


class Food(Asset):

    FOOD_PATH: Final = './food.png'
    FOOD_TAG: Final = 'food_tag'

    def __init__(self):
        super().__init__()
        self.position = (50, 500)
        self.gen_interval = 8000

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


class Board(Asset):

    SCORE_TAG: Final = 'score_tag'

    def __init__(self):
        super().__init__()
        self.score = 0

    def load_image(self):
        pass

    def draw(self, game):
        game.create_text(50, 20, text=f"Score: {self.score}", tag=self.SCORE_TAG, fill="#ffffff", font=('Lucida Sans Unicode', 16))

    def update(self, game):
        self.score += 1
        game.itemconfigure(game.find_withtag(self.SCORE_TAG), text=f"Score: {self.score}", tag=self.SCORE_TAG)


class Snake(Asset):

    SNAKE_PATH: Final = './snake.png'
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


class SnakeGame(Canvas):

    WIDTH: Final = 700
    HEIGHT: Final = 600
    BACKGROUND_COLOR = 'black'

    LEFT: Final = 37
    RIGHT: Final = 39
    UP: Final = 38
    DOWN: Final = 40

    def __init__(self, assets: List[Any]):
        super().__init__(width=self.WIDTH, height=self.HEIGHT, background=self.BACKGROUND_COLOR)

        self.collision_interval = 100
        self.assets = assets
        self.start_game()

    def start_game(self):
        try:
            self.load_assets()
            self.draw_assets()

            self.bind_all("<Key>", self.key_pressed)

            self.pack()

            self.after(self.assets[AssetsEnum.SNAKE.value].speed, self.snake_action)

        except IOError:
            self.destroy()

    def load_assets(self):
        for asset in self.assets:
            asset.load_image()

    def draw_assets(self):
        for asset in self.assets:
            asset.draw(self)

    def snake_action(self):
        self.snake_food_collision()
        self.snake_collision()
        self.snake_movements()

        self.after(self.assets[AssetsEnum.SNAKE.value].speed, self.snake_action)

    def key_pressed(self, event):
        new_direction = event.keycode

        if (abs(new_direction - self.assets[AssetsEnum.SNAKE.value].direction)) == 2:
            return

        self.assets[AssetsEnum.SNAKE.value].direction = event.keycode

    def snake_movements(self):
        x, y = self.assets[AssetsEnum.SNAKE.value].positions[0]
        new_position = []

        if self.assets[AssetsEnum.SNAKE.value].direction == self.UP:
            new_position = (x, y - self.assets[AssetsEnum.SNAKE.value].movement_step)
        elif self.assets[AssetsEnum.SNAKE.value].direction == self.DOWN:
            new_position = (x, y + self.assets[AssetsEnum.SNAKE.value].movement_step)
        elif self.assets[AssetsEnum.SNAKE.value].direction == self.LEFT:
            new_position = (x - self.assets[AssetsEnum.SNAKE.value].movement_step, y)
        elif self.assets[AssetsEnum.SNAKE.value].direction == self.RIGHT:
            new_position = (x + self.assets[AssetsEnum.SNAKE.value].movement_step, y)

        if x < 0:
            new_position = (x + self.WIDTH, y)
        elif y < 0:
            new_position = (x, y + self.HEIGHT)
        elif x >= self.WIDTH:
            new_position = (x - self.WIDTH, y)
        elif y >= self.HEIGHT:
            new_position = (x, y - self.HEIGHT)

        if len(new_position) > 0:
            self.assets[AssetsEnum.SNAKE.value].positions = [new_position] + self.assets[AssetsEnum.SNAKE.value].positions[:-1]

        self.assets[AssetsEnum.SNAKE.value].update(self)

    def snake_food_collision(self):
        x, y = self.assets[AssetsEnum.SNAKE.value].positions[0]
        has_collied = self.assets[AssetsEnum.FOOD.value].check_collision(x, y)

        if not has_collied:
            return

        self.assets[AssetsEnum.FOOD.value].generate_food(self, self.WIDTH, self.HEIGHT)
        self.assets[AssetsEnum.BOARD.value].update(self)
        self.assets[AssetsEnum.SNAKE.value].grow(self)
        self.assets[AssetsEnum.SNAKE.value].increase_speed()

    def end_game(self):
        self.delete(ALL)
        self.create_text(
            self.winfo_width() // 2,
            self.winfo_height() // 2,
            text=f"Score: {self.assets[AssetsEnum.BOARD.value].score}",
            fill="#fff",
            font=('Lucida Sans Unicode', 22)
        )

    def snake_collision(self):
        x, y = self.assets[AssetsEnum.SNAKE.value].positions[0]
        for position in self.assets[AssetsEnum.SNAKE.value].positions[1:]:
            if position[0] == x and position[1] == y:
                self.end_game()


if __name__ == '__main__':
    snake = Snake()
    board = Board()
    food = Food()

    root = Tk()
    root.title("Snake Game")
    root.resizable(False, False)
    content = Frame(root)

    assets = [snake, food, board]
    game = SnakeGame(assets)

    root.mainloop()
