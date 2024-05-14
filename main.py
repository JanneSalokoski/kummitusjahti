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

class Collision:
    """Defines what collisions can happen"""
    def __init__(self):
        self.left: bool = False
        self.right: bool = False
        self.top: bool = False
        self.bottom: bool = False

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

ObjectType = Enum("ObjectType", ["PLAYER", "MONSTER", "COIN", "DOOR", "FLAMES", "ROPE", "WALL"])
class Object:
    """Represent a generic game object"""
    def __init__(self, type: ObjectType):
        self.__type: ObjectType = type
        self.__pos: Point = Point(0,0)
        self.__vel: Point = Point(0,0)
        self.__hitbox: Point = Point(0,0)

        self.collision: Collision = Collision()

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

        x = min(borders.right-20-self.hitbox.x, max(borders.left+20, self.pos.x + self.vel.x))
        y = min(borders.bottom-self.hitbox.y, self.pos.y - self.vel.y)

        new_x = x
        new_y = y

        if (self.collision.right and x > self.pos.x):
            new_x = self.pos.x
        if (self.collision.left and x < self.pos.x):
            new_x = self.pos.x
        if (self.collision.bottom and y > self.pos.y):
            new_y = self.pos.y
        if (self.collision.top and y < self.pos.y):
            new_y = self.pos.y

        self.set_pos(new_x,new_y)

    def update_velocity(self, borders) -> None:
        pass

    def check_collision(self, other) -> None:
        """See if we collide with other"""
        own_left_border = self.pos.x
        own_right_border = self.pos.x + self.hitbox.x
        own_top_border = self.pos.y
        own_bottom_border = self.pos.y + self.hitbox.y

        other_left_border = other.pos.x
        other_right_border = other.pos.x + other.hitbox.x
        other_top_border = other.pos.y
        other_bottom_border = other.pos.y + other.hitbox.y

        if (own_right_border >= other_left_border and
            own_left_border <= other_left_border and
            not (own_bottom_border < other_top_border or
            own_top_border > other_bottom_border)):
            self.collision.right = True

        if (own_left_border <= other_right_border and
            own_right_border >= other_right_border and
            not (own_bottom_border < other_top_border or
            own_top_border > other_bottom_border)):
            self.collision.left = True

        if (own_bottom_border >= other_top_border and
            own_bottom_border <= other_bottom_border and
            not (own_right_border < other_left_border or
            own_left_border > other_right_border)):
            self.collision.bottom = True

        if (own_top_border <= other_bottom_border and
            own_top_border >= other_top_border and
            not (own_right_border < other_left_border or
            own_left_border > other_right_border)):
            self.collision.top = True

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

class Wall(RenderedObject):
    """A wall object"""
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(ObjectType.WALL)
        self.set_pos(x, y)
        self.hitbox = Point(width, height)

    def render(self, display: any) -> None:
        pygame.draw.rect(display, (255,0,0), (self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))

class Player(ImageObject):
    """"Represent the player"""
    def __init__(self):
        super().__init__(ObjectType.PLAYER)

    def update_velocity(self, borders: Borders) -> None:
        if self.vel.y < 0:
            self.set_vel(self.vel.x, self.vel.y + 1)
        elif self.vel.y > 0:
            self.set_vel(self.vel.x, self.vel.y - 1)

        if self.vel.x > 0:
            self.set_vel(self.vel.x - 1, self.vel.y)
        elif self.vel.x < 0:
            self.set_vel(self.vel.x + 1, self.vel.y)

        if not self.collision.bottom:
            self.set_vel(self.vel.x, self.vel.y - 2)

class Monster(ImageObject):
    """"Represent the monster"""
    def __init__(self):
        super().__init__(ObjectType.MONSTER)
        self.set_vel(1, 0)

    def update_velocity(self, borders) -> None:
        if self.collision.left:
            self.set_vel(1, 0)
        elif self.collision.right:
            self.set_vel(-1, 0)

    def move(self, borders) -> None:
        x = min(borders.right-20-self.hitbox.x, max(borders.left+20, self.pos.x + self.vel.x))
        y = min(borders.bottom-self.hitbox.y, self.pos.y - self.vel.y)

        self.set_pos(x,y)

        

