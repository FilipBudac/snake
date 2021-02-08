from typing import Final
from src.assets.asset import Asset


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

