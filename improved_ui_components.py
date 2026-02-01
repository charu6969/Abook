"""
Improved UI Components with better icons and grayscale design
"""
import pygame
from datetime import datetime
from config import *


def draw_improved_status_bar(screen, font_s):
    """Enhanced status bar with better icons - GRAYSCALE"""
    bar_width = 600  # Portrait width
    pygame.draw.rect(screen, (250, 250, 250), (0, 0, bar_width, 25))  # Light gray background
    pygame.draw.line(screen, (200, 200, 200), (0, 25), (bar_width, 25), 1)  # Separator
    
    # Time - CENTERED
    time_str = datetime.now().strftime("%H:%M")
    time_surface = font_s.render(time_str, True, (40, 40, 40))
    time_x = (bar_width - time_surface.get_width()) // 2
    screen.blit(time_surface, (time_x, 4))
    
    # Enhanced WiFi icon - left side
    draw_enhanced_wifi_icon(screen, 15, 12, (40, 40, 40))
    
    # Enhanced Battery icon - right side
    draw_enhanced_battery_icon(screen, bar_width - 50, 6, (40, 40, 40), 85)


def draw_enhanced_wifi_icon(screen, x, y, color):
    """Draw improved WiFi icon with better design - GRAYSCALE"""
    # Base point (center bottom)
    base_x, base_y = x, y + 6
    
    # Signal strength indicator (3 curved lines)
    for i in range(3):
        radius = 6 + i * 4
        thickness = 2
        # Draw arc
        rect = pygame.Rect(base_x - radius, base_y - radius, radius * 2, radius * 2)
        # Simulate arc by drawing multiple small lines
        import math
        start_angle = -0.6  # Start angle in radians
        end_angle = 0.6    # End angle in radians
        steps = 10
        
        for step in range(steps):
            angle1 = start_angle + (end_angle - start_angle) * step / steps
            angle2 = start_angle + (end_angle - start_angle) * (step + 1) / steps
            
            x1 = base_x + radius * math.sin(angle1)
            y1 = base_y - radius * math.cos(angle1)
            x2 = base_x + radius * math.sin(angle2)
            y2 = base_y - radius * math.cos(angle2)
            
            pygame.draw.line(screen, color, (int(x1), int(y1)), (int(x2), int(y2)), thickness)
    
    # Center dot
    pygame.draw.circle(screen, color, (base_x, base_y), 2)


def draw_enhanced_battery_icon(screen, x, y, color, percentage):
    """Draw improved battery icon with percentage - GRAYSCALE"""
    # Battery body
    body_width = 28
    body_height = 14
    pygame.draw.rect(screen, color, (x, y, body_width, body_height), 2, border_radius=2)
    
    # Battery terminal (small rectangle on right)
    pygame.draw.rect(screen, color, (x + body_width, y + 4, 3, 6))
    
    # Fill level based on percentage
    fill_width = int((body_width - 4) * percentage / 100)
    
    # Color based on battery level (grayscale)
    if percentage > 50:
        fill_color = (80, 80, 80)  # Dark gray (good)
    elif percentage > 20:
        fill_color = (120, 120, 120)  # Medium gray (medium)
    else:
        fill_color = (160, 160, 160)  # Light gray (low)
    
    if fill_width > 0:
        pygame.draw.rect(screen, fill_color, (x + 2, y + 2, fill_width, body_height - 4))


def draw_enhanced_notebook_icon(screen, x, y, size=60, has_content=True):
    """Draw improved notebook icon - GRAYSCALE"""
    # Background (paper white)
    body_rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, (255, 255, 255), body_rect, border_radius=4)
    pygame.draw.rect(screen, (100, 100, 100), body_rect, 2, border_radius=4)  # Dark gray border
    
    # Spiral binding on left (multiple rings)
    ring_count = 4
    ring_spacing = size // (ring_count + 1)
    for i in range(1, ring_count + 1):
        ring_y = y + i * ring_spacing
        # Draw ring as two half circles
        pygame.draw.circle(screen, (120, 120, 120), (x - 2, ring_y), 4, 2)
    
    # Content lines (if has content)
    if has_content:
        line_color = (180, 180, 180)
        line_start_x = x + size // 4
        line_end_x = x + size * 3 // 4
        line_y = y + size // 3
        
        for i in range(3):
            pygame.draw.line(screen, line_color, 
                           (line_start_x, line_y + i * 8), 
                           (line_end_x, line_y + i * 8), 1)
    
    # Corner fold (top right)
    fold_size = size // 4
    fold_points = [
        (x + size - fold_size, y),
        (x + size, y),
        (x + size, y + fold_size),
        (x + size - fold_size, y + fold_size)
    ]
    pygame.draw.polygon(screen, (220, 220, 220), fold_points)
    pygame.draw.line(screen, (100, 100, 100), 
                    (x + size - fold_size, y), 
                    (x + size - fold_size, y + fold_size), 2)
    pygame.draw.line(screen, (100, 100, 100), 
                    (x + size - fold_size, y + fold_size), 
                    (x + size, y + fold_size), 2)


