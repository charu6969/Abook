"""
Modern Home View for ABook - Y Combinator Ready
"""
import pygame
from config import *


class ModernHomeView:
    """Modern, professional home screen"""
    
    def __init__(self, fonts):
        self.font_s, self.font_m, self.font_l = fonts
        try:
            self.font_xl = pygame.font.SysFont(None, 36)
        except:
            self.font_xl = self.font_l
        
        self.current_folder = 'notes'
        self.folder_tabs = {}
        self.notebook_rects = []
        self.delete_btns = []
        self.add_btn = None
    
    def draw(self, screen, notebooks, keyboard, renaming_idx, temp_name):
        """Draw modern home screen for PORTRAIT (600x1024)"""
        # Gradient background
        for y in range(1024):  # Portrait height
            progress = y / 1024
            r = int(248 + (241 - 248) * progress)
            g = int(250 + (245 - 250) * progress)
            b = int(252 + (249 - 252) * progress)
            pygame.draw.line(screen, (r, g, b), (0, y), (600, y))  # Portrait width
        
        # Modern header
        header_height = 100
        pygame.draw.rect(screen, COLOR_PRIMARY, (0, 0, 600, header_height))
        
        # App name with modern styling
        title_y = 25
        app_name = self.font_xl.render("ABook", True, COLOR_WHITE)
        screen.blit(app_name, (30, title_y))
        
        # Tagline
        tagline = self.font_s.render("Your Digital Notebook", True, COLOR_GRAY_300)
        screen.blit(tagline, (30, title_y + 35))
        
        # Stats bar
        stats_y = header_height - 30
        total_notes = len([n for n in notebooks if n.folder == 'notes'])
        total_books = len([n for n in notebooks if n.folder == 'books'])
        
        stats_text = f"{total_notes + total_books} Notebooks"
        stats = self.font_s.render(stats_text, True, COLOR_GRAY_300)
        screen.blit(stats, (30, stats_y))
        
        # Folder tabs - STACKED VERTICALLY for portrait
        tab_y = header_height + 30
        tab_width = 540  # Almost full width
        tab_height = 80
        tab_x = 30
        
        folders = [
            ('notes', 'Notes', COLOR_SECONDARY, total_notes),
            ('books', 'Books', COLOR_ACCENT, total_books)
        ]
        
        self.folder_tabs = {}
        
        for i, (folder_id, label, color, count) in enumerate(folders):
            y = tab_y + i * (tab_height + 15)
            
            # Tab card
            is_active = self.current_folder == folder_id
            tab_rect = pygame.Rect(tab_x, y, tab_width, tab_height)
            
            if is_active:
                pygame.draw.rect(screen, color, tab_rect, border_radius=12)
                text_color = COLOR_WHITE
                count_color = COLOR_WHITE
            else:
                pygame.draw.rect(screen, COLOR_WHITE, tab_rect, border_radius=12)
                pygame.draw.rect(screen, COLOR_GRAY_200, tab_rect, 2, border_radius=12)
                text_color = COLOR_GRAY_800
                count_color = color
            
            # Tab label
            label_surf = self.font_l.render(label, True, text_color)
            screen.blit(label_surf, (tab_rect.x + 20, tab_rect.y + 20))
            
            # Count badge
            count_surf = self.font_l.render(str(count), True, count_color)
            screen.blit(count_surf, (tab_rect.right - 60, tab_rect.y + 20))
            
            self.folder_tabs[folder_id] = tab_rect
        
        # Notebooks list
        notebooks_y = tab_y + len(folders) * (tab_height + 15) + 30
        filtered = [n for n in notebooks if n.folder == self.current_folder]
        
        if not filtered:
            # Empty state
            empty_y = notebooks_y + 100
            icon_size = 60
            icon_r = pygame.Rect((600 - icon_size)//2, empty_y, icon_size, icon_size)
            pygame.draw.rect(screen, COLOR_GRAY_200, icon_r, border_radius=15)
            
            pygame.draw.line(screen, COLOR_GRAY_400,
                           (icon_r.centerx, icon_r.centery - 15),
                           (icon_r.centerx, icon_r.centery + 15), 4)
            pygame.draw.line(screen, COLOR_GRAY_400,
                           (icon_r.centerx - 15, icon_r.centery),
                           (icon_r.centerx + 15, icon_r.centery), 4)
            
            msg = self.font_m.render("No notebooks yet", True, COLOR_GRAY_600)
            screen.blit(msg, ((600 - msg.get_width())//2, empty_y + 80))
            
            hint = self.font_s.render("Tap + to create", True, COLOR_GRAY_400)
            screen.blit(hint, ((600 - hint.get_width())//2, empty_y + 110))
        else:
            # Notebook cards - PORTRAIT
            self.notebook_rects = []
            self.delete_btns = []
            
            card_h = 85
            margin = 30
            card_width = 540
            y = notebooks_y
            
            for i, nb in enumerate(filtered):
                card = pygame.Rect(margin, y, card_width, card_h)
                
                # Shadow
                shadow = card.copy()
                shadow.x += 2
                shadow.y += 2
                pygame.draw.rect(screen, COLOR_GRAY_200, shadow, border_radius=12)
                
                # Card
                pygame.draw.rect(screen, COLOR_WHITE, card, border_radius=12)
                pygame.draw.rect(screen, COLOR_GRAY_300, card, 2, border_radius=12)
                
                # Name
                if renaming_idx == i:
                    name = temp_name + "|"
                    col = COLOR_PRIMARY
                else:
                    name = nb.name
                    col = COLOR_GRAY_800
                
                name_s = self.font_m.render(name, True, col)
                screen.blit(name_s, (card.x + 20, card.y + 20))
                
                # Layers
                info = f"{len(nb.layers)} layer{'s' if len(nb.layers) != 1 else ''}"
                info_s = self.font_s.render(info, True, COLOR_GRAY_500)
                screen.blit(info_s, (card.x + 20, card.y + 50))
                
                # Delete
                del_size = 36
                del_btn = pygame.Rect(card.right - del_size - 15, card.centery - del_size//2, del_size, del_size)
                pygame.draw.rect(screen, COLOR_DANGER, del_btn, border_radius=8)
                
                pygame.draw.line(screen, COLOR_WHITE,
                               (del_btn.centerx - 8, del_btn.centery - 8),
                               (del_btn.centerx + 8, del_btn.centery + 8), 3)
                pygame.draw.line(screen, COLOR_WHITE,
                               (del_btn.centerx + 8, del_btn.centery - 8),
                               (del_btn.centerx - 8, del_btn.centery + 8), 3)
                
                self.notebook_rects.append(card)
                self.delete_btns.append(del_btn)
                
                y += card_h + 12
        
        # Floating action button (FAB) - PORTRAIT
        fab_size = 60
        fab_x = 600 - fab_size - 20  # Portrait width
        fab_y = 1024 - fab_size - 20  # Portrait height
        self.add_btn = pygame.Rect(fab_x, fab_y, fab_size, fab_size)
        
        shadow = self.add_btn.copy()
        shadow.x += 3
        shadow.y += 3
        pygame.draw.circle(screen, COLOR_GRAY_300, shadow.center, fab_size//2)
        pygame.draw.circle(screen, COLOR_ACCENT, self.add_btn.center, fab_size//2)
        
        pygame.draw.line(screen, COLOR_WHITE,
                        (self.add_btn.centerx, self.add_btn.centery - 15),
                        (self.add_btn.centerx, self.add_btn.centery + 15), 4)
        pygame.draw.line(screen, COLOR_WHITE,
                        (self.add_btn.centerx - 15, self.add_btn.centery),
                        (self.add_btn.centerx + 15, self.add_btn.centery), 4)
        
        if renaming_idx is not None:
            keyboard.draw(screen)
    
    def handle_click(self, pos, notebooks=None, keyboard=None, renaming_idx=None, temp_name=None):
        """Handle clicks - compatible with main.py"""
        # Folder tabs
        for fid, rect in self.folder_tabs.items():
            if rect.collidepoint(pos):
                self.current_folder = fid
                return ('switch_folder', fid)
        
        # Notebooks
        for i, rect in enumerate(self.notebook_rects):
            if rect.collidepoint(pos):
                # Return the actual notebook index from filtered list
                filtered = [nb for nb in notebooks if nb.folder == self.current_folder]
                if i < len(filtered):
                    # Find the actual index in the full notebooks list
                    actual_idx = notebooks.index(filtered[i])
                    return ('open_notebook', actual_idx)
        
        # Delete buttons
        for i, btn in enumerate(self.delete_btns):
            if btn.collidepoint(pos):
                return ('delete_notebook', i)
        
        # Add button
        if self.add_btn and self.add_btn.collidepoint(pos):
            return ('add_notebook', self.current_folder)
        
        return (None, None)