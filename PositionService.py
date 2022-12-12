class PositionService:
    """Track black tile"""

    blank_tile_instance = None

    def __init__(self):
        self.x = 0
        self.y = 0

    def __str__(self):
        return f"x: {self.x} y: {self.y}"

    @classmethod
    def get_instance(cls):
        if cls.blank_tile_instance is None:
            cls.blank_tile_instance = PositionService()
        return cls.blank_tile_instance


def set_position(x, y):
    instance = PositionService.get_instance()
    instance.x, instance.y = x, y


def get_position_x():
    instance = PositionService.get_instance()
    return instance.x


def get_position_y():
    instance = PositionService.get_instance()
    return instance.y
