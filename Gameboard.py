import os


class Gameboard:
    """Design the layout for the gameboard."""

    resource_path = "./Resources/"
    root_path = "./"
    current_puzzle = "mario"  # set default puzzle as "mario"
    correct_answer = []

    def __init__(
        self,
        puzzle=(-355, 320, 480, 480),
        leader=(170, 320, 185, 480),
        control=(-355, -205, 710, 115),
        reset=(80, -262),
        load=(180, -262),
        quit=(280, -262),
        thumbnail=(262.5, 250),
    ):
        """Inits the Gameboard object.
        x,y coordinate locate at top-left corner.
        Parameters
        ----------
        puzzle : tuple
            puzzle box size (x coord, y coord, length, width), by default (-355, 320, 480, 480)
        leader : tuple
            leader box size (x coord, y coord, length, width), by default (170, 320, 185, 480)
        control : tuple
            control box size (x coord, y coord, length, width), by default (-355, -205, 710, 115)
        reset : tuple
            reset button coordinate (x coord, y coord), by default (80, -262)
        load : tuple
            load button coordinate (x coord, y coord), by default (180, -262)
        quit : tuple
            quit button coordinate (x coord, y coord), by default (280, -262)
        thumbnail : tuple
            thumbnail coordinate (x coord, y coord), by default (262.5, 250)
        """
        self.puzzle = puzzle
        self.leader = leader
        self.control = control
        self.reset = reset
        self.load = load
        self.quit = quit
        self.thumbnail = thumbnail

    def get_available_puzzle(self):
        """Get all the puzzle that user can play with.

        Returns
        -------
        list
            List which contains all of the available puzzle
        """
        all_puzzle = [
            file for file in os.listdir(self.root_path) if file.endswith(".puz")
        ]
        return all_puzzle
