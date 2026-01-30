import pygame
from constants import *

class NotepadPage:
    def __init__(self, screen, font_s):
        self.screen = screen
        self.font_s = font_s
        self.tool = 'pen'
        self.p_size = 4
        self.e_size = 30

    def draw(self, notebook, active_layer):
        self.screen.fill(COLOR_WHITE)
        draw_status_bar(self.screen, self.font_s)
        # ... (Insert Toolbar and Drawing logic)