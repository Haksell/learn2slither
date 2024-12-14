import itertools
import pyglet

_MAX_TILE_SIZE = 125
_MAX_SCREEN_PROPORTION = 0.7
_TILE_PADDING = 0.03
_COLOR_CORRECT = (232, 138, 69)
_COLOR_INCORRECT = (106, 198, 184)


def _make_goal(height, width):
    length = width * height
    tiles = [-1] * length
    x = y = 0
    dx = 1
    dy = 0
    for cur in itertools.chain(range(1, length), [0]):
        tiles[x + y * width] = cur
        cur += 1
        if (
            x + dx >= width
            or x + dx < 0
            or y + dy >= height
            or y + dy < 0
            or tiles[x + dx + (y + dy) * width] != -1
        ):
            dx, dy = -dy, dx
        x += dx
        y += dy
    return tiles


class Puzzle:
    def __init__(self, tiles, height, width, *, goal=None):
        self.__height = height
        self.__width = width
        self.__tiles = tiles
        self.update_goal(goal or _make_goal(height, width))
        self.minx = self.miny = 0
        self.maxx = width - 1
        self.maxy = height - 1

    def __len__(self):
        return len(self.__tiles)

    def __iter__(self):
        yield from self.__tiles

    def __getitem__(self, idx):
        return self.__tiles[idx]

    def __str__(self):
        return "\n".join(
            " ".join(
                f"{self[y*self.__width+x]:{self.padding}}" for x in range(self.__width)
            )
            for y in range(self.__height)
        )

    @property
    def padding(self):
        return len(str(len(self) - 1))

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def goal(self):
        return self.__goal

    def is_correct(self, i):
        return self[i] == self.__goal[i]

    def update_goal(self, goal):
        self.__goal = goal


class Game(pyglet.window.Window):
    def __init__(self, puzzle):
        self.__puzzle = puzzle
        self.__tile_size = self.__compute_tile_size()
        self.__padding = round(_TILE_PADDING * self.__tile_size)
        super().__init__(
            width=self.__tile_size * puzzle.width + 2 * self.__padding,
            height=self.__tile_size * puzzle.height + 2 * self.__padding,
            caption="learn2slither",
        )
        self.__batch = self.__make_batch()
        self.__keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.__keys)

    def __compute_tile_size(self):
        screen = pyglet.canvas.get_display().get_default_screen()
        h = screen.height / self.__puzzle.height
        w = screen.width / self.__puzzle.width
        return min(_MAX_TILE_SIZE, int(min(h, w) * _MAX_SCREEN_PROPORTION))

    def __make_batch(self):
        batch = pyglet.graphics.Batch()
        visible_tile_size = (1 - 2 * _TILE_PADDING) * self.__tile_size
        for i, number in enumerate(self.__puzzle):
            if number == 0:
                continue
            y, x = divmod(i, self.__puzzle.width)
            pyglet.shapes.Rectangle(
                x * self.__tile_size + 2 * self.__padding,
                self.height - (y * self.__tile_size + self.__tile_size),
                visible_tile_size,
                visible_tile_size,
                color=_COLOR_CORRECT
                if self.__puzzle.is_correct(i)
                else _COLOR_INCORRECT,
                batch=batch,
            )
        return batch

    def on_draw(self):
        for k in [
            pyglet.window.key.UP,
            pyglet.window.key.RIGHT,
            pyglet.window.key.DOWN,
            pyglet.window.key.LEFT,
        ]:
            if self.__keys[k]:
                print(k)
        pyglet.gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        self.clear()
        self.__batch.draw()

    def run(self):
        pyglet.app.run()


def __main():
    puzzle = Puzzle([1, 2, 3, 4, 5, 6, 7, 8, 0], 3, 3)
    Game(puzzle).run()


if __name__ == "__main__":
    __main()
