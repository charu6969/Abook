"""
Home view for ABook application - displays folders and notebooks
"""
import pygame
from config import *
from ui_components import draw_status_bar


class HomeView:
    """Home screen view with folder-based navigation"""
    def __init__(self, fonts):
        self.font_s, self.font_m, self.font_l = fonts
        self.current_folder = None  # None = main view, 'notes', 'books', or 'test'
        self.folder_rects = []
        self.nb_rects = []
        self.back_btn = None
        self.new_btn = None
    
    def draw_folder_icon(self, screen, x, y, size=60):
        """Draw a folder icon - GRAYSCALE"""
        # Folder tab (dark grey)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, size//2, size//4), border_radius=3)
        # Folder body (light grey)
        pygame.draw.rect(screen, (200, 200, 200), (x, y + size//4, size, size*2//3), border_radius=5)
        pygame.draw.rect(screen, (80, 80, 80), (x, y + size//4, size, size*2//3), 2, border_radius=5)
    
    def draw_main_view(self, screen):
        """Draw the main folder view - FOR PORTRAIT 600x1024"""
        screen.fill(COLOR_WHITE)
        draw_status_bar(screen, self.font_s)
        
        # Folders - stacked vertically for portrait
        self.folder_rects = []
        folders = [
            ('notes', 'Notes'),
            ('books', 'Books')
        ]
        
        # Start from top with good margin
        y_start = 100
        
        for i, (folder_id, label) in enumerate(folders):
            rect = pygame.Rect(
                50,  # Left margin for portrait
                y_start + i * 180,
                500,  # Width for portrait (600 - 100 margin)
                150
            )
            
            # Draw folder card - GRAYSCALE
            pygame.draw.rect(screen, (250, 250, 250), rect, border_radius=10)  # Light grey
            pygame.draw.rect(screen, (150, 150, 150), rect, 2, border_radius=10)  # Medium grey border
            
            # Draw folder icon (centered in card)
            icon_x = rect.centerx - 30
            icon_y = rect.centery - 20
            self.draw_folder_icon(screen, icon_x, icon_y, size=60)
            
            # Draw folder label below icon
            label_text = self.font_l.render(label, True, COLOR_BLACK)
            label_x = rect.centerx - label_text.get_width() // 2
            label_y = rect.centery + 25
            screen.blit(label_text, (label_x, label_y))
            
            self.folder_rects.append((rect, folder_id))
    
    def draw_folder_contents(self, screen, notebooks, keyboard, renaming_idx, temp_name):
        """Draw the contents of a folder (notebooks)"""
        screen.fill(COLOR_WHITE)
        draw_status_bar(screen, self.font_s)
        
        # Back button - GRAYSCALE
        self.back_btn = pygame.Rect(10, 40, 70, 40)
        pygame.draw.rect(screen, (200, 200, 200), self.back_btn, border_radius=20)  # Light grey
        back_text = self.font_s.render("< Back", True, COLOR_BLACK)
        screen.blit(back_text, (20, 50))
        
        # Folder title
        folder_names = {'notes': 'Notes', 'books': 'Books'}
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
            
            # Draw notebook icon/preview area
            icon_rect = pygame.Rect(rect.x + 10, rect.y + 10, 230, 90)
            pygame.draw.rect(screen, COLOR_WHITE, icon_rect, border_radius=5)
            
            # Draw simple notebook icon
            pygame.draw.line(screen, COLOR_UI_DARK, 
                           (icon_rect.centerx - 20, icon_rect.centery - 15),
                           (icon_rect.centerx - 20, icon_rect.centery + 15), 3)
            pygame.draw.line(screen, COLOR_UI_DARK,
                           (icon_rect.centerx - 10, icon_rect.centery - 15),
                           (icon_rect.centerx - 10, icon_rect.centery + 15), 2)
            pygame.draw.line(screen, COLOR_UI_DARK,
                           (icon_rect.centerx, icon_rect.centery - 15),
                           (icon_rect.centerx, icon_rect.centery + 15), 2)
            
            # Draw notebook name area
            name_rect = pygame.Rect(rect.x + 10, rect.y + 110, 230, 30)
            
            if renaming_idx == actual_idx:
                # Editing mode
                pygame.draw.rect(screen, COLOR_WHITE, name_rect, border_radius=5)
                pygame.draw.rect(screen, COLOR_BLACK, name_rect, 1, border_radius=5)
                txt = self.font_s.render(temp_name + "|", True, COLOR_BLACK)
            else:
                # Display mode
                txt = self.font_s.render(nb.name, True, COLOR_BLACK)
            
            screen.blit(txt, (name_rect.x + 5, name_rect.y + 5))
            self.nb_rects.append((rect, name_rect, actual_idx))
        
        # Show message if no notebooks
        if not filtered_notebooks:
            msg = self.font_m.render("No items yet. Tap + New to create one.", True, COLOR_UI_DARK)
            screen.blit(msg, (DISPLAY_WIDTH // 2 - 150, DISPLAY_HEIGHT // 2))
        
        # Draw keyboard if visible
        keyboard.draw(screen)
    
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
        # Check keyboard clicks (only when in folder view)
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