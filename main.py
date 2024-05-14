""" main.py - runs a pygame based game """

import pygame

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

class Object:
    """Represent a generic game object"""
    def __init__(self):
        pass

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

    def init_game(self) -> None:
        """Initialize the game itself"""
        pass

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

    def __render_frame(self) -> None:
        """Render a single frame"""
        self.display.fill((15, 17, 20))

        pygame.display.flip()
        self.clock.tick(60)

def main():
    """Run the program"""
    game = Game(640, 480)
    game.game_loop()

main()