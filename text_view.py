"""
Text view for displaying and editing converted handwriting
"""
import pygame
from config import *
from ui_components import draw_status_bar


class TextView:
    """View for displaying converted text with formatting options"""
    
    def __init__(self, fonts):
        self.font_s, self.font_m, self.font_l = fonts
        
        # Text content
        self.text = ""
        self.summary = ""
        self.show_summary = False
        
        # Font settings
        self.current_font_index = 0
        self.current_size_index = 3  # 18pt default
        self.text_font = None
        self.update_font()
        
        # UI elements
        self.back_btn = None
        self.convert_btn = None
        self.summarize_btn = None
        self.font_btn = None
        self.size_up_btn = None
        self.size_down_btn = None
        
        # Scrolling
        self.scroll_offset = 0
        self.line_height = 25
    
    def update_font(self):
        """Update the text rendering font"""
        font_name = AVAILABLE_FONTS[self.current_font_index][0]
        size = TEXT_SIZES[self.current_size_index]
        
        try:
            self.text_font = pygame.font.SysFont(font_name, size)
        except:
            self.text_font = pygame.font.SysFont('Arial', size)
    
    def set_text(self, text):
        """Set the text content"""
        self.text = text
        self.scroll_offset = 0
        self.show_summary = False
    
    def set_summary(self, summary):
        """Set the summary content"""
        self.summary = summary
    
    def toggle_summary(self):
        """Toggle between full text and summary"""
        if self.summary:
            self.show_summary = not self.show_summary
    
    def change_font(self):
        """Cycle to next font"""
        self.current_font_index = (self.current_font_index + 1) % len(AVAILABLE_FONTS)
        self.update_font()
    
    def change_size(self, increase):
        """Change font size"""
        if increase and self.current_size_index < len(TEXT_SIZES) - 1:
            self.current_size_index += 1
        elif not increase and self.current_size_index > 0:
            self.current_size_index -= 1
        self.update_font()
    
    def draw(self, screen):
        """Draw the text view"""
        screen.fill(COLOR_WHITE)
        draw_status_bar(screen, self.font_s)
        
        # Toolbar
        toolbar_height = 60
        pygame.draw.rect(screen, COLOR_PAPER, (0, 25, DISPLAY_WIDTH, toolbar_height))
        
        # Back button
        self.back_btn = pygame.Rect(10, 35, 70, 40)
        pygame.draw.rect(screen, COLOR_UI_LIGHT, self.back_btn, border_radius=20)
        back_text = self.font_s.render("← Back", True, COLOR_BLACK)
        screen.blit(back_text, (15, 45))
        
        # Font selector
        self.font_btn = pygame.Rect(90, 35, 100, 40)
        pygame.draw.rect(screen, COLOR_UI_LIGHT, self.font_btn, border_radius=5)
        font_name = AVAILABLE_FONTS[self.current_font_index][0].split()[0]
        font_text = self.font_s.render(font_name, True, COLOR_BLACK)
        screen.blit(font_text, (self.font_btn.centerx - font_text.get_width()//2, 45))
        
        # Size controls
        self.size_down_btn = pygame.Rect(200, 35, 35, 40)
        self.size_up_btn = pygame.Rect(245, 35, 35, 40)
        
        pygame.draw.rect(screen, COLOR_UI_LIGHT, self.size_down_btn, border_radius=5)
        pygame.draw.rect(screen, COLOR_UI_LIGHT, self.size_up_btn, border_radius=5)
        
        minus_text = self.font_m.render("−", True, COLOR_BLACK)
        plus_text = self.font_m.render("+", True, COLOR_BLACK)
        screen.blit(minus_text, (self.size_down_btn.centerx - 6, 40))
        screen.blit(plus_text, (self.size_up_btn.centerx - 6, 40))
        
        # Size indicator
        size_text = self.font_s.render(f"{TEXT_SIZES[self.current_size_index]}", True, COLOR_BLACK)
        screen.blit(size_text, (290, 45))
        
        # Summary toggle (if summary available)
        if self.summary:
            self.summarize_btn = pygame.Rect(DISPLAY_WIDTH - 120, 35, 110, 40)
            color = COLOR_ACCENT if self.show_summary else COLOR_UI_LIGHT
            pygame.draw.rect(screen, color, self.summarize_btn, border_radius=5)
            text_color = COLOR_WHITE if self.show_summary else COLOR_BLACK
            summary_text = self.font_s.render("Summary", True, text_color)
            screen.blit(summary_text, (self.summarize_btn.centerx - 30, 45))
        
        # Text content area
        content_y = 25 + toolbar_height + 20
        content_height = DISPLAY_HEIGHT - content_y - 20
        
        # Render text with word wrapping
        display_text = self.summary if self.show_summary else self.text
        
        if display_text:
            self._render_wrapped_text(screen, display_text, 20, content_y, 
                                     DISPLAY_WIDTH - 40, content_height)
        else:
            # Placeholder
            placeholder = self.font_m.render("No text converted yet", True, COLOR_UI_DARK)
            screen.blit(placeholder, (DISPLAY_WIDTH//2 - 100, DISPLAY_HEIGHT//2))
    
    def _render_wrapped_text(self, screen, text, x, y, max_width, max_height):
        """Render text with word wrapping and scrolling"""
        words = text.split()
        lines = []
        current_line = []
        
        # Word wrap
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.text_font.render(test_line, True, COLOR_BLACK)
            
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate line height
        line_height = self.text_font.get_linesize()
        
        # Render visible lines with scroll offset
        y_pos = y - self.scroll_offset
        
        for line in lines:
            if y_pos > y - line_height and y_pos < y + max_height:
                line_surface = self.text_font.render(line, True, COLOR_BLACK)
                screen.blit(line_surface, (x, y_pos))
            y_pos += line_height
    
    def handle_scroll(self, y_delta):
        """Handle scroll events"""
        self.scroll_offset -= y_delta * 20
        self.scroll_offset = max(0, self.scroll_offset)
    
    def handle_click(self, pos):
        """
        Handle click events
        Returns: (action, data) tuple
        """
        if self.back_btn and self.back_btn.collidepoint(pos):
            return ('back', None)
        
        if self.font_btn and self.font_btn.collidepoint(pos):
            return ('change_font', None)
        
        if self.size_up_btn and self.size_up_btn.collidepoint(pos):
            return ('size_up', None)
        
        if self.size_down_btn and self.size_down_btn.collidepoint(pos):
            return ('size_down', None)
        
        if self.summarize_btn and self.summarize_btn.collidepoint(pos):
            return ('toggle_summary', None)
        
        return (None, None)