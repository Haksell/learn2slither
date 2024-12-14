import pyglet

_MAX_TILE_SIZE = 125
_MAX_SCREEN_PROPORTION = 0.7
_TILE_PADDING = 0.03

_BAD_APPLE_COLOR = (255, 96, 96)
_GOOD_APPLE_COLOR = (96, 255, 96)
_SNAKE_COLOR = (96, 96, 255)
_BACKGROUND_COLOR = (50, 50, 50)


class Game(pyglet.window.Window):
    def __init__(self, *, width=10, height=10):
        self.__width = width
        self.__height = height
        self.__tile_size = self.__compute_tile_size()
        self.__padding = round(_TILE_PADDING * self.__tile_size)
        super().__init__(
            width=self.__tile_size * width + 2 * self.__padding,
            height=self.__tile_size * height + 2 * self.__padding,
            caption="learn2slither",
        )
        self.__batch = self.__make_batch()
        self.__keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.__keys)

    def __compute_tile_size(self):
        screen = pyglet.canvas.get_display().get_default_screen()
        h = screen.height / self.__height
        w = screen.width / self.__width
        return min(_MAX_TILE_SIZE, int(min(h, w) * _MAX_SCREEN_PROPORTION))

    def __make_batch(self):
        batch = pyglet.graphics.Batch()
        visible_tile_size = (1 - 2 * _TILE_PADDING) * self.__tile_size
        for y in range(self.__height):
            for x in range(self.__width):
                color = [
                    [_SNAKE_COLOR, _BACKGROUND_COLOR][x & 1],
                    [_GOOD_APPLE_COLOR, _BAD_APPLE_COLOR][x & 1],
                ][y & 1]
                pyglet.shapes.Rectangle(
                    x * self.__tile_size + 2 * self.__padding,
                    self.height - (y * self.__tile_size + self.__tile_size),
                    visible_tile_size,
                    visible_tile_size,
                    color=color,
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
    for i in range(1, 31):
        Game(width=i, height=i).run()


if __name__ == "__main__":
    __main()
