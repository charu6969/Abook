"""
UI Components for ABook application
"""
import pygame
from datetime import datetime
from config import *


def draw_status_bar(screen, font_s):
    """Render status bar with time, WiFi, and battery - FOR PORTRAIT 600x1024"""
    # Status bar for portrait mode
    bar_width = 600  # Portrait width
    pygame.draw.rect(screen, COLOR_PAPER, (0, 0, bar_width, 25))
    
    # Time - CENTERED in portrait width
    time_str = datetime.now().strftime("%H:%M")
    time_surface = font_s.render(time_str, True, COLOR_BLACK)
    time_x = (bar_width - time_surface.get_width()) // 2  # Center properly
    screen.blit(time_surface, (time_x, 4))
    
    # WiFi icon - left side
    wifi_x, wifi_y = 15, 12
    pygame.draw.circle(screen, COLOR_BLACK, (wifi_x, wifi_y + 3), 2)
    for i in range(1, 3):
        pygame.draw.arc(
            screen,
            COLOR_BLACK,
            (wifi_x - i * 4, wifi_y - i * 3, i * 8, i * 8),
            0.5, 2.5, 1
        )
    
    # Battery icon - right side (portrait width)
    battery_x, battery_y = bar_width - 45, 6
    pygame.draw.rect(screen, COLOR_BLACK, (battery_x, battery_y, 25, 12), 1)
    pygame.draw.rect(screen, COLOR_BLACK, (battery_x + 25, battery_y + 3, 2, 6))
    pygame.draw.rect(screen, COLOR_BLACK, (battery_x + 2, battery_y + 2, 18, 8))  # 75% fill


class OnScreenKeyboard:
    """On-screen keyboard for text input"""
    def __init__(self, font):
        self.font = font
        self.visible = False
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫'],
            ['Space', 'Done']
        ]
        self.key_rects = []
    
    def draw(self, screen):
        """Draw the keyboard on screen"""
        if not self.visible:
            return
        
        panel = pygame.Rect(0, DISPLAY_HEIGHT - 250, DISPLAY_WIDTH, 250)
        pygame.draw.rect(screen, COLOR_WHITE, panel)
        pygame.draw.line(screen, COLOR_UI_LIGHT, (0, panel.y), (DISPLAY_WIDTH, panel.y), 2)
        
        self.key_rects = []
        y = panel.y + 20
        
        for row in self.keys:
            x = 20
            for key in row:
                # Determine key width
                if key == 'Space':
                    w = 150
                elif key == 'Done':
                    w = 80
                else:
                    w = 45
                
                rect = pygame.Rect(x, y, w, 40)
                
                # Draw key background
                color = COLOR_BLACK if key == 'Done' else COLOR_UI_LIGHT
                pygame.draw.rect(screen, color, rect, border_radius=5)
                
                # Draw key text
                text_color = COLOR_WHITE if key == 'Done' else COLOR_BLACK
                txt = self.font.render(key, True, text_color)
                screen.blit(
                    txt,
                    (rect.centerx - txt.get_width() // 2,
                     rect.centery - txt.get_height() // 2)
                )
                
                self.key_rects.append((rect, key))
                x += w + 8
            y += 48