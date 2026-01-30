"""
Templates for different notebook page styles
"""
import pygame
from config import *


class Template:
    """Base template class"""
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def draw(self, surface):
        """Draw the template on the surface"""
        pass


class BlankTemplate(Template):
    """Blank white page"""
    def __init__(self):
        super().__init__("Blank", "Plain white page")
    
    def draw(self, surface):
        surface.fill(COLOR_WHITE)


class SingleLineTemplate(Template):
    """Single ruled lines like a notebook"""
    def __init__(self):
        super().__init__("Single Line", "Ruled notebook lines")
        self.line_spacing = 40  # Space between lines
        self.line_color = (200, 200, 255)  # Light blue
    
    def draw(self, surface):
        surface.fill(COLOR_WHITE)
        width = surface.get_width()
        height = surface.get_height()
        
        # Draw horizontal lines
        y = self.line_spacing
        while y < height:
            pygame.draw.line(surface, self.line_color, (0, y), (width, y), 1)
            y += self.line_spacing
        
        # Draw left margin line (red)
        margin_x = 80
        pygame.draw.line(surface, (255, 200, 200), (margin_x, 0), (margin_x, height), 2)


class DoubleLineTemplate(Template):
    """Double ruled lines for better writing"""
    def __init__(self):
        super().__init__("Double Line", "Double ruled lines")
        self.line_spacing = 50
        self.sub_line_spacing = 25
        self.dark_line_color = (180, 180, 220)
        self.light_line_color = (220, 220, 240)
    
    def draw(self, surface):
        surface.fill(COLOR_WHITE)
        width = surface.get_width()
        height = surface.get_height()
        
        # Draw lines
        y = 0
        while y < height:
            # Main line (darker)
            pygame.draw.line(surface, self.dark_line_color, (0, y), (width, y), 2)
            
            # Sub line (lighter)
            y += self.sub_line_spacing
            if y < height:
                pygame.draw.line(surface, self.light_line_color, (0, y), (width, y), 1)
            
            y += self.sub_line_spacing
        
        # Margin
        margin_x = 80
        pygame.draw.line(surface, (255, 200, 200), (margin_x, 0), (margin_x, height), 2)


class GraphTemplate(Template):
    """Graph paper grid"""
    def __init__(self):
        super().__init__("Graph", "Grid for diagrams")
        self.grid_size = 20  # Size of each grid square
        self.main_line_color = (200, 200, 220)
        self.sub_line_color = (230, 230, 240)
    
    def draw(self, surface):
        surface.fill(COLOR_WHITE)
        width = surface.get_width()
        height = surface.get_height()
        
        # Draw vertical lines
        x = 0
        count = 0
        while x < width:
            color = self.main_line_color if count % 5 == 0 else self.sub_line_color
            thickness = 2 if count % 5 == 0 else 1
            pygame.draw.line(surface, color, (x, 0), (x, height), thickness)
            x += self.grid_size
            count += 1
        
        # Draw horizontal lines
        y = 0
        count = 0
        while y < height:
            color = self.main_line_color if count % 5 == 0 else self.sub_line_color
            thickness = 2 if count % 5 == 0 else 1
            pygame.draw.line(surface, color, (0, y), (width, y), thickness)
            y += self.grid_size
            count += 1


class DottedTemplate(Template):
    """Dotted grid for bullet journaling"""
    def __init__(self):
        super().__init__("Dotted", "Dot grid pattern")
        self.dot_spacing = 25
        self.dot_color = (200, 200, 220)
        self.dot_size = 2
    
    def draw(self, surface):
        surface.fill(COLOR_WHITE)
        width = surface.get_width()
        height = surface.get_height()
        
        # Draw dots
        y = self.dot_spacing
        while y < height:
            x = self.dot_spacing
            while x < width:
                pygame.draw.circle(surface, self.dot_color, (x, y), self.dot_size)
                x += self.dot_spacing
            y += self.dot_spacing


# Available templates
TEMPLATES = [
    BlankTemplate(),
    SingleLineTemplate(),
    DoubleLineTemplate(),
    GraphTemplate(),
    DottedTemplate()
]


def get_template_by_name(name):
    """Get template by name"""
    for template in TEMPLATES:
        if template.name == name:
            return template
    return TEMPLATES[0]  # Return blank as default