def draw_enhanced_folder_icon(screen, x, y, size=60):
    """Draw improved folder icon - GRAYSCALE"""
    # Folder tab (top)
    tab_width = size // 2
    tab_height = size // 5
    pygame.draw.rect(screen, (140, 140, 140), 
                    (x, y, tab_width, tab_height), border_radius=3)
    
    # Folder body
    body_height = size * 2 // 3
    pygame.draw.rect(screen, (180, 180, 180), 
                    (x, y + tab_height, size, body_height), border_radius=5)
    pygame.draw.rect(screen, (100, 100, 100), 
                    (x, y + tab_height, size, body_height), 2, border_radius=5)
    
    # Folder label line
    pygame.draw.line(screen, (220, 220, 220), 
                    (x + size//4, y + tab_height + body_height//2), 
                    (x + size*3//4, y + tab_height + body_height//2), 2)


class ImprovedKeyboard:
    """Improved on-screen keyboard with better design - GRAYSCALE"""
    def __init__(self, font):
        self.font = font
        self.font_key = pygame.font.SysFont('Arial', 18, bold=True)
        self.visible = False
        self.shift_active = False
        
        # Better key layout
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['⇧', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫'],
            ['Space', '.', '-', '_', 'Done']
        ]
        self.key_rects = []
    
    def draw(self, screen):
        """Draw improved keyboard - GRAYSCALE"""
        if not self.visible:
            return
        
        # Keyboard panel - portrait mode (600 wide)
        panel_height = 280
        panel_y = 1024 - panel_height  # Portrait height
        panel = pygame.Rect(0, panel_y, 600, panel_height)
        
        # Background with subtle gradient
        for i in range(panel_height):
            gray = 230 - int(i * 0.1)  # Subtle gradient
            pygame.draw.line(screen, (gray, gray, gray), (0, panel_y + i), (600, panel_y + i))
        
        # Top border
        pygame.draw.line(screen, (150, 150, 150), (0, panel_y), (600, panel_y), 2)
        
        self.key_rects = []
        y = panel_y + 15
        
        for row_idx, row in enumerate(self.keys):
            # Calculate row width for centering
            row_width = sum(self._get_key_width(key) + 6 for key in row) - 6
            x = (600 - row_width) // 2  # Center the row
            
            for key in row:
                w = self._get_key_width(key)
                h = 45
                
                rect = pygame.Rect(x, y, w, h)
                
                # Determine key color
                if key == 'Done':
                    bg_color = (80, 80, 80)  # Dark gray
                    text_color = (255, 255, 255)  # White
                elif key == '⇧' and self.shift_active:
                    bg_color = (120, 120, 120)  # Active gray
                    text_color = (255, 255, 255)
                elif key in ['⇧', '⌫']:
                    bg_color = (180, 180, 180)  # Light gray
                    text_color = (40, 40, 40)
                else:
                    bg_color = (255, 255, 255)  # White
                    text_color = (40, 40, 40)
                
                # Draw key with shadow
                shadow_rect = rect.copy()
                shadow_rect.y += 2
                pygame.draw.rect(screen, (200, 200, 200), shadow_rect, border_radius=8)
                
                # Draw key
                pygame.draw.rect(screen, bg_color, rect, border_radius=8)
                pygame.draw.rect(screen, (160, 160, 160), rect, 1, border_radius=8)
                
                # Draw key text
                display_key = key
                if key.isalpha() and not self.shift_active:
                    display_key = key.lower()
                
                txt = self.font_key.render(display_key, True, text_color)
                screen.blit(txt, 
                          (rect.centerx - txt.get_width() // 2,
                           rect.centery - txt.get_height() // 2))
                
                self.key_rects.append((rect, key))
                x += w + 6
            
            y += 52
    
    def _get_key_width(self, key):
        """Get width for specific key"""
        if key == 'Space':
            return 180
        elif key == 'Done':
            return 100
        elif key in ['⇧', '⌫']:
            return 55
        else:
            return 50
    
    def handle_click(self, pos):
        """Handle keyboard click"""
        if not self.visible:
            return None
        
        for rect, key in self.key_rects:
            if rect.collidepoint(pos):
                if key == '⇧':
                    self.shift_active = not self.shift_active
                    return None
                elif key == 'Done':
                    return ('done', None)
                elif key == '⌫':
                    return ('backspace', None)
                elif key == 'Space':
                    return ('char', ' ')
                else:
                    char = key if self.shift_active or key.isdigit() or key in ['.', '-', '_'] else key.lower()
                    if key.isalpha():
                        self.shift_active = False  # Turn off shift after letter
                    return ('char', char)
        return None
