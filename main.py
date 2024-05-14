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
        """"Access to the position of the object"""
        return self.__pos

    def set_pos(self, x: int, y: int) -> None:
        """Modify the position"""
        self.__pos = Point(x,y)

    @property
    def vel(self) -> Point:
        """Access the velocity"""
        return self.__vel

    def set_vel(self, x: int, y: int) -> None:
        """Modify the velocity"""
        self.__vel = Point(x,y)

    def move(self, borders) -> None:
        """Handle the basic movement pattern of an object"""
        self.update_velocity(borders)

        # Make sure we are not going over the playing area
        x = min(borders.right-20-self.hitbox.x, max(borders.left+20, self.pos.x + self.vel.x))
        y = min(borders.bottom-self.hitbox.y, self.pos.y - self.vel.y)

        new_x = x
        new_y = y

        # We can't pass through other objects either
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
        """Placeholder for a subclass implementation"""
        pass

    def handle_coin_collision(self, coin, trash):
        """Placeholder for a subclass implementation"""
        pass

    def handle_monster_collision(self, monster, trash):
        """Placeholder for a subclass implementation"""
        pass

    def check_collision(self, other, trash) -> None:
        """See if we collide with other"""

        # This really should be cleaned up a little...
        # We are repeating a lot of code that could
        # be replaced by arrays and clever functions
        # and it's wierd to handle coins and monsters here

        # calculate borders of self
        own_left_border = self.pos.x
        own_right_border = self.pos.x + self.hitbox.x
        own_top_border = self.pos.y
        own_bottom_border = self.pos.y + self.hitbox.y

        # calculate borders of other
        other_left_border = other.pos.x
        other_right_border = other.pos.x + other.hitbox.x
        other_top_border = other.pos.y
        other_bottom_border = other.pos.y + other.hitbox.y

        # check right border
        if (own_right_border >= other_left_border and
            own_left_border <= other_left_border and
            not (own_bottom_border < other_top_border or
            own_top_border > other_bottom_border)):
            self.collision.right = True
            if other.type == ObjectType.COIN:
                self.handle_coin_collision(other, trash)
            if other.type == ObjectType.MONSTER:
                self.handle_monster_collision(other, trash)

        # check left border
        if (own_left_border <= other_right_border and
            own_right_border >= other_right_border and
            not (own_bottom_border < other_top_border or
            own_top_border > other_bottom_border)):
            self.collision.left = True
            if other.type == ObjectType.COIN:
                self.handle_coin_collision(other, trash)
            
            if other.type == ObjectType.MONSTER:
                self.handle_monster_collision(other, trash)

        # check bottom border
        if (own_bottom_border >= other_top_border and
            own_bottom_border <= other_bottom_border and
            not (own_right_border < other_left_border or
            own_left_border > other_right_border)):
            self.collision.bottom = True
            if other.type == ObjectType.COIN:
                self.handle_coin_collision(other, trash)

        # check top border
        if (own_top_border <= other_bottom_border and
            own_top_border >= other_top_border and
            not (own_right_border < other_left_border or
            own_left_border > other_right_border)):
            self.collision.top = True
            if other.type == ObjectType.COIN:
                self.handle_coin_collision(other, trash)

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
        """Render the object image to the screen"""
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
        """Draw the shape of the object on the screen"""
        pygame.draw.rect(display, (255,0,0), (self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))

class Player(ImageObject):
    """"Represent the player"""
    def __init__(self):
        super().__init__(ObjectType.PLAYER)

    def update_velocity(self, borders: Borders) -> None:
        """Update players velocity each frame"""
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

    def handle_coin_collision(self, coin, trash):
        """Handle when we hit a coin"""
        trash.add(coin)

    def handle_monster_collision(self, monster, trash):
        """Handle when we hit a monster"""
        trash.add(monster)

class Coin(ImageObject):
    """Represent a coin"""
    def __init__(self):
        super().__init__(ObjectType.COIN)

    def update_velocity(self, borders) -> None:
        pass # This is just to override the default implementation

    def move(self, borders) -> None:
        pass # This is just to override the default implementation

