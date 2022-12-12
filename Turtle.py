import turtle
import time
import random
from Tile import *
from PositionService import *
from copy import deepcopy
from Gameboard import *
import datetime
import os


def bubble_sort(list):
    """To sort the leader

    Parameters
    ----------
    list : list
        Leaders list for specific puzzle game
    """
    for passnum in range(len(list) - 1, 0, -1):
        for i in range(passnum):
            if int(list[i].split()[1]) > int(list[i + 1].split()[1]):
                temp = list[i]
                list[i] = list[i + 1]
                list[i + 1] = temp
    return list


def write_error_log(err_msg, func):
    """Write the error log

    Parameters
    ----------
    err_msg : str
        error mesage
    func : str
        Error comes from this function
    """
    now_time = datetime.datetime.now()
    with open("./puzzle.err", "a", encoding="utf-8") as f:
        f.write(f"{now_time.strftime('%c')}: {err_msg}. LOCATION: {func}()\n")


def swap_element_in_list(list, element1, element2):
    """Swap the index of element1 and element2

    Parameters
    ----------
    list : list
        List of Tile object
    element1 : Tile object
        Tile object
    element2 : Tile object
        Tile object

    """
    index1, index2 = list.index(element2), list.index(element1)
    list[index1], list[index2] = list[index2], list[index1]


