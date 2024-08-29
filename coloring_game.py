import random
from typing import List
from enum import Enum

BOARD_SIZE: int = 18
ALLOWED_MOVES: int = 21


class ColorEnum(Enum):
    RED = "r"
    GREEN = "g"
    BLUE = "b"
    YELLOW = "y"


class Color:
    def __init__(self, code: ColorEnum):
        self.code = code

    def __repr__(self) -> str:
        return self.code.value


class Cell:
    def __init__(self, color: Color, row: int, col: int):
        self.color = color
        self.row = row
        self.col = col


class Board:
    def __init__(self, size: int, colors: List[Color]):
        self.size = size
        self.colors = colors
        self.grid = self._initialize_grid()

    def _initialize_grid(self) -> List[List[Cell]]:
        return [
            [Cell(random.choice(self.colors), i, j) for j in range(self.size)]
            for i in range(self.size)
        ]

    def get_neighbors_cells(self, cell: Cell) -> List[Cell]:
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = cell.row + dx, cell.col + dy
            # check that we dont exceed board limits
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                neighbors.append(self.grid[new_row][new_col])
        return neighbors


class GameState:
    def __init__(self, board: Board):
        self.board = board
        self.moves_used = 0

    def is_game_over(self) -> bool:
        first_color = self.board.grid[0][0].color
        return (
            all(cell.color == first_color for row in self.board.grid for cell in row)
            or self.moves_used > ALLOWED_MOVES
        )


class GameActions:
    @staticmethod
    def spill_color(state: GameState, new_color: Color) -> None:
        # if the user chose the existing color, do nothing
        if new_color == state.board.grid[0][0].color:
            return

        GameActions.paint_neighbors(state.board, state.board.grid[0][0], new_color)

    @staticmethod
    def paint_neighbors(board: Board, start_cell: Cell, new_color: Color) -> None:
        # the first cell is always considered as a neighbor
        old_color = start_cell.color
        neighbors_stack = [start_cell]

        while neighbors_stack:
            current_cell = neighbors_stack.pop()
            if current_cell.color != old_color:
                continue

            current_cell.color = new_color
            # invite new neighbors to check
            neighbors_stack.extend(board.get_neighbors_cells(current_cell))


class Game:
    def __init__(self):
        self.colors = [
            Color(ColorEnum.RED),
            Color(ColorEnum.BLUE),
            Color(ColorEnum.GREEN),
            Color(ColorEnum.YELLOW),
        ]
        self.board = Board(BOARD_SIZE, self.colors)
        self.state = GameState(self.board)

    def play_turn(self, color: Color) -> bool:
        self.state.moves_used += 1
        GameActions.spill_color(self.state, color)
        if self.state.is_game_over():
            return True
        return False

    def print_board(self):
        for row in self.board.grid:
            print([cell.color for cell in row])


def main():
    game = Game()

    while True:
        game.print_board()
        print("Choose Color (r/b/g/y):")
        chosen_color_code = input().lower()

        # TODO: find a more readable way to filter undesired inputs
        chosen_color = next(
            (color for color in game.colors if color.code.value == chosen_color_code),
            None,
        )

        if chosen_color is None:
            print("Invalid color. Please choose r, b, g, or y.")
            continue

        game_over = game.play_turn(chosen_color)

        print(f"Moves used: {game.state.moves_used}")
        if game_over:
            # TODO: redundant use of ALLOWED_MOVES (twice in the code), split win/lose cases better
            if game.state.moves_used <= ALLOWED_MOVES:
                print(f"You won in {game.state.moves_used} moves!")
            else:
                print(f"Game over! You have exeeded 21 moves, try again!")
            break


if __name__ == "__main__":
    main()
