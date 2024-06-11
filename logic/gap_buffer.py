import curses

class GapBuffer() :

    def __init__(self):
        self.buffer = [''] * 1024
        self.start, self.end = 0, len(self.buffer)

    def insert(self, position, text):
        self.move_gap(position)

        for char in text:
            if self.start < self.end:
                self.buffer[self.start] = char
                self.start += 1
            else:
                self.buffer.append(char)
                self.start += 1
                self.end += 1

    def delete(self, position):
        # Ensure the position is within bounds
        if position < 0 or position >= self.start:
            return

        # Move the gap to just after the position where deletion should occur
        self.move_gap(position + 1)

        if self.start > 0:
            self.start -= 1
            # clear the deleted character
            self.buffer[self.start] = ' '

    def move_gap(self, position):
        """Move the gap to the specified position."""
        if position < 0 or position > len(self.buffer):
            raise IndexError("Position out of bounds")

        # Move gap left
        while self.start > position:
            self.start -= 1
            self.buffer[self.start] = self.buffer[self.end - 1]
            self.buffer[self.end - 1] = ' '
            self.end -= 1

        # Move gap right
        while self.start < position and self.end < len(self.buffer):
            self.buffer[self.end] = self.buffer[self.start]
            self.end += 1
            self.start += 1
            self.buffer[self.start] = ' '

    def get_text(self):
        # Retrieve the current text, excluding the gap
        return ''.join(self.buffer[:self.start] + self.buffer[self.end:])

    def calc_insert_position(self, x, y):
        lines_up_to_cursor = self.get_text().split('\n')[:y]
        # Total length of text before the current line, adding one for each new line
        position = sum(len(line) for line in lines_up_to_cursor) + len(lines_up_to_cursor)

        # Add the horizontal position (x) to calculate the final insert position
        position += x

        return position


    def calc_gap_buffer_index(self, x, y):
        # Translate cursor positions to an index in the gap buffer
        lines = self.get_text().split('\n')
        index = sum(len(line) for line in lines[:y]) + y
        # Add horizontal position
        index += x
        return index
