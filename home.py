import pygame
from constants import *

class HomePage:
    def __init__(self, screen, font_s, font_l):
        self.screen = screen
        self.font_s = font_s
        self.font_l = font_l
        self.renaming_idx = None
    
    def draw(self, notebooks, keyboard):
        self.screen.fill(COLOR_WHITE)
        draw_status_bar(self.screen, self.font_s)
        # ... (Insert Home Screen rendering logic)