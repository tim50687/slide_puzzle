class Tile:
    """Store each tile's information"""

    def __init__(
        self,
        coordinate_x=0,
        coordinate_y=0,
        image="",
        size=0,
        astamp=0,
    ):
        """Inits the Tile object.

        Parameters
        ----------
        coordinate_x : int
            x coordinate of tile, by default 0
        coordinate_y : int
            y coordinate of tile, by default 0
        image : str
            Relative path of the tile, by default ""
        size : int
            Size of the tile, by default 0
        astamp : int
            Stamp ID of the tile, by default 0
        """

        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.image = image
        self.size = size
        self.astamp = astamp

    def switch(self, other):
        """Switch two tiles' x and y coordinate.

        Parameters
        ----------
        other : Tile
            Another tile object
        """
        temp_coordinate_x = self.coordinate_x
        self.coordinate_x = other.coordinate_x
        other.coordinate_x = temp_coordinate_x

        temp_coordinate_y = self.coordinate_y
        self.coordinate_y = other.coordinate_y
        other.coordinate_y = temp_coordinate_y
