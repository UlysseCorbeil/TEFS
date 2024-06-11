from abc import ABC, abstractmethod 

class Event():

    @abstractmethod
    def __init__(self, stdscr, x, y):
        self.stdscr = stdscr
        self.x, self.y = x, y

    @abstractmethod
    def trigger(self):
        pass
