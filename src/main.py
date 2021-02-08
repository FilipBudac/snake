from tkinter import Canvas, ALL
from tkinter.tix import Tk
from typing import List, Final, Any
from src.assets.asset import AssetsEnum
from src.assets.board import Board
from src.assets.food import Food
from src.assets.snake import Snake


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
    assets = [snake, food, board]

    root = Tk()
    root.title("Snake Game")
    root.resizable(False, False)

    SnakeGame(assets)

    root.mainloop()

