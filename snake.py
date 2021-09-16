from a_star import GraphNode, a_star
import config
from dataclasses import dataclass
import numpy as np
import random


def check_other_type(f):
    def wrapper(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("You can only add Coord to Coord.")

        return f(self, other)

    return wrapper


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    @check_other_type
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    @check_other_type
    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    @check_other_type
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @check_other_type
    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    # needed for priority queue
    @check_other_type
    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    @check_other_type
    def distance(self, other: "Coord"):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Direction:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Tiles:
    EMPTY = 0
    BORDER = 1
    SNAKE = 2
    PREY = 3


# MAIN CLASS
class SnakeGame:
    def __init__(self, height: int, width: int):
        if height < config.MIN_BOARD_HEIGHT or width < config.MIN_BOARD_WIDTH:
            raise ValueError(
                f"Size of the game board must be at least {config.MIN_BOARD_HEIGHT}x{config.MIN_BOARD_WIDTH}."
            )

        board = np.empty((height, width), np.short)

        # fill in borders
        board[:, 0].fill(Tiles.BORDER)
        board[:, -1].fill(Tiles.BORDER)
        board[0, :].fill(Tiles.BORDER)
        board[-1, :].fill(Tiles.BORDER)

        # snake start (horizontally)
        snake_height = (width - 1) // 2
        snake_width = (
            width - config.START_SNAKE_SIZE
        ) // 2 + config.START_SNAKE_SIZE  # X coord of snake head
        self.snake = [
            Coord(i, snake_height)
            for i in range(snake_width, snake_width - config.START_SNAKE_SIZE, -1)
        ]

        # random prey location
        while True:
            x = random.randrange(1, width - 1)
            y = random.randrange(1, height - 1)

            if x not in (snake_width, snake_width - 1, snake_width + 1,) and y not in (
                snake_height,
                snake_height - 1,
                snake_height + 1,
            ):
                self.prey = Coord(x, y)
                break

        self.board = board
        self._update_board()
        self.prey_moved = True

    def _clear_board(self):
        self.board[1:-1, 1:-1].fill(Tiles.EMPTY)

    def _update_board(self):
        self._clear_board()

        for snake_coord in self.snake:
            self.board[snake_coord.y][snake_coord.x] = Tiles.SNAKE

        self.board[self.prey.y][self.prey.x] = Tiles.PREY

    def _calculate_next_move(self):
        graph = {}
        start_point = self.snake[0]
        end_point = self.prey

        # create graph
        for row_idx, row in enumerate(self.board[1:-1, 1:-1], start=1):
            for col_idx, tile in enumerate(row, start=1):
                # ignore snake and prey tiles
                if tile != Tiles.SNAKE or (
                    col_idx == start_point.x and row_idx == start_point.y
                ):
                    neighbors = {}
                    for neigh in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                        x = col_idx + neigh[0]
                        y = row_idx + neigh[1]

                        if self.board[y, x] not in (Tiles.SNAKE, Tiles.BORDER):
                            neighbors[Coord(x, y)] = 1

                    coord = Coord(col_idx, row_idx)
                    node = GraphNode(coord, neighbors, end_point.distance(coord))
                    graph[coord] = node

        self.path = a_star(graph, start_point, end_point)[1:]

    def get_snake_head(self) -> Coord:
        return self.snake[0]

    def enlarge_snake(self) -> None:
        # check what is the direction of last block
        # add on the opposite direction
        next_to_last = self.snake[-2]

        dir_dict = {
            next_to_last + Coord(0, 1): Coord(0, -1),
            next_to_last + Coord(0, -1): Coord(0, 1),
            next_to_last + Coord(1, 0): Coord(1, 0),
            next_to_last + Coord(-1, 0): Coord(-1, 0),
        }

        last = self.snake[-1]
        to_add = dir_dict[last]
        new_coord = last + to_add

        # check if new spot isn't border, prey...
        if self.board[new_coord.y][new_coord.x] != Tiles.EMPTY:
            to_choose = list(set(dir_dict.values()) - {to_add, -to_add})

            # if can't enlarge, don't do anything
            if not to_choose:
                return

            new_coord = last + random.choice(to_choose)

        self.snake.append(new_coord)

        self._update_board()

    def move_prey(self, direction: Direction) -> bool:
        # return True if game ended
        dir_dict = {
            Direction.UP: Coord(0, -1),
            Direction.DOWN: Coord(0, 1),
            Direction.LEFT: Coord(-1, 0),
            Direction.RIGHT: Coord(1, 0),
        }
        to_add = dir_dict[direction]

        new_prey = self.prey + to_add

        # if any tile to move is occupied, do nothing
        if self.board[new_prey.y][new_prey.x] == Tiles.SNAKE:
            return True
        elif self.board[new_prey.y][new_prey.x] != Tiles.EMPTY:
            return False

        self.prey = new_prey
        self._update_board()
        self.prey_moved = True
        return False

    def move_snake(self) -> bool:
        # returns if game ended or not

        # calculate where to go
        # don't recalculate if prey hasn't moved
        if self.prey_moved:
            self._calculate_next_move()

        next_move = self.path[0]

        if next_move == self.prey:
            return True

        self.snake = [next_move] + self.snake[:-1]

        self._update_board()
        return False
