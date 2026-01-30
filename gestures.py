"""
Smart Touch Gesture Recognition for ABook
Swipe gestures, long press, multi-touch
"""

import pygame
import time
from config import COLOR_BLACK, COLOR_WHITE


class GestureRecognizer:
    """Recognizes touch gestures for navigation"""
    
    def __init__(self):
        # Gesture state
        self.touch_start_pos = None
        self.touch_start_time = None
        self.is_long_press = False
        self.swipe_threshold = 100  # pixels
        self.long_press_duration = 0.5  # seconds
        
        # Multi-touch (for future)
        self.touch_points = []
        
        # Gesture history
        self.last_gesture = None
        self.last_gesture_time = 0
        
    def start_touch(self, pos):
        """Register touch start"""
        self.touch_start_pos = pos
        self.touch_start_time = time.time()
        self.is_long_press = False
        
    def update_touch(self, pos):
        """Update touch position (for detecting long press)"""
        if self.touch_start_time:
            elapsed = time.time() - self.touch_start_time
            
            # Check if it's a long press (not moving much)
            if elapsed > self.long_press_duration:
                if self.touch_start_pos:
                    dx = abs(pos[0] - self.touch_start_pos[0])
                    dy = abs(pos[1] - self.touch_start_pos[1])
                    
                    # If not moved much, it's a long press
                    if dx < 10 and dy < 10:
                        self.is_long_press = True
                        return 'long_press', pos
        
        return None, None
    
    def end_touch(self, pos):
        """Detect gesture on touch end"""
        if not self.touch_start_pos:
            return None, None
        
        # Calculate swipe distance and direction
        dx = pos[0] - self.touch_start_pos[0]
        dy = pos[1] - self.touch_start_pos[1]
        distance = (dx**2 + dy**2) ** 0.5
        
        elapsed = time.time() - self.touch_start_time
        
        # Long press (already handled in update)
        if self.is_long_press:
            gesture = 'long_press'
            data = pos
        
        # Swipe gestures (need sufficient distance and speed)
        elif distance > self.swipe_threshold and elapsed < 0.5:
            # Determine dominant direction
            if abs(dx) > abs(dy):
                # Horizontal swipe
                if dx > 0:
                    gesture = 'swipe_right'
                    data = 'back'  # Swipe right = go back
                else:
                    gesture = 'swipe_left'
                    data = 'forward'
            else:
                # Vertical swipe
                if dy > 0:
                    gesture = 'swipe_down'
                    data = 'scroll_down'
                else:
                    gesture = 'swipe_up'
                    data = 'scroll_up'
        else:
            # Regular tap
            gesture = 'tap'
            data = pos
        
        # Reset state
        self.touch_start_pos = None
        self.touch_start_time = None
        self.is_long_press = False
        
        # Store for debugging
        self.last_gesture = gesture
        self.last_gesture_time = time.time()
        
        return gesture, data
    
    def cancel_touch(self):
        """Cancel current touch (e.g., when leaving area)"""
        self.touch_start_pos = None
        self.touch_start_time = None
        self.is_long_press = False
    
    def is_swipe_gesture(self, start_pos, end_pos):
        """Check if movement qualifies as swipe"""
        if not start_pos or not end_pos:
            return False
        
        dx = abs(end_pos[0] - start_pos[0])
        dy = abs(end_pos[1] - start_pos[1])
        distance = (dx**2 + dy**2) ** 0.5
        
        return distance > self.swipe_threshold
    
    def get_swipe_direction(self, start_pos, end_pos):
        """Get swipe direction"""
        if not start_pos or not end_pos:
            return None
        
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        if abs(dx) > abs(dy):
            return 'right' if dx > 0 else 'left'
        else:
            return 'down' if dy > 0 else 'up'


class GestureIndicator:
    """Visual feedback for gestures"""
    
    def __init__(self, fonts):
        self.font_s, self.font_m, self.font_l = fonts
        self.active = False
        self.gesture_type = None
        self.start_time = 0
        self.duration = 1.0  # seconds
        
    def show(self, gesture_type):
        """Show gesture indicator"""
        self.active = True
        self.gesture_type = gesture_type
        self.start_time = time.time()
    
    def draw(self, screen):
        """Draw gesture indicator (grayscale)"""
        if not self.active:
            return
        
        elapsed = time.time() - self.start_time
        if elapsed > self.duration:
            self.active = False
            return
        
        # Fade out effect
        alpha = int(255 * (1 - elapsed / self.duration))
        
        # Draw at bottom of screen
        y = 950
        
        # Background
        rect = pygame.Rect(150, y, 300, 50)
        surf = pygame.Surface((300, 50), pygame.SRCALPHA)
        pygame.draw.rect(surf, (200, 200, 200, alpha), (0, 0, 300, 50), border_radius=10)
        screen.blit(surf, (150, y))
        
        # Gesture icon/text
        gesture_icons = {
            'swipe_right': '← Swipe Right (Back)',
            'swipe_left': 'Swipe Left →',
            'swipe_up': '↑ Swipe Up',
            'swipe_down': '↓ Swipe Down',
            'long_press': 'Long Press',
            'tap': 'Tap'
        }
        
        text = gesture_icons.get(self.gesture_type, self.gesture_type)
        text_surf = self.font_m.render(text, True, (50, 50, 50))
        text_x = 150 + (300 - text_surf.get_width()) // 2
        screen.blit(text_surf, (text_x, y + 15))


# Gesture tutorial overlay
class GestureTutorial:
    """Show gesture tutorial on first launch"""
    
    def __init__(self, fonts):
        self.font_s, self.font_m, self.font_l = fonts
        self.shown = False
        
    def draw(self, screen):
        """Draw tutorial overlay"""
        # Dark overlay
        overlay = pygame.Surface((600, 1024), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 180), (0, 0, 600, 1024))
        screen.blit(overlay, (0, 0))
        
        # Tutorial panel
        panel_rect = pygame.Rect(50, 200, 500, 600)
        pygame.draw.rect(screen, (240, 240, 240), panel_rect, border_radius=15)
        pygame.draw.rect(screen, (100, 100, 100), panel_rect, 3, border_radius=15)
        
        # Title
        title = self.font_l.render("Smart Touch Gestures", True, COLOR_BLACK)
        screen.blit(title, (100, 230))
        
        # Gestures
        gestures = [
            ("→ Swipe Right", "Go Back"),
            ("← Swipe Left", "Go Forward"),
            ("↑ Swipe Up", "Scroll Up"),
            ("↓ Swipe Down", "Scroll Down"),
            ("Long Press", "Context Menu (future)"),
            ("Tap", "Select/Click"),
        ]
        
        y = 300
        for gesture, action in gestures:
            # Gesture
            gesture_text = self.font_m.render(gesture, True, (50, 50, 50))
            screen.blit(gesture_text, (80, y))
            
            # Separator
            sep_text = self.font_m.render("→", True, (150, 150, 150))
            screen.blit(sep_text, (280, y))
            
            # Action
            action_text = self.font_m.render(action, True, (100, 100, 100))
            screen.blit(action_text, (320, y))
            
            y += 60
        
        # Close button
        close_btn = pygame.Rect(200, 720, 200, 50)
        pygame.draw.rect(screen, (80, 80, 80), close_btn, border_radius=10)
        close_text = self.font_l.render("Got It!", True, COLOR_WHITE)
        screen.blit(close_text, (240, 730))
        
        return close_btn