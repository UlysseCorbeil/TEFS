import curses
import signal
from components.line_guide import LineGuide
from logic.gap_buffer import GapBuffer
from logic.word_wrapper import WordWrapper

class Handler():

    def __init__(self, stdscr, x, y):
        self.stdscr = stdscr
        self.x, self.y = x, y
        self.lines = LineGuide(self.stdscr, self.x, self.y)
        self.gap_buffer = GapBuffer()
        self.word_wrapper = WordWrapper(self.stdscr)

    def handle_window(self):

        while True:
            self.stdscr.clear()
            self.lines.display(self.y)

            margin = self.lines.calc_margin()
            win_w = self.word_wrapper.get_window_width()
            raw_text = self.gap_buffer.get_text().split("\n")
            # lines_text = self.word_wrapper.wrap_text(raw_text, win_w, margin)

            for k, line in enumerate(raw_text):
                self.stdscr.addstr(k, margin, line)

            self.stdscr.move(self.y, self.x + margin)
            key = self.stdscr.getch()

            if key == ord('\n'):
               self.handle_next_char()
               self.update_lines()
            elif key == curses.KEY_BACKSPACE:
               self.handle_backspace()
            elif key == 27:
                break
            elif key == 26:
                self.handle_backspace()
            else:
                self.handle_forward(chr(key))

            self.stdscr.move(self.y, self.x)

            self.stdscr.refresh()

    # def handle_menu(self):
    #     # Basic implementation of menu interaction
    #     menu_options = ['Open File', 'Save File', 'Exit']
    #     current_option = 0

    #     while True:
    #         self.stdscr.clear()
    #         for i, option in enumerate(menu_options):
    #             mode = curses.A_REVERSE if i == current_option else curses.A_NORMAL
    #             self.stdscr.addstr(i, 0, option, mode)

    #         key = self.stdscr.getch()

    #         if key == curses.KEY_UP and current_option > 0:
    #             current_option -= 1
    #         elif key == curses.KEY_DOWN and current_option < len(menu_options) - 1:
    #             current_option += 1
    #         elif key == ord('\n'):  # Enter key to select
    #             if current_option == 0:  # Open File
    #                 self.open_file()
    #             elif current_option == 1:  # Save File
    #                 self.save_file()
    #             elif current_option == 2:  # Exit menu
    #                 break
    #         self.stdscr.refresh()

    def update_lines(self):
        self.lines.update(self.y + 1)

    def handle_forward(self, u_key):
        insert_position = self.gap_buffer.calc_insert_position(self.x, self.y)
        self.gap_buffer.insert(insert_position, u_key)
        self.x += 1

    def handle_next_char(self):
        # Insert a line break and move to the next line
        insert_position = self.gap_buffer.calc_insert_position(self.x, self.y)
        self.gap_buffer.insert(insert_position, '\n')
        self.y += 1
        self.x = 0

    def handle_backspace(self):

        # Allow backspace if not at the start of the document
        if self.x > 0 or self.y > 0:
            delete_position = self.gap_buffer.calc_insert_position(self.x, self.y)
            self.gap_buffer.delete(delete_position - 1)

            # Adjust cursor position
            if self.x > 0:
                self.x -= 1
            elif self.y > 0:
                # Move cursor to the end of the previous line if at the start of a line
                self.y -= 1
                self.x = len(self.gap_buffer.get_text().split('\n')[self.y])
            self.update_lines()