class Turtle(Gameboard):
    currrent_tile_list = []  # store the current tile
    click_count = 0  # how many times user move the tile

    # By rule, the game doesn't end even if user click reset button.
    # Thus, I use the boolean logic to prevent user from winning the game directly.
    # User can win the game only if self.is_reset == False.
    # Thus, after reset the puzzle, set is_reset = True. User need to swap the tile to turn
    # self.is_reset == False.
    is_reset = False

    def __init__(
        self,
        name="Tim",
        play_times="10",
        puzzle=(-355, 320, 480, 480),
        leader=(170, 320, 185, 480),
        control=(-355, -205, 710, 115),
        reset=(80, -262),
        load=(180, -262),
        quit=(280, -262),
        thumbnail=(262.5, 250),
        ttl=turtle.Turtle(),
        wds=turtle.Screen(),
        eraser=turtle.Turtle(),
        error=turtle.Turtle(),
        leader_pencil=turtle.Turtle(),
    ):
        super().__init__(
            puzzle=(-355, 320, 480, 480),
            leader=(170, 320, 185, 480),
            control=(-355, -205, 710, 115),
            reset=(80, -262),
            load=(180, -262),
            quit=(280, -262),
            thumbnail=(262.5, 250),
        )
        self.name = name
        self.play_times = play_times
        self.wds = wds
        # Create a eraser turtle for write player moves and clear player moves
        self.eraser = eraser
        self.eraser.pencolor("black")
        self.eraser.speed(0)
        self.eraser.hideturtle()

        # Create a error turtle for handling error message
        self.err = error
        self.err.pencolor("black")
        self.err.speed(0)
        self.err.hideturtle()

        # Create a leader turtle for handling each leader's information
        self.leader_pencil = leader_pencil
        self.leader_pencil.pencolor("blue")
        self.leader_pencil.speed(0)
        self.leader_pencil.hideturtle()

        # Create a drawing turtle to draw the layout and each tile
        self.ttl = ttl
        self.ttl.pencolor("black")
        self.ttl.speed(0)
        self.ttl.width(4)  # thickness of turtle
        self.ttl.hideturtle()

    def puzzle_to_list(self, puzzle):
        """Sort the puzzle's metadata to a list for turtle do play the game

        Parameters
        ----------
        puzzle : str
            Puzzle name

        Returns
        -------
        tuple
            (relative path of each tile, size of tile, puzzle thumbnail)

        Raises
        ------
        ValueError
            If user want to play puzzle not in the range 2*2, 3*3, or 4*4, shows the file_error image.
        FileNotFoundError
            If user input wrong puzzle name, or puzzle doesn't exist, shows the file_error image.
        """
        try:
            # Clean data
            path = Gameboard.root_path + puzzle + ".puz"
            with open(
                path,
                "r",
                encoding="utf-8",
            ) as f:
                gif_data = f.readlines()[4:]
                f.seek(0)
                # Get the tile size
                gif_size = f.readlines()[2].strip("\n").strip("size: ")
                f.seek(0)
                # Get the puzzle thumbnail
                gif_thumbnail = f.readlines()[3].strip(
                    "\n").strip("thumbnail: ")
                if len(gif_data) not in [4, 9, 16]:
                    raise ValueError("Puzzle size should be 4, 9 or 16.")
                for i in range(len(gif_data)):
                    # Get relative path of each tile
                    gif_data[i] = gif_data[i].strip(
                        "\n").strip(str(i + 1) + ": ")
                    if os.path.exists(Gameboard.root_path + gif_data[i]) is False:
                        raise FileNotFoundError(
                            f"{Gameboard.root_path + gif_data[i]} <-- Cannot find this file!"
                        )
            return gif_data, int(gif_size), gif_thumbnail
        except FileNotFoundError as error:
            write_error_log(error, "load_click")
            self.draw_error("/file_error.gif")
        except ValueError as error2:
            write_error_log(error2, "load_click")
            self.draw_error("/file_error.gif")

    def splash_screen(self):
        """Show the Splash Screen before gameplay starts"""
        self.wds.setup(800, 730)
        self.wds.addshape(Turtle.resource_path + "/splash_screen.gif")
        # set the turtle shape to shape with a given name
        self.ttl.shape(Turtle.resource_path + "/splash_screen.gif")
        time.sleep(1)
        self.ttl.hideturtle()

    def get_user_data(self):
        """Get the user name and let user select the number of "moves"
        they can have to unscramble the puzzle
        """
        self.name = self.wds.textinput("CS 5001 Puzzle Slide", "Your name:")
        self.play_times = self.wds.numinput(
            "CS 5001 Puzzle Slide - Moves",
            "Enter the number of moves (chances) you want (5-200)?",
            minval=5,
            maxval=200,
        )

    def write_leader(self):
        """Update the leader board corresponding to the puzzle"""
        # Always shows the top 5 - to do
        self.leader_pencil.clear()
        self.leader_pencil.penup()
        self.leader_pencil.setpos(195, 150)
        self.leader_pencil.pendown()
        # Create a empty list to store current puzzzle top 5 leader
        current_leader = []
        with open("./leader.txt", "r", encoding="utf-8") as f:
            for line in f:
                puzzle = line.strip("\n").split(" ")[2]
                if puzzle == self.current_puzzle:
                    current_leader.append(line)

        leader_Y_position = 130  # first leader showup position
        # Sort the leader from best to worst by bubble sort
        bubble_sort(current_leader)

        # Write leader board information
        self.leader_pencil.write(
            f"Puzzle: {self.current_puzzle}\nLeaders: ",
            align="left",
            font=("Calibri", 15, "bold"),
        )
        for i in range(len(current_leader)):
            if i > 4:  # only shows up 5 leaders
                break
            self.leader_pencil.penup()
            self.leader_pencil.setpos(195, leader_Y_position)
            self.leader_pencil.pendown()
            self.leader_pencil.write(
                f"{current_leader[i].split()[0]}: {current_leader[i].split()[1]}",
                align="left",
                font=("Calibri", 15, "bold"),
            )
            leader_Y_position -= 20

    def draw_square(self, tpl):
        """Tell turtle to draw a square.

        Parameters
        ----------
        tpl : tuple
            The top-left x,y coordinate and the length, width of the square.
        """
        x, y, length, width = tpl
        self.ttl.penup()  # pull the pen up
        self.ttl.setpos(x, y)  # set a position
        self.ttl.pendown()  # pull the pen down
        # Draw square
        self.ttl.forward(length)
        self.ttl.right(90)
        self.ttl.forward(width)
        self.ttl.right(90)
        self.ttl.forward(length)
        self.ttl.right(90)
        self.ttl.forward(width)
        self.ttl.right(90)

    def draw_image(self, tpl, gif):
        """Tell turtle to draw a circle.

        Parameters
        ----------
        tpl : tuple
            The top-left x,y coordinate of the image.
        gif : gif
            Image in the form of GIF.
        """
        x, y = tpl
        self.ttl.penup()  # pull the pen up
        self.ttl.setpos(x, y)  # set a position
        self.ttl.pendown()  # pull the pen down
        self.wds.addshape(gif)
        self.ttl.shape(gif)
        # Whatever the shape of the turtle is, it is printed at that point
        # and continues with the next instructions.
        astamp = self.ttl.stamp()
        return astamp

    def draw_puzzle(self, list, size, thumbnail):
        """Tell turtle to draw the puzzle, and write the leaderboard.
        Additionally, create tile objects as well.

        Parameters
        ----------
        list : list
            List of each tile of the puzzle.
        size : int
            Size of the tile.
        thumbnail : GIF
            The image of the puzzle.
        """
        # create a empty list to store created tile object
        lst = []

        # safe the correct answer by making a deepcopy in order to
        # verify whether user win the game or not.
        self.correct_answer = deepcopy(list)

        # Store the correct answer in the form of
        # EX. ["./slider_puzzle_project_fall2021_assets-2022/Resources/Images/mario/16.gif, ......"]
        for i in range(len(self.correct_answer)):
            self.correct_answer[i] = Gameboard.root_path + \
                self.correct_answer[i]

        random.shuffle(list)  # shuffle the puzzle

        # Use the count variable to let turtle know when
        # is the timing going to next line to add tile.
        count = 0

        # Create a dictionary to let turtle know the number of
        # tiles in each line based on number of tiles.
        puzzle_num_dict = {16: 4, 9: 3, 4: 2}
        divisor = puzzle_num_dict.get(len(list))

        # Initialize the x,y coordinate for first tile to be added.
        x = -295
        y = 260

        # Draw the tiles
        for i in list:
            if "blank" in i:
                # Create a instance to keep track of blank
                set_position(x, y)
            if count % divisor == 0 and count != 0:
                y -= size + 2
                x -= (size + 2) * divisor
                if "blank" in i:
                    # create a instance to keep track of blank
                    set_position(x, y)
                astamp = self.draw_image((x, y), Gameboard.root_path + i)
            else:
                astamp = self.draw_image((x, y), Gameboard.root_path + i)
            # Create tile object
            lst.append(Tile(x, y, Gameboard.root_path + i, size, astamp))
            x += size + 2
            count += 1

        # Draw thumbnail
        self.draw_image(self.thumbnail, Gameboard.root_path + thumbnail)
        # Write leader board
        self.write_leader()
        # Updates current currrent_tile_list everytime draw the tiles on the Gameboard.
        self.currrent_tile_list = lst

    def draw_error(self, error_gif):
        """Whenever error occurs, turtle will show the error message

        Parameters
        ----------
        error_gif : GIF
            Error image
        """
        self.wds.addshape(Turtle.resource_path + error_gif)
        # set the turtle shape to shape with a given name
        self.err.shape(Turtle.resource_path + error_gif)
        astamp = self.err.stamp()
        self.wds.update()
        time.sleep(1.5)
        self.err.clearstamp(astamp)

    def draw_default_puzzle(self):
        """Draw the default tile"""
        list, size, thumbnail = self.puzzle_to_list(self.current_puzzle)
        self.draw_puzzle(list, size, thumbnail)

    def click_handler(self, x, y):
        """Based on the coordinate which user clicks, decides which event will be triggered.

        Parameters
        ----------
        x : int
            x coordinate that user clicked
        y : int
            y coordinate that user clicked
        """
        # Get the size of the tile
        size = self.currrent_tile_list[0].size
        # Range that will trigger quit function
        if 240 < x < 320 and -288.5 < y < -235.5:
            self.quit_click(x, y)
        # Range that will trigger reset function
        elif 40 < x < 120 and -302 < y < -222:
            self.reset_click(x, y)
        # Range that will trigger load function
        elif 140 < x < 220 and -300 < y < -224:
            self.load_click(x, y)
        # Range that will trigger tile click function
        elif (
            -295 - size / 2
            < x
            < -295
            + (len(self.currrent_tile_list) ** (1 / 2)) * (size + 2)
            - size / 2
            - (len(self.currrent_tile_list) ** (1 / 2)) * 2
            and 260
            - ((len(self.currrent_tile_list) ** (1 / 2)) - 1) * (size + 2)
            - size / 2
            - ((len(self.currrent_tile_list) ** (1 / 2)) - 1) * 2
            < y
            < 260 + size / 2
        ):
            self.tile_click(x, y)

    def quit_click(self, x, y):
        """Logic when clicking on the quit button.
        Quit the whole game.

        Parameters
        ----------
        x : int
            x coordinate within quit button
        y : int
            y coordinate within quit button
        """
        self.draw_image((0, 0), Gameboard.resource_path + "quitmsg.gif")
        self.wds.update()
        time.sleep(3)
        self.wds.bye()

    def load_click(self, x, y):
        """Logic when clicking on the load button.
        Load new puzzle to play

        Parameters
        ----------
        x : int
            x coordinate within load button
        y : int
            y coordinate within load button
        """
        # Get all available puzzles
        puz = "\n".join(self.get_available_puzzle())
        # Get next puzzle that user want to play
        new_puzzle = self.wds.textinput("Load Puzzle!", puz)
        list, size, thumbnail = self.puzzle_to_list(new_puzzle.strip(".puz"))

        # Clear previous puzzle
        self.ttl.clearstamps(-len(self.currrent_tile_list) - 1)
        # Clear player moves
        self.eraser.clear()
        # Reset click count = 0
        self.click_count = 0
        # Set current_puzzle = new_puzzle
        self.current_puzzle = new_puzzle.strip(".puz")

        # Draw new puzzle
        self.draw_puzzle(list, size, thumbnail)

    def reset_click(self, x, y):
        """Logic when clicking on the reset button.
        Reset the puzzle (cheat sheet for user)

        Parameters
        ----------
        x : int
            x coordinate within reset button
        y : int
            y coordinate within reset button
        """
        list, size, thumbnail = self.puzzle_to_list(self.current_puzzle)

        # create a empty list to store created tile object
        lst = []

        # Use the count variable to let turtle know when
        # is the timing going to next line to add tile.
        count = 0

        # Create a dictionary to let turtle know the number of
        # tiles in each line based on number of tiles.
        puzzle_num_dict = {16: 4, 9: 3, 4: 2}  # use the root
        divisor = puzzle_num_dict.get(len(list))

        # Initialize the x,y coordinate for first tile to be added.
        x = -295
        y = 260

        # Clear the shuffle tiles
        self.ttl.clearstamps(-len(self.currrent_tile_list) - 1)

        # Draw the tiles (unshuffle)
        for i in list:
            if "blank" in i:
                # create a instance to keep track of blank
                set_position(x, y)
            if count % divisor == 0 and count != 0:
                y -= size + 2
                x -= (size + 2) * divisor
                astamp = self.draw_image((x, y), Gameboard.root_path + i)
            else:
                astamp = self.draw_image((x, y), Gameboard.root_path + i)
            # Create a tile object
            lst.append(Tile(x, y, Gameboard.root_path + i, size, astamp))
            x += size + 2
            count += 1
        # Draw thumbnail
        self.draw_image(self.thumbnail, Gameboard.root_path + thumbnail)

        # Updates current currrent_tile_list everytime draw the tiles on the Gameboard.
        self.currrent_tile_list = lst

        # By rule, the game doesn't end even if user click reset button.
        # Thus, I use the boolean logic to prevent user from winning the game directly.
        # User can win the game only if self.is_reset == False.
        # Thus, after reset the puzzle, set is_reset = True. User need to swap the tile to turn
        # self.is_reset == False.
        self.is_reset = True

    def tile_click(self, x, y):
        """Logic when clicking on the tile.
        Also determine if user win or lose after each click.

        Parameters
        ----------
        x : int
            x coordinate within puzzle
        y : int
            y coordinate within puzzle
        """

        list = []  # store tiles adjacent to blank tile
        blank_list = []  # store blank tile

        # Get the blank tile x,y coordination
        blank_x = get_position_x()
        blank_y = get_position_y()

        # Find the tile that can be change
        for tile in self.currrent_tile_list:
            if (
                tile.coordinate_x + tile.size + 2 == blank_x
                or tile.coordinate_x - tile.size - 2 == blank_x
            ) and tile.coordinate_y == blank_y:
                list.append(tile)
            if (
                tile.coordinate_y + tile.size + 2 == blank_y
                or tile.coordinate_y - tile.size - 2 == blank_y
            ) and tile.coordinate_x == blank_x:
                list.append(tile)
            if "blank" in tile.image:
                blank_list.append(tile)

        # If click on the tile that can be changed, swap with the blank tile
        for adjacent_tile in list:
            if (
                adjacent_tile.coordinate_x - adjacent_tile.size / 2
                < x
                < adjacent_tile.coordinate_x + adjacent_tile.size / 2
                and adjacent_tile.coordinate_y - adjacent_tile.size / 2
                < y
                < adjacent_tile.coordinate_y + adjacent_tile.size / 2
            ):

                # Everytime user switch the tile with blank tile,
                # also switch both elements' index in current_tile_list, in order to
                # compare to correct answer to see if user solve the puzzle.
                swap_element_in_list(
                    self.currrent_tile_list, adjacent_tile, blank_list[0]
                )
                # Wwitch the tile
                adjacent_tile.switch(blank_list[0])
                # After using reset button, make user still need to swap the tile to win
                self.is_reset = False
                # Reset the blank tile x, y
                set_position(blank_list[0].coordinate_x,
                             blank_list[0].coordinate_y)

                # Clean the image of the tile and draw the new image
                self.ttl.clearstamp(adjacent_tile.astamp)
                self.ttl.clearstamp(blank_list[0].astamp)
                astamp = self.draw_image(
                    (adjacent_tile.coordinate_x, adjacent_tile.coordinate_y),
                    adjacent_tile.image,
                )
                adjacent_tile.astamp = astamp  # update the stamp ID
                bstamp = self.draw_image(
                    (blank_list[0].coordinate_x, blank_list[0].coordinate_y),
                    blank_list[0].image,
                )
                blank_list[0].astamp = bstamp  # update the stamp ID

                # If user swap tile, click +=1
                self.click_count += 1

        # Write the player move and keep update
        if self.click_count >= 1:
            self.eraser.clear()
            self.eraser.penup()
            self.eraser.setpos(-340, -275)
            self.eraser.pendown()
            self.eraser.write(
                f"Player move: {self.click_count}", font=("Calibri", 30, "bold")
            )

        # Win or Lose logic
        # Check if user lose logic after each click

        # Check if user lost first
        if self.click_count > int(self.play_times):
            self.lose()
        # Then check if user won
        for i in range(len(self.currrent_tile_list)):
            if self.currrent_tile_list[i].image == self.correct_answer[i]:
                if (
                    i == len(self.currrent_tile_list) - 1
                    and self.click_count <= int(self.play_times)
                    and not self.is_reset
                ):
                    # Put the winner in the leader file
                    with open("./leader.txt", "a", encoding="utf-8") as f:
                        f.write(
                            self.name
                            + " "
                            + str(self.click_count)
                            + " "
                            + self.current_puzzle
                            + "\n"
                        )
                    self.win()
                continue
            break

    def pregame(self, square_func, image_func):
        """Control turtle to implement the pregame layout

        Parameters
        ----------
        square_func : func
            Function to draw square
        image_func : func
            Function to draw button
        """
        # Draw splash screem
        self.splash_screen()
        # Get user information
        self.get_user_data()
        # Draw boxes
        square_func(self.puzzle)
        square_func(self.leader)
        square_func(self.control)
        # Draw button
        image_func(self.reset, Gameboard.resource_path + "resetbutton.gif")
        image_func(self.load, Gameboard.resource_path + "loadbutton.gif")
        image_func(self.quit, Gameboard.resource_path + "quitbutton.gif")

    def win(self):
        """Tell turtle show winning image"""
        self.draw_image((0, 0), Gameboard.resource_path + "winner.gif")
        self.wds.update()
        time.sleep(3)
        self.wds.bye()

    def lose(self):
        """Tell turtle show losing image"""
        self.draw_image((0, 0), Gameboard.resource_path + "Lose.gif")
        self.wds.update()
        time.sleep(3)
        self.wds.bye()
