"""
Lock screen for ABook
Swipe right to unlock
"""
import pygame
from config import *


class LockScreen:
    """Lock screen with swipe to unlock"""
    
    def __init__(self, fonts):
        self.font_s, self.font_m, self.font_l = fonts
        self.font_xl = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_xxl = pygame.font.SysFont('Arial', 64, bold=True)
        
        # Swipe state
        self.swipe_start_x = None
        self.current_x = 0
        self.is_swiping = False
        self.swipe_threshold = 400  # Need to swipe 400px to unlock
        
    def draw(self, screen):
        """Draw the lock screen"""
        # Dark background
        screen.fill((40, 40, 40))
        
        # Time display
        import datetime
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M")
        date_str = now.strftime("%A, %B %d")
        
        time_text = self.font_xxl.render(time_str, True, (255, 255, 255))
        time_x = (600 - time_text.get_width()) // 2
        screen.blit(time_text, (time_x, 200))
        
        date_text = self.font_m.render(date_str, True, (180, 180, 180))
        date_x = (600 - date_text.get_width()) // 2
        screen.blit(date_text, (date_x, 280))
        
        # ABook branding with lowercase 'b'
        abook_font = pygame.font.SysFont('Arial', 42, bold=False)
        
        # Draw "ABook" with capital A and lowercase b
        abook_text = abook_font.render("ABook", True, (255, 255, 255))
        abook_x = (600 - abook_text.get_width()) // 2
        screen.blit(abook_text, (abook_x, 350))
        
        # Subtitle
        subtitle_text = self.font_s.render("Digital Notebook Reimagined", True, (150, 150, 150))
        subtitle_x = (600 - subtitle_text.get_width()) // 2
        screen.blit(subtitle_text, (subtitle_x, 400))
        
        # Swipe indicator
        swipe_y = 800
        
        # Draw swipe track
        track_rect = pygame.Rect(50, swipe_y, 500, 60)
        pygame.draw.rect(screen, (60, 60, 60), track_rect, border_radius=30)
        
        # Draw swipe button
        if self.is_swiping:
            button_x = min(50 + self.current_x, 490)
        else:
            button_x = 50
        
        button_rect = pygame.Rect(button_x, swipe_y, 60, 60)
        pygame.draw.rect(screen, (200, 200, 200), button_rect, border_radius=30)
        
        # Draw arrow in button
        arrow_x = button_x + 30
        arrow_y = swipe_y + 30
        arrow_points = [
            (arrow_x - 10, arrow_y),
            (arrow_x + 10, arrow_y - 8),
            (arrow_x + 10, arrow_y + 8)
        ]
        pygame.draw.polygon(screen, (40, 40, 40), arrow_points)
        
        # Instruction text
        if not self.is_swiping:
            instruction = self.font_m.render("Swipe up to unlock", True, (180, 180, 180))
            instruction_x = (600 - instruction.get_width()) // 2
            screen.blit(instruction, (instruction_x, swipe_y - 50))
        
        # "Powered by ABook" at bottom
        footer_text = self.font_s.render("Powered by Abook™", True, (100, 100, 100))
        footer_x = (600 - footer_text.get_width()) // 2
        screen.blit(footer_text, (footer_x, 980))
    
    def handle_mouse_down(self, pos):
        """Handle mouse/touch down"""
        # Check if touching the swipe area
        if 800 <= pos[1] <= 860 and 50 <= pos[0] <= 550:
            self.is_swiping = True
            self.swipe_start_x = pos[0]
            self.current_x = 0
    
    def handle_mouse_motion(self, pos):
        """Handle mouse/touch motion"""
        if self.is_swiping and self.swipe_start_x:
            # Calculate swipe distance
            self.current_x = pos[0] - self.swipe_start_x
            # Clamp to valid range
            self.current_x = max(0, min(440, self.current_x))
    
    def handle_mouse_up(self, pos):
        """Handle mouse/touch release - returns True if unlocked"""
        if self.is_swiping:
            # Check if swiped far enough
            if self.current_x >= self.swipe_threshold:
                # Unlocked!
                self.is_swiping = False
                self.swipe_start_x = None
                self.current_x = 0
                return True
            else:
                # Not far enough, reset
                self.is_swiping = False
                self.swipe_start_x = None
                self.current_x = 0
        
        return False