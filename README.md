# Puzzle Slider Game

Puzzle Slider Game is a combination puzzle where a player must slide pieces vertically or horizontally on a board to establish an end result that matches a solution. In this project, you can create your own 3X3 puzzle or 4X4 puzzle!

## Prerequisites
- Python >= 3.11.0

## Installation

Use the package manager pip3 to install Pillow.

```bash
pip3 install Pillow
```

## Getting Started
There are some default puzzles, to start the puzzle game, execute:

```bash
python3 puzzle_game.py
```
You can move the tile and click the function button by mouse, have fun!
<img src="https://i.imgur.com/tTZsYSs.jpg" alt="drawing" width="500"/>

## Play on your own puzzle
If you wish you can create your own puzzles by downloading image file(jpeg, jpg or png) to
slide_puzzle folder.
<img src="https://i.imgur.com/9EQExuD.png" alt="drawing" width="500"/>


Run the custom_puzzle_setup.py on terminal to make the custom puzzle!
```bash
% python3 custom_puzzle_setup.py
```
Follow the instruction typing the image file name then the size of the puzzle you want.
```
What is your image's name?
Ex. mario.jpg
:southpark.png
What kind of puzzle do you want?
Ex. 3 as (3*3 puzzle) or 4 as (4*4 puzzle)
:4
Resized the image!
Dicerctory southpark created!
Tiles created!
.puz file created!
Delete image!
```


Now, if you execute the puzzle and click "load button", you can play your custom puzzle!
```bash
python3 puzzle_game.py
```
<img src="https://i.imgur.com/rGAFhKQ.jpg" alt="drawing" width="500"/>
<img src="https://i.imgur.com/Mp1Iiq5.jpg" alt="drawing" width="500"/>


## License

[MIT](https://choosealicense.com/licenses/mit/)
