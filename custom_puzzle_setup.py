import os
from itertools import product
from PIL import Image
import re


def create_folder(dir):
    """Create a directory for the puzzle's gif

    Parameters
    ----------
    dir : string
        Name of the dircetory
    """
    os.mkdir(f"./Images/{dir}")
    print(f"Dicerctory {dir} created!")


def resize_image(name, nums_of_tiles):
    """Resize the image to (nums_of_tiles * 100) * (nums_of_tiles * 100)
    """

    # Opens a image in RGB mode
    image = Image.open(rf"./{name}")
    image = image.resize((nums_of_tiles * 100, nums_of_tiles * 100))
    image.save(f"./{name}")
    print("Resized the image!")


def create_tile(name, dir_name, nums_of_tiles):
    """Create tile for the game.

    Parameters
    ----------
    name : string
        Name of the image
    dir_name : string 
        Puzzle's image name
    nums_of_tiles : integer
        Form of puzzle that user want to play
    """
    image = Image.open(rf"./{name}")
    count = nums_of_tiles ** 2
    w, h = image.size
    grid = product(range(0, w-w % nums_of_tiles, w // nums_of_tiles),
                   range(0, h-h % nums_of_tiles, h // nums_of_tiles))
    for i, j in grid:
        box = (j, i, j + h // nums_of_tiles, i + w // nums_of_tiles)
        image.crop(box).save(f"./Images/{dir_name}/{count}.gif")
        count -= 1

    def add_blank_tile():
        """Remove last tile with blank tile
        """
        blank = Image.open(rf"./blank_sample.gif")
        blank = blank.resize((w // nums_of_tiles, h // nums_of_tiles))
        blank.save(f"./Images/{dir_name}/blank.gif")

    def create_thumbnail():
        """Create thumbnail image
        """
        image = Image.open(name)
        image = image.resize((w // nums_of_tiles, h // nums_of_tiles))
        image.save(f"./Images/{dir_name}/{dir_name}_thumbnail.gif")

    def create_puz_file():
        """Create .puz file in root directory
        """
        with open(f"./{dir_name}.puz", "w", encoding="utf-8") as f:
            f.write(f"name: {dir_name}\n")
            f.write(f"number: {nums_of_tiles ** 2}\n")
            f.write(f"size: {w // nums_of_tiles}\n")
            f.write(
                f"thumbnail: /Images/{dir_name}/{dir_name}_thumbnail.gif\n")
            c = 1
            for i in range(nums_of_tiles ** 2, 0, -1):
                if i == 1:
                    f.write(f"{c}: /Images/{dir_name}/blank.gif\n")
                else:
                    f.write(f"{c}: /Images/{dir_name}/{i}.gif\n")
                c += 1

    add_blank_tile()
    create_thumbnail()
    print("Tiles created!")
    create_puz_file()
    print(".puz file created!")


def remove_image(name):
    """Remove download image

    Parameters
    ----------
    name : string
        Name of image
    """
    os.remove(f"./{name}")
    print("Delete image!")


def main():
    name = str(input("What is your image's name?\nEx. mario.jpg\n:"))
    nums_of_tiles = int(input(
        "What kind of puzzle do you want?\nEx. 3 as (3*3 puzzle) or 4 as (4*4 puzzle)\n:"))
    dir_name = re.sub("\..+", "", name)
    resize_image(name, nums_of_tiles)
    create_folder(dir_name)
    create_tile(name, dir_name, nums_of_tiles)
    remove_image(name)


if __name__ == "__main__":
    main()
