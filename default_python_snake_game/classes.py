import curses
from enum import Enum
import random
from typing import List, Optional, Tuple


class Directions(Enum):
    """Enumeration for snake movement directions."""

    UP = 50  # ascii of 2
    DOWN = 56  # ascii of 8
    LEFT = 52  # ascii of 4
    RIGHT = 54  # ascii of 6
    PAUSE = 53  # ascii of 5


class PositionObject:
    """Base class for game objects with position property."""

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    @property
    def position(self) -> Tuple[int, int]:
        """Return the current position of the object."""
        return (self.y, self.x)


class Food(PositionObject):
    """Represents the food in the game."""

    def __init__(self, y: int, x: int):
        super().__init__(y, x)

    def draw(self, window: "curses.window") -> None:
        """Draw the food on the game window."""
        window.addch(self.y, self.x, "*")


class SnakeSegment(PositionObject):
    """Represents a segment of the snake's body."""

    def __init__(self, y: int, x: int):
        super().__init__(y, x)

    def draw(self, window: "curses.window") -> None:
        """Draw the snake segment on the game window."""
        window.addch(self.y, self.x, "#")


class Snake:
    def __init__(self, initial_y: int, initial_x: int, length: int = 3):
        self.body: List[SnakeSegment] = [
            SnakeSegment(initial_y + i, initial_x) for i in range(length)
        ]
        self.direction = Directions.UP

    def new_head_location(self, new_head: SnakeSegment) -> SnakeSegment:

        if self.direction == Directions.UP:
            new_head.y -= 1
        elif self.direction == Directions.DOWN:
            new_head.y += 1
        elif self.direction == Directions.LEFT:
            new_head.x -= 1
        elif self.direction == Directions.RIGHT:
            new_head.x += 1

        return new_head

    def move(self) -> None:
        """Move the snake to its current direction."""
        head = self.body[0]
        new_head = self.new_head_location(SnakeSegment(head.y, head.x))
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self, food_y: int, food_x: int) -> None:
        """Make the food as the new head of the snake"""
        food_as_head = self.new_head_location(SnakeSegment(food_y, food_x))
        self.body.insert(0, food_as_head)

    def draw(self, window: "curses.window") -> None:
        """Draw the entire snake on the game window."""
        for segment in self.body:
            segment.draw(window)

    def check_collision(self, max_y: int, max_x: int) -> bool:
        """Check if the snake has collided with the wall or itself."""
        head = self.body[0]
        return (
            head.y in [0, max_y]
            or head.x in [0, max_x]
            or any(segment.position == head.position for segment in self.body[1:])
        )


class Game:
    """Main game class that manages the game state and logic."""

    def __init__(
        self,
        window: Optional["curses.window"] = None,
        board_size: Optional[int] = None,
        food_list: Optional[List[Food]] = None,
    ):
        self.window = window
        ## this suppose to differentiate between test cases (where there are no window element) to regular game
        if window:
            self.max_y, self.max_x = window.getmaxyx()
        elif board_size:
            self.max_y = self.max_x = board_size
        else:
            raise ValueError("Either window or board_size must be provided")
        self.snake = Snake(self.max_y // 2, self.max_x // 2)
        self.food_list = food_list or self.generate_food_list()
        self.food_index = 0
        self.food = self.food_list[self.food_index]
        self.score = 0
        self.paused = False

    def generate_food_list(self) -> List[Food]:
        """Generate food list with 10 elements at random positions."""
        food_list: List[Food] = [
            Food(random.randint(1, self.max_y - 2), random.randint(1, self.max_x - 2))
            for _ in range(10)
        ]
        return food_list

    def get_next_food_in_list(self) -> List[Food]:
        """Get the next food to place on screen."""
        while True:
            self.food_index += 1
            ## cycle through the list if reached to the end
            if self.food_index >= len(self.food_list):
                self.food_index = 0
            food = self.food_list[self.food_index]
            if food.position not in [seg.position for seg in self.snake.body]:
                return food

    def process_input(self, key: int) -> None:
        """Process user input to change snake direction."""
        if key == Directions.UP.value and self.snake.direction != Directions.DOWN:
            self.snake.direction = Directions.UP
        elif key == Directions.DOWN.value and self.snake.direction != Directions.UP:
            self.snake.direction = Directions.DOWN
        elif key == Directions.LEFT.value and self.snake.direction != Directions.RIGHT:
            self.snake.direction = Directions.LEFT
        elif key == Directions.RIGHT.value and self.snake.direction != Directions.LEFT:
            self.snake.direction = Directions.RIGHT
        elif key == Directions.PAUSE.value and self.paused == False:
            self.paused = True
        elif key == Directions.PAUSE.value and self.paused == True:
            self.paused = False

    def update(self) -> bool:
        """Update game state. Returns False if the game should end."""
        self.snake.move()

        if self.snake.check_collision(self.max_y - 1, self.max_x - 1):
            return False

        if self.snake.body[0].position == self.food.position:
            self.snake.grow(*self.food.position)
            self.food = self.get_next_food_in_list()
            self.score += 1

        return True

    def draw(self) -> None:
        """Draw the current game state."""
        self.window.clear()
        self.window.border(0)
        self.snake.draw(self.window)
        self.food.draw(self.window)
        if self.paused:
            self.window.addstr(0, 2, "Game Paused")
        self.window.refresh()
