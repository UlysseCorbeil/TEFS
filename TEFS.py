from components.window import Window
import curses

# Text Editor For Shenanigans
class TEFS():

    def start(stdscr):
        Window(stdscr)

    curses.wrapper(start)
