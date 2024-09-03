---Snake Game---

This project implements a classic Snake game in Python, along with a testing framework for the game logic.

---Project Structure---

classes.py: Contains the main game classes including Game, Snake, Food, and others.
test_game.py: Implements a testing framework for the game logic.

---In Order To Play---

Just run 'python3 snake_game.py'.
The screen size will adjust itself to you terminal size.

---Running Tests---

The testing framework in test_game.py allows for automated testing of the game logic. It uses a text-based input system to set up and run game scenarios.
To run tests:

Execute tests.py
Input the number of test cases
For each test case, provide:

Board size (n)
Number of moves (k)
List of food positions
Sequence of moves


The test runner will output the score for each test case.

---Example Test Input---

5
3
[(1,2), (3,4)]
2
6
4

This sets up a 5x5 board, with 3 moves, food at positions (1,2) and (3,4), and moves the snake up, right, and left.
