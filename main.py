""" main.py - runs a pygame based game """

import pygame

from enum import Enum

class Point:
    """An immutable cartesian point with x and y coordinates"""
    def __init__(self, x: int, y: int):
        self.__x: int = x
        self.__y: int = y

    @property
    def x(self) -> int:
        """Read only access to the x-coordinate"""
        return self.__x

    @property
    def y(self) -> int:
        """Read only access to the y-coordinate"""
        return self.__y

class Borders:
    """Defines borders for the pygame display"""
    def __init__(self, left: int, right: int, top: int, bottom: int):
        self.__left: int = left
        self.__right: int = right
        self.__top: int = top
        self.__bottom: int = bottom

    @property
    def left(self) -> int:
        """"Read only access to the left-border"""
        return self.__left

    @property
    def right(self) -> int:
        """"Read only access to the right-border"""
        return self.__right

    @property
    def top(self) -> int:
        """"Read only access to the top-border"""
        return self.__top

    @property
    def bottom(self) -> int:
        """"Read only access to the bottom-border"""
        return self.__bottom

ObjectType = Enum("ObjectType", ["PLAYER", "MONSTER", "COIN", "DOOR", "FLAMES", "ROPE", "FLOOR"])
class Object:
    """Represent a generic game object"""
    def __init__(self, type: ObjectType):
        self.__type: ObjectType = type
        self.__pos: Point = Point(0,0)
        self.__vel: Point = Point(0,0)
        self.__hitbox: Point = Point(0,0)

    @property
    def hitbox(self) -> Point:
        """"Read only access to the hitbox of the object"""
        return self.__hitbox

    @classmethod
    def hitbox(self, x: int, y: int) -> None:
        """"Update the hitbox"""
        self.__hitbox = Point(x,y)
    

    @property
    def type(self) -> ObjectType:
        """"Read only access to the type of the object"""
        return self.__type

    @property
    def pos(self) -> Point:
        return self.__pos

    def set_pos(self, x: int, y: int) -> None:
        self.__pos = Point(x,y)

    @property
    def vel(self) -> Point:
        return self.__vel

    def set_vel(self, x: int, y: int) -> None:
        self.__vel = Point(x,y)

    def move(self, borders) -> None:
        self.update_velocity(borders)

        x = min(borders.right-self.hitbox.x, max(borders.left, self.pos.x + self.vel.x))
        y = min(borders.bottom-self.hitbox.y, max(borders.top, self.pos.y + self.vel.y))

        self.set_pos(x, y)

    def update_velocity(self, borders) -> None:
        pass

class ImageObject(Object):
    """An image-object that is loaded by pygame"""
    def __init__(self, type: ObjectType):
        super().__init__(type)
        self.__image_file: str = self.__get_object_image()
        self.__image_object = pygame.image.load(self.__image_file)
        self.hitbox = Point(self.__image_object.get_width(), self.__image_object.get_height())
        
    def __get_object_image(self) -> str:
        """Get the matching image-file for the objects type"""
        match self.type:
            case ObjectType.PLAYER:
                return "robo.png"
            case ObjectType.MONSTER:
                return "hirvio.png"
            case ObjectType.COIN:
                return "kolikko.png"
            case ObjectType.DOOR:
                return "ovi.png"

    def render(self, display: any) -> None:
        display.blit(self.__image_object, (self.pos.x, self.pos.y))

class RenderedObject(Object):
    """An object that is rendered, instead of loaded"""
    def __init__(self, type: ObjectType):
        super().__init__(type)

class Player(ImageObject):
    """"Represent the player"""
    def __init__(self):
        super().__init__(ObjectType.PLAYER)

    def update_velocity(self, borders: Borders) -> None:
        if self.pos.y < borders.bottom - self.hitbox.y:
            self.set_vel(self.vel.x, self.vel.y + 1)
        else:
            self.set_vel(self.vel.x, 0)

class Game:
    """An instance of a pygame-based game"""
    def __init__(self, x: int, y: int):
        self.__borders = Borders(0, x, 0, y)
        self.__objects: list[Object] = []
        self.__display: any = None # to-do: find type of display
        self.__clock: any = pygame.time.Clock()

        self.init()

    @property
    def borders(self) -> Borders:
        """"Read only access to the borders of the game"""
        return self.__borders

    @property
    def objects(self) -> list[Object]:
        """"Read only access to the object-list"""
        return self.__objects

    @property
    def display(self) -> any:
        """"Read only access to the pygame display"""
        return self.__display

    @property
    def clock(self) -> any:
        """Read only access to the pygame clock"""
        return self.__clock


    def init_pygame(self) -> None:
        """Initialize pygame"""
        pygame.init()

        self.__display = pygame.display.set_mode(
            (self.borders.right, self.borders.bottom)
        )

    def __create_image_object(self, type: ObjectType, x: int, y: int) -> ImageObject:
        obj = ImageObject(type)
        obj.set_pos(x, y)

        self.__objects.append(obj)

    def __create_player(self, x: int, y: int) -> Player:
        player = Player()
        player.set_pos(x, y)

        self.__objects.append(player)

    def __spawn_objects(self):
        """Spawn all of the objects"""
        self.__create_player(20, self.borders.bottom-200)

    def init_game(self) -> None:
        """Initialize the game itself"""
        self.__spawn_objects()

    def init(self) -> None:
        """Initialize whole class"""
        self.init_pygame()
        self.init_game()

    def game_loop(self) -> None:
        """Run the game-loop"""
        while True:
            self.__handle_events()
            self.__render_frame()

    def __handle_events(self) -> None:
        """"Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def __move_objects(self) -> None:
        for obj in self.objects:
            obj.move(self.borders)

    def __render_objects(self) -> None:
        for obj in self.objects:
            obj.render(self.display)

    def __render_frame(self) -> None:
        """Render a single frame"""
        self.display.fill((15, 17, 20))

        self.__move_objects()
        self.__render_objects()

        pygame.display.flip()
        self.clock.tick(60)

def main():
    """Run the program"""
    game = Game(640, 480)
    game.game_loop()

main()