import curses
import math
import logic.constants as const

class LineGuide:
    def __init__(self, stdscr, x, y, lines = 1):
        self.stdscr = stdscr
        self.x, self.y, self.lines= x, y, lines

        self.left_margin = const.LINES_NUMBER_MARGIN_LEFT
        self.right_margin = const.LINES_NUMBER_MARGIN_RIGHT

        self.max_width = self.calc_max_width()

    def calc_max_width(self):
        return len(str(self.lines))

    def calc_margin(self):
        return self.left_margin + self.max_width + self.right_margin

    def update(self, lines):
        self.lines = lines
        self.display(self.y)

    def display(self, curr_line):
        for k in range(self.lines):
            line_num = str(k + 1)
            formatted_number = line_num.rjust(self.left_margin + self.max_width) + ' ' * self.right_margin
            if k == curr_line:
                self.stdscr.addstr(k, 0, formatted_number)
            else:
                self.stdscr.addstr(k, 0, formatted_number, curses.A_DIM)
        self.stdscr.refresh()
