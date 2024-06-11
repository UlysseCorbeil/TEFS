import curses
from logic.handler import Handler
import logic.constants as const

class Window:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.x, self.y = 0, 0
        self.handler = Handler(self.stdscr, self.x, self.y)
        self.c_initialize()

    def c_initialize(self):

        # Clear screen and start from the top-left corner
        self.stdscr.clear()

        # Turn on echoing of characters
        curses.echo()

        # Make the cursor visible
        curses.curs_set(1)

        self.handler.handle_window()
