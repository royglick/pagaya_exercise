import curses
from classes import Game


def main(window: "curses.window") -> None:
    """Main function to set up and run the game."""
    curses.curs_set(0)
    window.nodelay(1)

    game = Game(window)

    if game.max_x < 5 or game.max_y < 5:
        print("Board size must be bigger than 5 in both axises")
        return

    while True:
        game.draw()
        key = window.getch()
        game.process_input(key)

        if game.paused or key == 53:
            continue

        if not game.update():
            window.addstr(game.max_y // 2, game.max_x // 2 - 5, "GAME OVER")
            window.addstr(
                game.max_y // 2 + 4, game.max_x // 2 - 7, f"Your Score Is {game.score}"
            )
            window.timeout(800)
            window.refresh()
            window.getch()
            break
        window.timeout(200)


if __name__ == "__main__":
    curses.wrapper(main)