class Monster(ImageObject):
    """"Represent the monster"""
    def __init__(self):
        super().__init__(ObjectType.MONSTER)
        self.set_vel(1, 0)

    def update_velocity(self, borders) -> None:
        """Update velocities of monsters on each frame"""
        if self.collision.left:
            self.set_vel(1, 0)
        elif self.collision.right:
            self.set_vel(-1, 0)

    def move(self, borders) -> None:
        """Move the monster according to it's velocity"""
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
        self.__trash: set[Object] = set()

        self.player_health = 2
        self.coins_collected = 0

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

    def __create_player(self, x: int, y: int) -> Player:
        """Create a new player object"""
        player = Player()
        player.set_pos(x, y)

        self.__objects.append(player)
        return player

    def __create_monster(self, x: int, y: int) -> Monster:
        """Create a new monster object"""
        monster = Monster()
        monster.set_pos(x, y)

        self.__objects.append(monster)
        return monster

    def __create_coin(self, x: int, y: int) -> Coin:
        """Create a new coin object"""
        coin = Coin()
        coin.set_pos(x, y)

        self.__objects.append(coin)
        return coin

    def __create_wall(self, x: int, y: int, width: int, height: int) -> Wall:
        """Create a new wall-object"""
        wall = Wall(x, y, width, height)
        self.__objects.append(wall)
        return wall

    def __spawn_objects(self):
        """Spawn all of the objects"""

        self.__create_player(20, self.borders.bottom-200)

        wall_positions = [(0,450,800,50), (100,400,50,50), (400,400,50,50), (0,200,100,50),
                          (350,200,450,50), (200, 250, 50, 50), (400,150,50,50), (750,150,50,50)]
        for p in wall_positions:
            self.__create_wall(p[0], p[1], p[2], p[3])

        monster_positions = [(300,380), (650,130), (450,130)]
        for m in monster_positions:
            self.__create_monster(m[0], m[1])

        coin_positions = [(0,0), (4,4), (15,2), (8,7), (13,8)]
        for c in coin_positions:
            self.__create_coin(c[0]*50, c[1]*50)

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
            if self.coins_collected == 5:
                # Handle winning the game
                font = pygame.font.SysFont("monospace", 30)
                text = font.render("YOU WON!", True, (255,255,255))
                self.display.fill((0,0,0))
                self.display.blit(text, (300,230))
                pygame.display.flip()

            elif self.player_health > 0: 
                # Handle normal game
                self.__render_frame()

            elif self.player_health == 0:
                # Handle losing the game
                font = pygame.font.SysFont("monospace", 30)
                self.display.fill((0,0,0))
                text = font.render("GAME OVER!", True, (255,0,0))
                self.display.blit(text, (300,230))
                pygame.display.flip()

            self.__handle_events()

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
        """Update velocities of players and monsters"""
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
        """Move all objects according to their velocities"""
        for obj in self.objects:
            if obj.type == ObjectType.PLAYER or obj.type == ObjectType.MONSTER:
                obj.move(self.borders)

    def __check_collisions(self) -> None:
        """Check for any collisions between objects"""
        player = self.objects[0]
        player.collision = Collision()
        for obj in self.objects[1:]:
            obj.collision = Collision()
            player.check_collision(obj, self.__trash)
            if obj.type == ObjectType.MONSTER:
                for o2 in self.__objects:
                    if obj != o2:
                        obj.check_collision(o2, self.__trash)

    def __render_objects(self) -> None:
        """Render all objects on the screen"""
        for obj in self.objects:
            obj.render(self.display)

    def __render_texts(self) -> None:
        """Render some stats"""
        font = pygame.font.SysFont("monospace", 20)
        health = font.render(f"health: {(self.player_health/2)*100:.0f}%", True, (255,255,255))
        coins = font.render(f"coins: {self.coins_collected}/5", True, (255,255,255))

        self.display.blit(health, (self.borders.right - health.get_width() - 10,10))
        self.display.blit(coins, (self.borders.right - coins.get_width() - 10,30))

    def __render_gridlines(self):
        """Render gridlines to help with counting pixels"""
        for i in range(20):
            pygame.draw.line(self.display, (0,0,255), (i*50,self.borders.top), (i*50,self.borders.bottom))

        for i in range(20):
            pygame.draw.line(self.display, (0,0,255), (self.borders.left, i*50), (self.borders.right, i*50))

    def __clean_trash(self):
        """Remove items from the trashbin"""
        for item in self.__trash:
            # To-do: remove these from here, it's odd to set them here
            if item.type == ObjectType.MONSTER:
                print("HIT A MONSTER")
                self.player_health -= 1;

            if item.type == ObjectType.COIN:
                self.coins_collected += 1;

            try: # This shouldn't also be necessary?
                self.__objects.remove(item)
            except Exception:
                pass

        self.__trash.clear()

    def __render_frame(self) -> None:
        """Render a single frame"""
        self.display.fill((15, 17, 20))

        self.__update_velocities()
        self.__check_collisions()
        self.__move_objects()
        self.__render_objects()
        # self.__render_gridlines()
        self.__render_texts()
        self.__clean_trash()

        pygame.display.flip()
        self.clock.tick(60)

def main():
    """Run the program"""
    game = Game(800, 500)
    game.game_loop()

main()