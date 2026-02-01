"""
Home view for ABook application - displays folders and notebooks
Modern grayscale icons for Notes, Books, and Tests
"""
import pygame
from config import *


def draw_modern_notes_icon(screen, x, y, size=60):
    """Draw modern notebook icon - clean lines"""
    # Notebook body (rounded rectangle)
    body_rect = pygame.Rect(x, y, size, int(size * 1.2))
    pygame.draw.rect(screen, (220, 220, 220), body_rect, border_radius=8)
    pygame.draw.rect(screen, (140, 140, 140), body_rect, 2, border_radius=8)
    
    # Spiral binding (left side dots)
    for i in range(5):
        dot_y = y + 15 + i * (int(size * 1.2) - 30) // 4
        pygame.draw.circle(screen, (140, 140, 140), (x + 8, dot_y), 3)
    
    # Lined paper effect (horizontal lines)
    for i in range(4):
        line_y = y + 20 + i * 18
        pygame.draw.line(screen, (180, 180, 180), 
                        (x + 15, line_y), (x + size - 8, line_y), 1)


def draw_modern_books_icon(screen, x, y, size=60):
    """Draw modern book icon - stacked books"""
    # Book 1 (back)
    book1 = pygame.Rect(x + 8, y + 10, size - 16, int(size * 1.0))
    pygame.draw.rect(screen, (200, 200, 200), book1, border_radius=4)
    pygame.draw.rect(screen, (140, 140, 140), book1, 2, border_radius=4)
    
    # Book 2 (front, slightly offset)
    book2 = pygame.Rect(x, y + 20, size - 16, int(size * 1.0))
    pygame.draw.rect(screen, (230, 230, 230), book2, border_radius=4)
    pygame.draw.rect(screen, (140, 140, 140), book2, 2, border_radius=4)
    
    # Pages indication (small lines on side)
    for i in range(3):
        page_y = book2.y + 10 + i * 12
        pygame.draw.line(screen, (180, 180, 180),
                        (book2.right, page_y),
                        (book2.right + 3, page_y), 1)
    
    # Bookmark ribbon
    pygame.draw.rect(screen, (160, 160, 160), 
                    (book2.x + size//2 - 8, book2.y - 5, 8, 15))


def draw_modern_test_icon(screen, x, y, size=60):
    """Draw modern test/exam icon - clipboard with checkmarks"""
    # Clipboard body
    clipboard = pygame.Rect(x + 5, y + 8, size - 10, int(size * 1.1))
    pygame.draw.rect(screen, (230, 230, 230), clipboard, border_radius=6)
    pygame.draw.rect(screen, (140, 140, 140), clipboard, 2, border_radius=6)
    
    # Clip at top
    clip_rect = pygame.Rect(x + size//2 - 8, y, 16, 12)
    pygame.draw.rect(screen, (180, 180, 180), clip_rect, border_radius=3)
    pygame.draw.rect(screen, (140, 140, 140), clip_rect, 2, border_radius=3)
    
    # Checkboxes with checkmarks
    checkbox_size = 10
    for i in range(3):
        box_x = x + 15
        box_y = y + 25 + i * 18
        
        # Checkbox
        checkbox = pygame.Rect(box_x, box_y, checkbox_size, checkbox_size)
        pygame.draw.rect(screen, (255, 255, 255), checkbox)
        pygame.draw.rect(screen, (140, 140, 140), checkbox, 1)
        
        # Checkmark
        if i < 2:  # First two checked
            pygame.draw.line(screen, (100, 100, 100),
                           (box_x + 2, box_y + 5),
                           (box_x + 4, box_y + 8), 2)
            pygame.draw.line(screen, (100, 100, 100),
                           (box_x + 4, box_y + 8),
                           (box_x + 8, box_y + 2), 2)
        
        # Line next to checkbox
        pygame.draw.line(screen, (180, 180, 180),
                        (box_x + 15, box_y + 5),
                        (box_x + size - 25, box_y + 5), 1)


class HomeView:
    """Home screen view with folder-based navigation"""
    def __init__(self, fonts):
        self.font_s, self.font_m, self.font_l = fonts
        self.current_folder = None  # None = main view, 'notes', 'books', or 'tests'
        self.folder_rects = []
        self.nb_rects = []
        self.back_btn = None
        self.new_btn = None
    
    def draw_main_view(self, screen):
        """Draw the main folder view - FOR PORTRAIT 600x1024"""
        screen.fill(COLOR_WHITE)
        
        # Status bar
        self.draw_status_bar(screen)
        
        # Title
        title = self.font_l.render("ABook", True, COLOR_BLACK)
        title_x = (600 - title.get_width()) // 2
        screen.blit(title, (title_x, 50))
        
        # Folders - 3 folders vertically stacked
        self.folder_rects = []
        folders = [
            ('notes', 'Notes', draw_modern_notes_icon),
            ('books', 'Books', draw_modern_books_icon),
            ('tests', 'Tests', draw_modern_test_icon)  # NEW!
        ]
        
        # Start from top with good margin
        y_start = 130
        card_height = 200
        card_spacing = 30
        
        for i, (folder_id, label, icon_func) in enumerate(folders):
            rect = pygame.Rect(
                50,  # Left margin for portrait
                y_start + i * (card_height + card_spacing),
                500,  # Width for portrait (600 - 100 margin)
                card_height
            )
            
            # Draw folder card - GRAYSCALE
            pygame.draw.rect(screen, (245, 245, 245), rect, border_radius=15)  # Light grey
            pygame.draw.rect(screen, (160, 160, 160), rect, 2, border_radius=15)  # Grey border
            
            # Draw modern icon (centered in card)
            icon_size = 70
            icon_x = rect.centerx - icon_size // 2
            icon_y = rect.y + 40
            icon_func(screen, icon_x, icon_y, icon_size)
            
            # Draw folder label below icon
            label_text = self.font_l.render(label, True, COLOR_BLACK)
            label_x = rect.centerx - label_text.get_width() // 2
            label_y = rect.y + 140
            screen.blit(label_text, (label_x, label_y))
            
            self.folder_rects.append((rect, folder_id))
    
    def draw_folder_contents(self, screen, notebooks, keyboard, renaming_idx, temp_name):
        """Draw the contents of a folder (notebooks)"""
        screen.fill(COLOR_WHITE)
        self.draw_status_bar(screen)
        
        # Back button - GRAYSCALE
        self.back_btn = pygame.Rect(10, 40, 70, 40)
        pygame.draw.rect(screen, (200, 200, 200), self.back_btn, border_radius=20)  # Light grey
        back_text = self.font_s.render("< Back", True, COLOR_BLACK)
        screen.blit(back_text, (20, 50))
        
        # Folder title
        folder_names = {'notes': 'Notes', 'books': 'Books', 'tests': 'Tests'}
        title = self.font_l.render(folder_names.get(self.current_folder, 'Files'), True, COLOR_BLACK)
        screen.blit(title, (100, 45))
        
        # New notebook button - FOR PORTRAIT - GRAYSCALE
        self.new_btn = pygame.Rect(450, 45, 120, 40)  # Portrait positioning
        pygame.draw.rect(screen, (100, 100, 100), self.new_btn, border_radius=20)  # Dark grey
        btn_text = self.font_s.render("+ New", True, COLOR_WHITE)
        screen.blit(btn_text, (self.new_btn.centerx - 25, self.new_btn.centery - 10))
        
        # Filter notebooks by folder
        filtered_notebooks = [(i, nb) for i, nb in enumerate(notebooks) 
                             if nb.folder == self.current_folder]
        
        # Notebook list - STACKED for portrait
        self.nb_rects = []
        for display_idx, (actual_idx, nb) in enumerate(filtered_notebooks):
            # Stack vertically for portrait
            rect = pygame.Rect(30, 120 + display_idx * 160, 540, 145)
            
            # Draw notebook card - GRAYSCALE
            pygame.draw.rect(screen, (245, 245, 245), rect, border_radius=10)  # Very light grey
            pygame.draw.rect(screen, (180, 180, 180), rect, 2, border_radius=10)  # Grey border
            
            # Draw notebook icon/preview area with enhanced icon
            icon_rect = pygame.Rect(rect.x + 10, rect.y + 10, 80, 90)
            
            # Use appropriate icon based on folder
            if self.current_folder == 'notes':
                draw_modern_notes_icon(screen, icon_rect.x, icon_rect.y, 70)
            elif self.current_folder == 'books':
                draw_modern_books_icon(screen, icon_rect.x, icon_rect.y, 70)
            else:  # tests
                draw_modern_test_icon(screen, icon_rect.x, icon_rect.y, 70)
            
            # Draw notebook name area
            name_rect = pygame.Rect(rect.x + 100, rect.y + 30, 430, 70)
            
            if renaming_idx == actual_idx:
                # Editing mode
                pygame.draw.rect(screen, COLOR_WHITE, name_rect, border_radius=5)
                pygame.draw.rect(screen, COLOR_BLACK, name_rect, 1, border_radius=5)
                txt = self.font_m.render(temp_name + "|", True, COLOR_BLACK)
            else:
                # Display mode
                txt = self.font_m.render(nb.name, True, COLOR_BLACK)
            
            screen.blit(txt, (name_rect.x + 10, name_rect.y + 20))
            
            # Add page count indicator
            page_count = len(nb.layers)
            pages_text = self.font_s.render(f"{page_count} {'page' if page_count == 1 else 'pages'}", True, (120, 120, 120))
            screen.blit(pages_text, (name_rect.x + 10, name_rect.y + 48))
            
            self.nb_rects.append((rect, name_rect, actual_idx))
        
        # Show message if no notebooks
        if not filtered_notebooks:
            msg_lines = [
                "No items yet.",
                "Tap + New to create one."
            ]
            y = 400
            for line in msg_lines:
                msg = self.font_m.render(line, True, (120, 120, 120))
                msg_x = (600 - msg.get_width()) // 2
                screen.blit(msg, (msg_x, y))
                y += 35
        
        # Draw keyboard if visible
        keyboard.draw(screen)
    
    def draw_status_bar(self, screen):
        """Draw simple status bar"""
        # Status bar background
        bar_rect = pygame.Rect(0, 0, 600, 25)
        pygame.draw.rect(screen, (30, 30, 50), bar_rect)
        
        # Time (center)
        import datetime
        time_str = datetime.datetime.now().strftime("%H:%M")
        time_surface = self.font_s.render(time_str, True, COLOR_WHITE)
        time_x = (600 - time_surface.get_width()) // 2
        screen.blit(time_surface, (time_x, 5))
        
        # WiFi icon (left)
        wifi_text = self.font_s.render("WiFi", True, COLOR_WHITE)
        screen.blit(wifi_text, (10, 5))
        
        # Battery (right)
        battery_text = self.font_s.render("85%", True, COLOR_WHITE)
        screen.blit(battery_text, (545, 5))
    
    def draw(self, screen, notebooks, keyboard, renaming_idx, temp_name):
        """Draw the appropriate view based on current state"""
        if self.current_folder is None:
            self.draw_main_view(screen)
        else:
            self.draw_folder_contents(screen, notebooks, keyboard, renaming_idx, temp_name)
    
    def handle_click(self, pos, notebooks, keyboard, renaming_idx, temp_name):
        """
        Handle click events on home screen
        Returns: (action, data) tuple
        """
        # Check keyboard clicks first (when in folder view)
        if self.current_folder and keyboard.visible:
            for rect, key in keyboard.key_rects:
                if rect.collidepoint(pos):
                    if key == 'Done':
                        return ('rename_done', temp_name)
                    elif key == '⌫':
                        return ('backspace', None)
                    elif key == 'Space':
                        return ('add_char', ' ')
                    else:
                        return ('add_char', key)
        
        # Main view - folder selection
        if self.current_folder is None:
            for rect, folder_id in self.folder_rects:
                if rect.collidepoint(pos):
                    return ('open_folder', folder_id)
        
        # Folder view
        else:
            # Back button
            if self.back_btn and self.back_btn.collidepoint(pos):
                return ('back_to_folders', None)
            
            # New button
            if self.new_btn and self.new_btn.collidepoint(pos):
                return ('new_notebook', self.current_folder)
            
            # Notebook clicks
            for rect, name_rect, idx in self.nb_rects:
                if name_rect.collidepoint(pos):
                    return ('start_rename', idx)
                elif rect.collidepoint(pos):
                    return ('open_notebook', idx)
        
        return (None, None)
    
    def set_folder(self, folder):
        """Set the current folder view"""
        self.current_folder = folder
    
    def back_to_main(self):
        """Return to main folder view"""
        self.current_folder = None