class Game:
    """An instance of a pygame-based game"""
    def __init__(self, x: int, y: int):
        self.__borders = Borders(0, x, 0, y)
        self.__objects: list[Object] = []
        self.__display: any = None # to-do: find type of display
        self.__clock: any = pygame.time.Clock()
        self.__keys: set[str] = set()

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

    def __create_monster(self, x: int, y: int) -> Monster:
        monster = Monster()
        monster.set_pos(x, y)

        self.__objects.append(monster)

    def __create_wall(self, x: int, y: int, width: int, height: int) -> Wall:
        wall = Wall(x, y, width, height)
        self.__objects.append(wall)

    def __spawn_objects(self):
        """Spawn all of the objects"""
        # self.__create_wall(self.borders.left, self.borders.bottom, self.borders.right, 10)
        self.__create_player(20, self.borders.bottom-200)

        self.__create_wall(self.borders.left, 450, self.borders.right, 50)
        self.__create_wall(100, 400, 50, 50)
        self.__create_wall(400, 400, 50, 50)

        self.__create_wall(0, 200, 100, 50)
        self.__create_wall(350, 200, 450, 50)

        self.__create_wall(200, 250, 50, 50)

        self.__create_wall(400, 150, 50, 50)
        self.__create_wall(750, 150, 50, 50)

        self.__create_monster(300, 380)
        self.__create_monster(650, 130)
        self.__create_monster(450, 130)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.__keys.add("LEFT")
                if event.key == pygame.K_RIGHT:
                    self.__keys.add("RIGHT")
                if event.key == pygame.K_UP:
                    self.__keys.add("UP")
                if event.key == pygame.K_DOWN:
                    self.__keys.add("DOWN")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.__keys.remove("LEFT")
                if event.key == pygame.K_RIGHT:
                    self.__keys.remove("RIGHT")
                if event.key == pygame.K_UP:
                    self.__keys.remove("UP")
                if event.key == pygame.K_DOWN:
                    self.__keys.remove("DOWN")

            if event.type == pygame.QUIT:
                exit()

    def __update_velocities(self) -> None:
        for obj in self.objects:
            if obj.type == ObjectType.PLAYER:
                if "UP" in self.__keys and obj.collision.bottom:
                    obj.set_vel(obj.vel.x, 30)
                if "LEFT" in self.__keys:
                    obj.set_vel(-8, obj.vel.y)
                if "RIGHT" in self.__keys:
                    obj.set_vel(8, obj.vel.y)

            if obj.type == ObjectType.MONSTER:
                obj.update_velocity(self.borders)


    def __move_objects(self) -> None:
        for obj in self.objects:
            if obj.type == ObjectType.PLAYER or obj.type == ObjectType.MONSTER:
                obj.move(self.borders)

    def __check_collisions(self) -> None:
        player = self.objects[0]
        player.collision = Collision()
        for obj in self.objects[1:]:
            obj.collision = Collision()
            player.check_collision(obj)
            if obj.type == ObjectType.MONSTER:
                for o2 in self.__objects:
                    if obj != o2:
                        obj.check_collision(o2)

    def __render_objects(self) -> None:
        for obj in self.objects:
            obj.render(self.display)

    def __render_gridlines(self):
        for i in range(20):
            pygame.draw.line(self.display, (0,0,255), (i*50,self.borders.top), (i*50,self.borders.bottom))

        for i in range(20):
            pygame.draw.line(self.display, (0,0,255), (self.borders.left, i*50), (self.borders.right, i*50))


    def __render_frame(self) -> None:
        """Render a single frame"""
        self.display.fill((15, 17, 20))

        self.__update_velocities()
        self.__check_collisions()
        self.__move_objects()
        self.__render_objects()
        self.__render_gridlines()

        pygame.display.flip()
        self.clock.tick(60)

def main():
    """Run the program"""
    game = Game(800, 500)
    game.game_loop()

main()