class WordWrapper():

    def __init__(self, stdscr):
        self.stdscr = stdscr

    def get_window_width(self):
        width = self.stdscr.getmaxyx()
        return width

    def wrap_text(self, text, margin_width):
        wrapped_lines = []
        current_line = ""
        words = text.split(' ')
        _, cols = self.get_window_width()

        for word in words:
            # Check if adding the next word exceeds the window width
            if len(current_line) + len(word) + 1 <= cols - margin_width:
                current_line += word + " "
            else:
                wrapped_lines.append(current_line.rstrip())
                current_line = word + " "

          # Add the last line
        wrapped_lines.append(current_line.rstrip())

        return wrapped_lines
