from Turtle import *


def main():
    test_game = Turtle()
    # Draw the pregame layout
    test_game.pregame(test_game.draw_square, test_game.draw_image)
    # Draw the default puzzle
    test_game.draw_default_puzzle()
    # Implement the onclick logic
    test_game.wds.onclick(test_game.click_handler)
    turtle.done()


if __name__ == "__main__":
    main()
