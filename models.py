"""
Data models for ABook application
"""
import pygame
from config import DISPLAY_WIDTH, DISPLAY_HEIGHT


class Layer:
    """Represents a drawing layer in a notebook"""
    def __init__(self, template_name="Blank"):
        # Create a larger canvas for scrolling - USE PORTRAIT DIMENSIONS
        # Portrait: 600 wide, 1024 tall (after rotation)
        canvas_width = 600 - 80  # 600px portrait width - 80px toolbar
        canvas_height = 1024 * 5  # 5x portrait height for scrolling
        self.surf = pygame.Surface((canvas_width, canvas_height), pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))  # Transparent white
        self.visible = True
        self.modified = False
        self.template_name = template_name
        self.name = f"Layer"  # Can be renamed by user


class Notebook:
    """Represents a notebook with multiple layers"""
    def __init__(self, name, folder='notes'):
        self.name = name
        self.folder = folder  # 'notes' or 'books'
        self.layers = [Layer()]
        self.template_name = "Blank"  # Current template for new layers