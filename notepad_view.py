"""
Notepad view for ABook application - drawing interface with scrolling
"""
import pygame
from config import *
from ui_components import draw_status_bar

try:
    from writing_assistant import get_writing_assistant
    WRITING_ASSISTANT_AVAILABLE = True
except ImportError:
    WRITING_ASSISTANT_AVAILABLE = False
    print("[Info] Writing assistant not available - install: pip install pyspellchecker language-tool-python")


class NotepadView:
    """Notepad screen view for drawing with infinite scroll"""
    def __init__(self, fonts):
        self.font_s, self.font_m, self.font_l = fonts
        
        # UI element rects
        self.back_btn = None
        self.pen_btn = None
        self.eraser_btn = None
        self.size_up = None
        self.size_down = None
        self.convert_btn = None
        self.template_btn = None
        self.layers_btn = None
        self.search_btn = None
        
        # Drawing state
        self.tool = 'pen'
        self.pen_size = 4
        self.highlighter_size = 20  # Wide for highlighting
        self.eraser_size = 30
        self.drawing = False
        self.last_pos = None
        self.first_point = False  # Track if this is the first point of a stroke
        
        # Writing assistant
        if WRITING_ASSISTANT_AVAILABLE:
            self.writing_assistant = get_writing_assistant()
        else:
            self.writing_assistant = None
        
        # Suggestion state
        self.show_suggestions = False
        self.current_suggestions = []
        self.suggestion_word = ""
        self.suggestion_position = None
        
        # Scrolling state
        self.scroll_offset = 0
        self.canvas_height = 1024 * 5  # 5x PORTRAIT height (not DISPLAY_HEIGHT)
        self.toolbar_width = 80  # Slightly wider for 1024px
        self.toolbar_start_y = 25  # After status bar
        
        # Menu states
        self.show_template_menu = False
        self.show_layer_menu = False
        self.show_search_panel = False
        self.search_text = ""
        self.extracted_words = []
        self.show_definition = False
        self.current_word_definition = None
    
    def draw(self, screen, notebook):
        """Draw the notepad screen with left toolbar - BLACK AND WHITE THEME"""
        screen.fill(NOTEPAD_BG)  # Pure white background
        draw_status_bar(screen, self.font_s)
        
        # Get the canvas dimensions - PORTRAIT MODE
        portrait_width = 600
        portrait_height = 1024
        canvas_width = portrait_width - self.toolbar_width
        visible_height = portrait_height - self.toolbar_start_y
        
        # Create a surface for the visible canvas area
        visible_canvas = pygame.Surface((canvas_width, visible_height))
        visible_canvas.fill(NOTEPAD_BG)  # Pure white
        
        # Draw all visible layers onto the visible canvas
        for layer in notebook.layers:
            if layer.visible:
                # Blit the portion of the layer that should be visible
                # accounting for scroll offset
                source_rect = pygame.Rect(0, self.scroll_offset, canvas_width, visible_height)
                visible_canvas.blit(layer.surf, (0, 0), source_rect)
        
        # Draw the visible canvas to the screen
        screen.blit(visible_canvas, (self.toolbar_width, self.toolbar_start_y))
        
        # Draw left toolbar - Light gray - PORTRAIT HEIGHT
        portrait_height = 1024
        toolbar_rect = pygame.Rect(0, self.toolbar_start_y, self.toolbar_width, portrait_height - self.toolbar_start_y)
        pygame.draw.rect(screen, NOTEPAD_TOOLBAR, toolbar_rect)
        pygame.draw.line(screen, NOTEPAD_BUTTON, (self.toolbar_width, self.toolbar_start_y), 
                        (self.toolbar_width, portrait_height), 2)
        
        # Draw left toolbar - USE PORTRAIT HEIGHT
        portrait_height = 1024
        toolbar_rect = pygame.Rect(0, self.toolbar_start_y, self.toolbar_width, portrait_height - self.toolbar_start_y)
        pygame.draw.rect(screen, COLOR_PAPER, toolbar_rect)
        pygame.draw.line(screen, COLOR_UI_LIGHT, (self.toolbar_width, self.toolbar_start_y), 
                        (self.toolbar_width, portrait_height), 2)
        
        # Back button at top of toolbar - SMALLER
        self.back_btn = pygame.Rect(10, 35, 60, 35)
        pygame.draw.rect(screen, COLOR_UI_LIGHT, self.back_btn, border_radius=12)
        back_text = self.font_s.render("←", True, COLOR_BLACK)
        screen.blit(back_text, (self.back_btn.centerx - 6, self.back_btn.centery - 8))
        
        # Tool selection buttons - HIGH POSITION for full visibility
        y_pos = 85  # Right after back button (was 150)
        button_gap = 15  # Compact spacing
        button_height = 68
        
        # Create 3 tool buttons: Pen, Highlighter, Eraser
        self.pen_btn = pygame.Rect(10, y_pos, 60, button_height)
        self.highlighter_btn = pygame.Rect(10, y_pos + button_height + button_gap, 60, button_height)
        self.eraser_btn = pygame.Rect(10, y_pos + 2*(button_height + button_gap), 60, button_height)
        
        # === PEN BUTTON ===
        pen_active = self.tool == 'pen'
        pygame.draw.rect(screen, COLOR_BLACK if pen_active else COLOR_UI_LIGHT, 
                        self.pen_btn, border_radius=8)
        pen_color = COLOR_WHITE if pen_active else COLOR_BLACK
        pen_cx = self.pen_btn.centerx
        pen_icon_y = self.pen_btn.y + 18
        
        # Better pen icon - ballpoint pen style
        # Pen body (angled rectangle)
        pen_points = [
            (pen_cx - 3, pen_icon_y - 12),
            (pen_cx + 3, pen_icon_y - 12),
            (pen_cx + 2, pen_icon_y + 8),
            (pen_cx - 2, pen_icon_y + 8)
        ]
        pygame.draw.polygon(screen, pen_color, pen_points)
        # Pen tip (triangle)
        tip_points = [
            (pen_cx - 2, pen_icon_y + 8),
            (pen_cx + 2, pen_icon_y + 8),
            (pen_cx, pen_icon_y + 12)
        ]
        pygame.draw.polygon(screen, pen_color, tip_points)
        # Pen cap line
        pygame.draw.line(screen, pen_color, 
                        (pen_cx - 3, pen_icon_y - 6), 
                        (pen_cx + 3, pen_icon_y - 6), 2)
        
        # Pen label
        pen_label = self.font_s.render("Pen", True, pen_color)
        screen.blit(pen_label, (pen_cx - pen_label.get_width()//2, self.pen_btn.y + 48))
        
        # === HIGHLIGHTER BUTTON ===
        highlighter_active = self.tool == 'highlighter'
        pygame.draw.rect(screen, COLOR_BLACK if highlighter_active else COLOR_UI_LIGHT,
                        self.highlighter_btn, border_radius=8)
        hl_color = COLOR_WHITE if highlighter_active else COLOR_BLACK
        hl_cx = self.highlighter_btn.centerx
        hl_icon_y = self.highlighter_btn.y + 18
        
        # Highlighter icon - wide marker shape
        # Body (wide rectangle)
        hl_body = pygame.Rect(hl_cx - 8, hl_icon_y - 10, 16, 18)
        pygame.draw.rect(screen, hl_color, hl_body, 2)
        # Cap (small rectangle on top)
        pygame.draw.rect(screen, hl_color, (hl_cx - 6, hl_icon_y - 12, 12, 3))
        # Tip (wide trapezoid)
        tip_points = [
            (hl_cx - 8, hl_icon_y + 8),
            (hl_cx + 8, hl_icon_y + 8),
            (hl_cx + 6, hl_icon_y + 12),
            (hl_cx - 6, hl_icon_y + 12)
        ]
        pygame.draw.polygon(screen, hl_color, tip_points)
        
        # Highlighter label
        hl_label = self.font_s.render("Mark", True, hl_color)
        screen.blit(hl_label, (hl_cx - hl_label.get_width()//2, self.highlighter_btn.y + 48))
        
        # === ERASER BUTTON ===
        eraser_active = self.tool == 'eraser'
        pygame.draw.rect(screen, COLOR_BLACK if eraser_active else COLOR_UI_LIGHT, 
                        self.eraser_btn, border_radius=8)
        eraser_color = COLOR_WHITE if eraser_active else COLOR_BLACK
        eraser_cx = self.eraser_btn.centerx
        eraser_icon_y = self.eraser_btn.y + 18
        
        # Better eraser icon - 3D block style
        # Main body (rectangle with 3D effect)
        eraser_main = pygame.Rect(eraser_cx - 10, eraser_icon_y - 6, 20, 12)
        pygame.draw.rect(screen, eraser_color, eraser_main, 2)
        # Top edge (to show 3D)
        pygame.draw.line(screen, eraser_color,
                        (eraser_cx - 10, eraser_icon_y - 6),
                        (eraser_cx - 7, eraser_icon_y - 9), 2)
        pygame.draw.line(screen, eraser_color,
                        (eraser_cx + 10, eraser_icon_y - 6),
                        (eraser_cx + 13, eraser_icon_y - 9), 2)
        pygame.draw.line(screen, eraser_color,
                        (eraser_cx - 7, eraser_icon_y - 9),
                        (eraser_cx + 13, eraser_icon_y - 9), 2)
        
        # Eraser label
        eraser_label = self.font_s.render("Eraser", True, eraser_color)
        screen.blit(eraser_label, (eraser_cx - eraser_label.get_width()//2, self.eraser_btn.y + 48))
        
        # Calculate all button positions for PORTRAIT 600x1024
        # Lots of vertical space! No need to cram buttons
        
        button_height = 50  # Nice comfortable size
        button_spacing = 15  # Generous spacing
        bottom_margin = 25
        portrait_height = 1024  # PORTRAIT HEIGHT, not DISPLAY_HEIGHT (600)
        
        # Bottom buttons (6 buttons from bottom up) - USE PORTRAIT HEIGHT
        y_layers = portrait_height - bottom_margin - button_height
        y_template = y_layers - button_spacing - button_height
        y_convert = y_template - button_spacing - button_height
        y_search = y_convert - button_spacing - button_height
        y_pdf = y_search - button_spacing - button_height
        y_db = y_pdf - button_spacing - button_height
        
        # Size controls go ABOVE the bottom buttons with LOTS of space
        size_section_height = 120
        size_controls_start = y_db - button_spacing * 4 - size_section_height
        
        # Size up button - Nice and comfortable
        self.size_up = pygame.Rect(10, size_controls_start, 60, 40)
        pygame.draw.rect(screen, COLOR_UI_LIGHT, self.size_up, border_radius=5)
        plus_text = self.font_l.render("+", True, COLOR_BLACK)
        screen.blit(plus_text, (self.size_up.centerx - 10, self.size_up.centery - 12))
        
        # Current size indicator - Shows size for current tool
        if self.tool == 'pen':
            current_size = self.pen_size
        elif self.tool == 'highlighter':
            current_size = self.highlighter_size
        else:
            current_size = self.eraser_size
            
        size_y = size_controls_start + 45
        display_radius = min(current_size // 2, 20)  # Can be bigger
        pygame.draw.circle(screen, COLOR_BLACK, (40, size_y + 15), display_radius)
        size_text = self.font_s.render(f"{current_size}", True, COLOR_BLACK)
        screen.blit(size_text, (40 - size_text.get_width()//2, size_y + 35))
        
        # Size down button
        self.size_down = pygame.Rect(10, size_controls_start + 80, 60, 40)
        pygame.draw.rect(screen, COLOR_UI_LIGHT, self.size_down, border_radius=5)
        minus_text = self.font_l.render("−", True, COLOR_BLACK)
        screen.blit(minus_text, (self.size_down.centerx - 8, self.size_down.centery - 12))
        
        
        # Save to DB button (topmost of bottom buttons) - GRAYSCALE
        self.save_db_btn = pygame.Rect(10, y_db, 60, button_height)
        pygame.draw.rect(screen, (80, 80, 80), self.save_db_btn, border_radius=8)  # Dark grey
        # Draw save/database icon
        pygame.draw.rect(screen, COLOR_WHITE, (self.save_db_btn.centerx - 10, self.save_db_btn.centery - 8, 20, 16), 2)
        pygame.draw.line(screen, COLOR_WHITE, (self.save_db_btn.centerx - 6, self.save_db_btn.centery),
                        (self.save_db_btn.centerx + 6, self.save_db_btn.centery), 2)
        
        # Export PDF button - GRAYSCALE
        self.export_pdf_btn = pygame.Rect(10, y_pdf, 60, button_height)
        pygame.draw.rect(screen, (100, 100, 100), self.export_pdf_btn, border_radius=8)  # Medium grey
        pdf_text = self.font_s.render("PDF", True, COLOR_WHITE)
        screen.blit(pdf_text, (self.export_pdf_btn.centerx - 12, self.export_pdf_btn.centery - 8))
        
        # Search button
        self.search_btn = pygame.Rect(10, y_search, 60, button_height)
        color = COLOR_BLACK if self.show_search_panel else COLOR_UI_LIGHT
        pygame.draw.rect(screen, color, self.search_btn, border_radius=8)
        # Draw magnifying glass icon
        icon_color = COLOR_WHITE if self.show_search_panel else COLOR_BLACK
        search_x, search_y = self.search_btn.centerx, self.search_btn.centery - 3
        pygame.draw.circle(screen, icon_color, (search_x, search_y), 8, 2)
        pygame.draw.line(screen, icon_color, (search_x + 6, search_y + 6), (search_x + 10, search_y + 10), 2)
        
        # Convert to text button - GRAYSCALE
        self.convert_btn = pygame.Rect(10, y_convert, 60, button_height)
        pygame.draw.rect(screen, (120, 120, 120), self.convert_btn, border_radius=8)  # Light grey
        convert_text = self.font_m.render("Aa", True, COLOR_WHITE)
        screen.blit(convert_text, (self.convert_btn.centerx - 10, self.convert_btn.centery - 10))
        
        # Spell Check button - ALWAYS SHOW (handle missing library gracefully)
        # Position: between convert and search  
        y_spell = y_convert - button_spacing - button_height
        self.spell_check_btn = pygame.Rect(10, y_spell, 60, button_height)
        
        # Highlight if suggestions are showing
        btn_color = COLOR_BLACK if self.show_suggestions else (140, 140, 140)
        pygame.draw.rect(screen, btn_color, self.spell_check_btn, border_radius=8)
        
        # Draw "ABC✓" icon
        icon_color = COLOR_WHITE
        abc_text = self.font_s.render("ABC", True, icon_color)
        screen.blit(abc_text, (self.spell_check_btn.centerx - 15, self.spell_check_btn.centery - 12))
        
        # Draw checkmark
        check_x = self.spell_check_btn.centerx + 8
        check_y = self.spell_check_btn.centery + 5
        pygame.draw.line(screen, icon_color, (check_x - 3, check_y), (check_x, check_y + 3), 2)
        pygame.draw.line(screen, icon_color, (check_x, check_y + 3), (check_x + 5, check_y - 4), 2)
        
        # Template button
        self.template_btn = pygame.Rect(10, y_template, 60, button_height)
        color = COLOR_BLACK if self.show_template_menu else COLOR_UI_LIGHT
        pygame.draw.rect(screen, color, self.template_btn, border_radius=8)
        # Draw page icon (smaller)
        icon_x, icon_y = self.template_btn.centerx, self.template_btn.centery
        icon_color = COLOR_WHITE if self.show_template_menu else COLOR_BLACK
        pygame.draw.rect(screen, icon_color, (icon_x - 10, icon_y - 12, 20, 24), 2)
        pygame.draw.line(screen, icon_color, (icon_x - 6, icon_y - 6), (icon_x + 6, icon_y - 6), 1)
        pygame.draw.line(screen, icon_color, (icon_x - 6, icon_y), (icon_x + 6, icon_y), 1)
        pygame.draw.line(screen, icon_color, (icon_x - 6, icon_y + 6), (icon_x + 6, icon_y + 6), 1)
        
        # Layers button (bottom)
        self.layers_btn = pygame.Rect(10, y_layers, 60, button_height)
        color = COLOR_BLACK if self.show_layer_menu else COLOR_UI_LIGHT
        pygame.draw.rect(screen, color, self.layers_btn, border_radius=8)
        # Draw 3 horizontal lines
        line_color = COLOR_WHITE if self.show_layer_menu else COLOR_BLACK
        center_x, center_y = self.layers_btn.centerx, self.layers_btn.centery
        pygame.draw.line(screen, line_color, (center_x - 12, center_y - 8), (center_x + 12, center_y - 8), 2)
        pygame.draw.line(screen, line_color, (center_x - 12, center_y), (center_x + 12, center_y), 2)
        pygame.draw.line(screen, line_color, (center_x - 12, center_y + 8), (center_x + 12, center_y + 8), 2)
        
        # Draw the menus on top of everything
        self.draw_template_menu(screen)
        self.draw_layer_menu(screen, notebook)
        
        # Draw spell check suggestions panel
        if self.show_suggestions and self.current_suggestions:
            self.draw_suggestions_panel(screen)
        
        # Draw search panel or definition
        if self.show_definition and self.current_word_definition:
            self.draw_word_definition(screen, self.current_word_definition['word'], 
                                     self.current_word_definition)
        else:
            self.draw_search_panel(screen, self.extracted_words)
        
        # Scroll indicator if scrolled
        if self.scroll_offset > 0:
            scroll_text = self.font_m.render("^", True, COLOR_UI_DARK)
            screen.blit(scroll_text, (35, DISPLAY_HEIGHT - 490))
    
    def handle_click(self, pos):
        """
        Handle click events on notepad screen
        Returns: (action, data) tuple
        """
        # Check if clicking on menus first
        if self.show_template_menu and hasattr(self, 'template_options'):
            for rect, template_name in self.template_options:
                if rect.collidepoint(pos):
                    return ('select_template', template_name)
        
        if self.show_layer_menu:
            # Check layer menu clicks first (higher priority)
            if hasattr(self, 'add_layer_btn') and self.add_layer_btn.collidepoint(pos):
                return ('add_layer', None)
            
            # Check visibility toggles
            if hasattr(self, 'layer_rects'):
                for rect, vis_rect, layer_idx in self.layer_rects:
                    if vis_rect.collidepoint(pos):
                        return ('toggle_layer_visibility', layer_idx)
                    elif rect.collidepoint(pos):
                        return ('select_layer', layer_idx)
            
            # Check up/down buttons
            if hasattr(self, 'layer_up_btns'):
                for btn, idx in self.layer_up_btns:
                    if btn.collidepoint(pos):
                        return ('move_layer_up', idx)
            
            if hasattr(self, 'layer_down_btns'):
                for btn, idx in self.layer_down_btns:
                    if btn.collidepoint(pos):
                        return ('move_layer_down', idx)
            
            # Check merge button
            if hasattr(self, 'merge_all_btn') and self.merge_all_btn.collidepoint(pos):
                return ('merge_all_layers', None)
            
            # If clicked anywhere else in menu, do nothing (don't close)
            return (None, None)
        
        if self.show_search_panel:
            if hasattr(self, 'close_search_btn') and self.close_search_btn.collidepoint(pos):
                return ('close_search', None)
            # Check if clicking on definition back button
            if self.show_definition and hasattr(self, 'dict_back_btn') and self.dict_back_btn.collidepoint(pos):
                return ('back_to_word_list', None)
            # Check if clicking on word buttons
            if not self.show_definition and hasattr(self, 'word_btns'):
                for rect, word in self.word_btns:
                    if rect.collidepoint(pos):
                        return ('search_word', word)
        
        # Spell check suggestions panel
        if self.show_suggestions:
            if hasattr(self, 'close_suggestions_btn') and self.close_suggestions_btn.collidepoint(pos):
                return ('close_suggestions', None)
            if hasattr(self, 'ignore_all_btn') and self.ignore_all_btn.collidepoint(pos):
                return ('ignore_all_spelling', None)
            if hasattr(self, 'recheck_btn') and self.recheck_btn.collidepoint(pos):
                return ('recheck_spelling', None)
            if hasattr(self, 'suggestion_btns'):
                for btn, original_word, suggestion, error_idx in self.suggestion_btns:
                    if btn.collidepoint(pos):
                        return ('accept_suggestion', (original_word, suggestion, error_idx))
            # Don't close panel if clicked inside
            return (None, None)
        
        # Back button
        if self.back_btn and self.back_btn.collidepoint(pos):
            return ('back', None)
        
        # Tool selection
        if self.pen_btn and self.pen_btn.collidepoint(pos):
            return ('select_pen', None)
        
        if self.highlighter_btn and self.highlighter_btn.collidepoint(pos):
            return ('select_highlighter', None)
        
        if self.eraser_btn and self.eraser_btn.collidepoint(pos):
            return ('select_eraser', None)
        
        # Size adjustment
        if self.size_up and self.size_up.collidepoint(pos):
            return ('increase_size', None)
        
        if self.size_down and self.size_down.collidepoint(pos):
            return ('decrease_size', None)
        
        # Search button
        if hasattr(self, 'search_btn') and self.search_btn and self.search_btn.collidepoint(pos):
            print(f"[DEBUG] Search button clicked at {pos}")
            return ('toggle_search', None)
        
        # Export PDF button
        if hasattr(self, 'export_pdf_btn') and self.export_pdf_btn and self.export_pdf_btn.collidepoint(pos):
            return ('export_pdf', None)
        
        # Save to DB button
        if hasattr(self, 'save_db_btn') and self.save_db_btn and self.save_db_btn.collidepoint(pos):
            return ('save_to_db', None)
        
        # Convert to text button
        if hasattr(self, 'convert_btn') and self.convert_btn and self.convert_btn.collidepoint(pos):
            return ('convert_to_text', None)
        
        # Spell check button
        if hasattr(self, 'spell_check_btn') and self.spell_check_btn and self.spell_check_btn.collidepoint(pos):
            return ('check_spelling', None)
        
        # Template button
        if hasattr(self, 'template_btn') and self.template_btn and self.template_btn.collidepoint(pos):
            return ('toggle_template_menu', None)
        
        # Layers button
        if hasattr(self, 'layers_btn') and self.layers_btn and self.layers_btn.collidepoint(pos):
            return ('toggle_layer_menu', None)
        
        # Drawing area (right of toolbar, below status bar)
        if pos[0] > self.toolbar_width and pos[1] > self.toolbar_start_y:
            # Adjust position for canvas coordinates (account for scroll and toolbar)
            canvas_x = pos[0] - self.toolbar_width
            canvas_y = pos[1] - self.toolbar_start_y + self.scroll_offset
            return ('start_drawing', (canvas_x, canvas_y))
        
        return (None, None)
    
    def handle_scroll(self, y_delta):
        """Handle scroll events"""
        # Scroll up (negative delta) or down (positive delta)
        self.scroll_offset -= y_delta * 30  # Multiply for sensitivity
        
        # Clamp scroll to valid range
        max_scroll = self.canvas_height - (DISPLAY_HEIGHT - self.toolbar_start_y)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
        
        # Expand canvas if we're near the bottom
        if self.scroll_offset > self.canvas_height - DISPLAY_HEIGHT:
            self.canvas_height += DISPLAY_HEIGHT
    
    def adjust_pos_for_canvas(self, pos):
        """Adjust mouse position to canvas coordinates"""
        if pos[0] < self.toolbar_width or pos[1] < self.toolbar_start_y:
            return None
        
        # Try without offset compensation
        canvas_pos = (pos[0] - self.toolbar_width, pos[1] - self.toolbar_start_y + self.scroll_offset)
        return canvas_pos
    
    def select_tool(self, tool):
        """Select pen or eraser tool"""
        self.tool = tool
    
    def adjust_size(self, increase):
        """Adjust the size of current tool"""
        if self.tool == 'pen':
            if increase:
                self.pen_size = min(40, self.pen_size + 2)
            else:
                self.pen_size = max(1, self.pen_size - 2)
        elif self.tool == 'highlighter':
            if increase:
                self.highlighter_size = min(60, self.highlighter_size + 5)
            else:
                self.highlighter_size = max(10, self.highlighter_size - 5)
        else:  # eraser
            if increase:
                self.eraser_size = min(100, self.eraser_size + 5)
            else:
                self.eraser_size = max(5, self.eraser_size - 5)
    
    def start_drawing(self, pos):
        """Start a drawing stroke"""
        self.drawing = True
        # Convert to canvas position immediately
        canvas_pos = self.adjust_pos_for_canvas(pos)
        if canvas_pos:
            self.last_pos = canvas_pos
            # Mark that this is the first point (don't draw line yet)
            self.first_point = True
        else:
            self.last_pos = None
            self.first_point = False
    
    def stop_drawing(self):
        """Stop drawing"""
        self.drawing = False
    
    def draw_stroke(self, surface, pos):
        """Draw a stroke on the surface from last_pos to pos"""
        if not self.drawing or not self.last_pos:
            return
        
        # Convert screen position to canvas position
        canvas_pos = self.adjust_pos_for_canvas(pos)
        if not canvas_pos:
            return
        
        # If this is the first point, just draw a dot/circle at that position
        if self.first_point:
            self.first_point = False
            if self.tool == 'pen':
                # Draw a small circle at the starting point
                pygame.draw.circle(surface, COLOR_BLACK, canvas_pos, self.pen_size // 2)
            elif self.tool == 'highlighter':
                # Draw a semi-transparent circle
                temp_surface = pygame.Surface((self.highlighter_size * 2, self.highlighter_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(temp_surface, (180, 180, 180, 100), 
                                 (self.highlighter_size, self.highlighter_size), 
                                 self.highlighter_size // 2)
                surface.blit(temp_surface, (canvas_pos[0] - self.highlighter_size, 
                                           canvas_pos[1] - self.highlighter_size))
            else:  # eraser
                pygame.draw.circle(surface, (0, 0, 0, 0), canvas_pos, self.eraser_size)
            
            self.last_pos = canvas_pos
            return
        
        # Draw from last position to current position (normal stroke)
        if self.tool == 'pen':
            pygame.draw.line(
                surface,
                COLOR_BLACK,
                self.last_pos,
                canvas_pos,
                self.pen_size
            )
        elif self.tool == 'highlighter':
            # Light grey highlighter for grayscale display (like real highlighting)
            # Create a temporary surface for transparency
            temp_surface = pygame.Surface((abs(canvas_pos[0] - self.last_pos[0]) + self.highlighter_size,
                                          abs(canvas_pos[1] - self.last_pos[1]) + self.highlighter_size),
                                         pygame.SRCALPHA)
            # Calculate relative positions on temp surface
            offset_x = min(self.last_pos[0], canvas_pos[0]) - self.highlighter_size//2
            offset_y = min(self.last_pos[1], canvas_pos[1]) - self.highlighter_size//2
            rel_last = (self.last_pos[0] - offset_x, self.last_pos[1] - offset_y)
            rel_pos = (canvas_pos[0] - offset_x, canvas_pos[1] - offset_y)
            
            # Draw semi-transparent light grey line (grayscale highlighter)
            pygame.draw.line(
                temp_surface,
                (180, 180, 180, 100),  # Light grey with alpha=100 (semi-transparent)
                rel_last,
                rel_pos,
                self.highlighter_size
            )
            # Blit to main surface
            surface.blit(temp_surface, (offset_x, offset_y))
        else:  # eraser
            pygame.draw.circle(
                surface,
                (0, 0, 0, 0),
                canvas_pos,
                self.eraser_size
            )
        
        self.last_pos = canvas_pos

    def draw_template_menu(self, screen):
        """Draw template selection menu"""
        if not self.show_template_menu:
            return
        
        from templates import TEMPLATES
        
        # Menu panel
        panel_width = 200
        panel_height = len(TEMPLATES) * 50 + 40
        panel_x = self.toolbar_width + 20
        panel_y = 100
        
        panel = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, COLOR_WHITE, panel, border_radius=10)
        pygame.draw.rect(screen, COLOR_UI_DARK, panel, 2, border_radius=10)
        
        # Title
        title = self.font_m.render("Templates", True, COLOR_BLACK)
        screen.blit(title, (panel_x + 10, panel_y + 10))
        
        # Template options
        y = panel_y + 40
        self.template_options = []
        for template in TEMPLATES:
            rect = pygame.Rect(panel_x + 10, y, panel_width - 20, 40)
            pygame.draw.rect(screen, COLOR_UI_LIGHT, rect, border_radius=5)
            
            name_text = self.font_s.render(template.name, True, COLOR_BLACK)
            screen.blit(name_text, (rect.x + 10, rect.y + 12))
            
            self.template_options.append((rect, template.name))
            y += 50
    
    def draw_layer_menu(self, screen, notebook):
        """Draw enhanced layer management menu"""
        if not self.show_layer_menu:
            return
        
        # Menu panel
        panel_width = 280
        panel_height = min(550, len(notebook.layers) * 70 + 150)
        panel_x = self.toolbar_width + 20
        panel_y = 60
        
        panel = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        # Shadow
        shadow = panel.copy()
        shadow.x += 3
        shadow.y += 3
        pygame.draw.rect(screen, (0, 0, 0, 30), shadow, border_radius=15)
        
        # Panel background
        pygame.draw.rect(screen, COLOR_WHITE, panel, border_radius=15)
        pygame.draw.rect(screen, COLOR_GRAY_300, panel, 2, border_radius=15)
        
        # Title
        title = self.font_l.render("Layers", True, COLOR_PRIMARY)
        screen.blit(title, (panel_x + 20, panel_y + 15))
        
        # Add layer button
        self.add_layer_btn = pygame.Rect(panel_x + panel_width - 100, panel_y + 12, 85, 35)
        pygame.draw.rect(screen, COLOR_SUCCESS, self.add_layer_btn, border_radius=8)
        add_text = self.font_s.render("+ Add", True, COLOR_WHITE)
        screen.blit(add_text, (self.add_layer_btn.centerx - 20, self.add_layer_btn.centery - 8))
        
        # Layer list
        y = panel_y + 65
        self.layer_rects = []
        self.layer_up_btns = []
        self.layer_down_btns = []
        self.layer_duplicate_btns = []
        self.layer_merge_btns = []
        
        for i, layer in enumerate(notebook.layers):
            if y > panel_y + panel_height - 80:
                break
            
            rect = pygame.Rect(panel_x + 15, y, panel_width - 30, 60)
            
            # Active layer highlight
            color = COLOR_SECONDARY if i == 0 else COLOR_GRAY_100
            pygame.draw.rect(screen, color, rect, border_radius=10)
            
            # Visibility toggle
            vis_size = 24
            vis_rect = pygame.Rect(rect.x + 10, rect.centery - vis_size//2, vis_size, vis_size)
            pygame.draw.rect(screen, COLOR_WHITE, vis_rect, border_radius=5)
            if layer.visible:
                # Eye icon (visible)
                pygame.draw.circle(screen, COLOR_PRIMARY, vis_rect.center, 6, 2)
                pygame.draw.circle(screen, COLOR_PRIMARY, vis_rect.center, 3)
            else:
                # Crossed eye (hidden)
                pygame.draw.line(screen, COLOR_GRAY_400,
                               (vis_rect.x + 3, vis_rect.y + 3),
                               (vis_rect.right - 3, vis_rect.bottom - 3), 2)
            
            # Layer name and info
            name_text = f"Layer {i+1}"
            name_color = COLOR_WHITE if i == 0 else COLOR_GRAY_800
            name_surf = self.font_m.render(name_text, True, name_color)
            screen.blit(name_surf, (rect.x + 45, rect.y + 12))
            
            template_text = f"({layer.template_name})"
            template_color = COLOR_GRAY_300 if i == 0 else COLOR_GRAY_500
            template_surf = self.font_s.render(template_text, True, template_color)
            screen.blit(template_surf, (rect.x + 45, rect.y + 36))
            
            # Action buttons (small)
            btn_size = 24
            btn_x = rect.right - btn_size - 10
            
            # Up arrow (move layer up)
            if i > 0:
                up_btn = pygame.Rect(btn_x, rect.y + 6, btn_size, btn_size)
                pygame.draw.rect(screen, COLOR_ACCENT, up_btn, border_radius=5)
                # Arrow up
                points = [
                    (up_btn.centerx, up_btn.y + 8),
                    (up_btn.x + 6, up_btn.centery + 2),
                    (up_btn.right - 6, up_btn.centery + 2)
                ]
                pygame.draw.polygon(screen, COLOR_WHITE, points)
                self.layer_up_btns.append((up_btn, i))
            
            # Down arrow (move layer down)
            if i < len(notebook.layers) - 1:
                down_btn = pygame.Rect(btn_x, rect.bottom - btn_size - 6, btn_size, btn_size)
                pygame.draw.rect(screen, COLOR_ACCENT, down_btn, border_radius=5)
                # Arrow down
                points = [
                    (down_btn.centerx, down_btn.bottom - 8),
                    (down_btn.x + 6, down_btn.centery - 2),
                    (down_btn.right - 6, down_btn.centery - 2)
                ]
                pygame.draw.polygon(screen, COLOR_WHITE, points)
                self.layer_down_btns.append((down_btn, i))
            
            self.layer_rects.append((rect, vis_rect, i))
            y += 65
        
        # Layer operations bar at bottom
        ops_y = panel_y + panel_height - 50
        ops_rect = pygame.Rect(panel_x + 15, ops_y, panel_width - 30, 40)
        pygame.draw.rect(screen, COLOR_GRAY_100, ops_rect, border_radius=8)
        
        # Merge all visible button
        merge_btn = pygame.Rect(ops_rect.x + 10, ops_rect.y + 8, 120, 24)
        pygame.draw.rect(screen, COLOR_WARNING, merge_btn, border_radius=5)
        merge_text = self.font_s.render("Merge All", True, COLOR_WHITE)
        screen.blit(merge_text, (merge_btn.centerx - 35, merge_btn.centery - 7))
        self.merge_all_btn = merge_btn
    
    def draw_suggestions_panel(self, screen):
        """Draw spell check suggestions panel"""
        # Panel dimensions
        panel_width = 300
        panel_height = 400
        panel_x = (600 - panel_width) // 2  # Center horizontally
        panel_y = 100
        
        # Background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, (240, 240, 240), panel_rect, border_radius=10)
        pygame.draw.rect(screen, (150, 150, 150), panel_rect, 2, border_radius=10)
        
        # Title
        title = self.font_m.render("Spelling Suggestions", True, COLOR_BLACK)
        screen.blit(title, (panel_x + 15, panel_y + 15))
        
        # Close button
        close_btn = pygame.Rect(panel_x + panel_width - 35, panel_y + 10, 25, 25)
        pygame.draw.rect(screen, (200, 200, 200), close_btn, border_radius=5)
        pygame.draw.line(screen, COLOR_BLACK, (close_btn.left + 7, close_btn.top + 7),
                        (close_btn.right - 7, close_btn.bottom - 7), 2)
        pygame.draw.line(screen, COLOR_BLACK, (close_btn.right - 7, close_btn.top + 7),
                        (close_btn.left + 7, close_btn.bottom - 7), 2)
        self.close_suggestions_btn = close_btn
        
        # Display suggestions
        y = panel_y + 55
        self.suggestion_btns = []
        
        for i, error in enumerate(self.current_suggestions[:5]):  # Show max 5 errors
            # Error word
            word_text = self.font_m.render(f'"{error["word"]}"', True, (150, 0, 0))
            screen.blit(word_text, (panel_x + 20, y))
            y += 30
            
            # Show top 3 suggestions
            if error.get('suggestions'):
                for j, suggestion in enumerate(error['suggestions'][:3]):
                    # Suggestion button
                    btn = pygame.Rect(panel_x + 30, y, panel_width - 60, 30)
                    pygame.draw.rect(screen, (220, 220, 220), btn, border_radius=5)
                    pygame.draw.rect(screen, (180, 180, 180), btn, 1, border_radius=5)
                    
                    # Suggestion text
                    sugg_text = self.font_s.render(suggestion, True, COLOR_BLACK)
                    screen.blit(sugg_text, (btn.x + 10, btn.centery - 8))
                    
                    # Store button for click detection
                    self.suggestion_btns.append((btn, error['word'], suggestion, i))
                    y += 35
            else:
                no_sugg = self.font_s.render("No suggestions", True, (100, 100, 100))
                screen.blit(no_sugg, (panel_x + 30, y))
                y += 30
            
            y += 15  # Space between errors
            
            if y > panel_y + panel_height - 60:
                break  # Don't overflow panel
        
        # Bottom buttons
        btn_y = panel_y + panel_height - 45
        
        # "Ignore All" button
        ignore_btn = pygame.Rect(panel_x + 20, btn_y, 120, 30)
        pygame.draw.rect(screen, (180, 180, 180), ignore_btn, border_radius=5)
        ignore_text = self.font_s.render("Ignore All", True, COLOR_BLACK)
        screen.blit(ignore_text, (ignore_btn.centerx - 35, ignore_btn.centery - 8))
        self.ignore_all_btn = ignore_btn
        
        # "Re-check" button  
        recheck_btn = pygame.Rect(panel_x + 160, btn_y, 120, 30)
        pygame.draw.rect(screen, (100, 100, 100), recheck_btn, border_radius=5)
        recheck_text = self.font_s.render("Re-check", True, COLOR_WHITE)
        screen.blit(recheck_text, (recheck_btn.centerx - 32, recheck_btn.centery - 8))
        self.recheck_btn = recheck_btn
    
    def draw_search_panel(self, screen, extracted_words=None):
        """Draw word search/dictionary panel showing words from notebook"""
        if not self.show_search_panel:
            return
        
        # Panel
        panel_width = 350
        panel_height = 500
        panel_x = (DISPLAY_WIDTH - panel_width) // 2
        panel_y = 80
        
        panel = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, COLOR_WHITE, panel, border_radius=10)
        pygame.draw.rect(screen, COLOR_UI_DARK, panel, 2, border_radius=10)
        
        # Title
        title = self.font_l.render("Word Search", True, COLOR_BLACK)
        screen.blit(title, (panel_x + 20, panel_y + 15))
        
        # Close button
        self.close_search_btn = pygame.Rect(panel_x + panel_width - 40, panel_y + 10, 30, 30)
        pygame.draw.rect(screen, COLOR_UI_LIGHT, self.close_search_btn, border_radius=5)
        close_text = self.font_l.render("×", True, COLOR_BLACK)
        screen.blit(close_text, (self.close_search_btn.centerx - 8, self.close_search_btn.centery - 12))
        
        # Show extracted words or instructions
        if extracted_words and len(extracted_words) > 0:
            # Instructions
            inst = self.font_s.render("Click a word to see its definition:", True, COLOR_BLACK)
            screen.blit(inst, (panel_x + 20, panel_y + 60))
            
            # Word buttons
            y = panel_y + 100
            self.word_btns = []
            
            for i, word in enumerate(extracted_words[:10]):  # Show max 10 words
                word_rect = pygame.Rect(panel_x + 20, y, panel_width - 40, 35)
                pygame.draw.rect(screen, COLOR_UI_LIGHT, word_rect, border_radius=5)
                
                word_text = self.font_m.render(word, True, COLOR_BLACK)
                screen.blit(word_text, (word_rect.x + 10, word_rect.y + 8))
                
                self.word_btns.append((word_rect, word))
                y += 40
        else:
            # No words extracted yet
            inst1 = self.font_m.render("Extracting text from your", True, COLOR_BLACK)
            inst2 = self.font_m.render("notebook...", True, COLOR_BLACK)
            screen.blit(inst1, (panel_x + 60, panel_y + 200))
            screen.blit(inst2, (panel_x + 100, panel_y + 230))
    
    def draw_word_definition(self, screen, word, definition_data):
        """Draw word definition panel"""
        # Panel
        panel_width = 400
        panel_height = 450
        panel_x = (DISPLAY_WIDTH - panel_width) // 2
        panel_y = 80
        
        panel = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, COLOR_WHITE, panel, border_radius=10)
        pygame.draw.rect(screen, COLOR_UI_DARK, panel, 2, border_radius=10)
        
        # Back button
        self.dict_back_btn = pygame.Rect(panel_x + 10, panel_y + 10, 60, 30)
        pygame.draw.rect(screen, COLOR_UI_LIGHT, self.dict_back_btn, border_radius=5)
        back_text = self.font_s.render("< Back", True, COLOR_BLACK)
        screen.blit(back_text, (self.dict_back_btn.x + 8, self.dict_back_btn.y + 8))
        
        # Word title
        word_title = self.font_l.render(word.upper(), True, COLOR_BLACK)
        screen.blit(word_title, (panel_x + 20, panel_y + 50))
        
        # Content area
        y = panel_y + 100
        
        if definition_data.get('found'):
            # Phonetic
            if definition_data.get('phonetic'):
                phonetic_text = self.font_s.render(definition_data['phonetic'], True, COLOR_UI_DARK)
                screen.blit(phonetic_text, (panel_x + 20, y))
                y += 30
            
            # Definitions
            for i, defn in enumerate(definition_data.get('definitions', [])[:3]):
                # Part of speech
                pos_text = self.font_m.render(f"{defn['pos']}", True, COLOR_ACCENT)
                screen.blit(pos_text, (panel_x + 20, y))
                y += 25
                
                # Definition (word wrap)
                def_lines = self._wrap_text(defn['definition'], panel_width - 60, self.font_s)
                for line in def_lines[:3]:  # Max 3 lines per definition
                    def_surf = self.font_s.render(line, True, COLOR_BLACK)
                    screen.blit(def_surf, (panel_x + 30, y))
                    y += 20
                y += 10
            
            # Synonyms
            if definition_data.get('synonyms'):
                syn_label = self.font_m.render("Synonyms:", True, COLOR_BLACK)
                screen.blit(syn_label, (panel_x + 20, y))
                y += 25
                
                syn_text = ", ".join(definition_data['synonyms'][:5])
                syn_lines = self._wrap_text(syn_text, panel_width - 60, self.font_s)
                for line in syn_lines[:2]:
                    syn_surf = self.font_s.render(line, True, COLOR_UI_DARK)
                    screen.blit(syn_surf, (panel_x + 30, y))
                    y += 20
        else:
            # Not found
            error_text = self.font_m.render("Word not found in dictionary", True, COLOR_BLACK)
            screen.blit(error_text, (panel_x + 60, y))
    
    def _wrap_text(self, text, max_width, font):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines