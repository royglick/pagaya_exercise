from ast import literal_eval
from typing import List, Tuple
from classes import Game, Snake, Food, Directions, PositionObject


class TestGame(Game):
    def __init__(self, n: int, foods: List[Tuple[int, int]]):
        food_list = [Food(y, x) for y, x in foods]
        super().__init__(window=None, board_size=n, food_list=food_list)

    def process_test_input(self, move: str) -> None:
        for char in move[::-1]:  # Process characters from right to left
            if char == "2":
                self.snake.direction = Directions.UP
                break
            elif char == "8":
                self.snake.direction = Directions.DOWN
                break
            elif char == "4":
                self.snake.direction = Directions.LEFT
                break
            elif char == "6":
                self.snake.direction = Directions.RIGHT
                break


def main():

    num_cases = int(input())
    for case in range(1, num_cases + 1):
        n = int(input())  # Board size
        k = int(input())  # Number of moves
        foods = literal_eval(input())

        game = TestGame(n, foods)

        for _ in range(k):
            move = input().strip()
            game.process_test_input(move)
            if not game.update():
                break

        print("Case #{}: {}".format(case, game.score))


if __name__ == "__main__":
    main()
