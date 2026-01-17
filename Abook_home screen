import pygame
import sys
import os
import math

DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 1024
BACKGROUND_COLOR = (255, 255, 255)
FOREGROUND_COLOR = (0, 0, 0)
LIGHT_GRAY = (240, 240, 240)

STATUS_BAR_HEIGHT = 64
STATUS_BAR_LEFT_PADDING = 20
STATUS_BAR_RIGHT_PADDING = 20
STATUS_BAR_ICON_SPACING = 18
STATUS_BAR_ICON_SIZE = 28
STATUS_BAR_FONT_SIZE = 28

ICON_TILE_SIZE = 120
ICON_BORDER_WIDTH = 2
ICON_CORNER_RADIUS = 20
ICON_GRAPHIC_SIZE = 72
ICON_STROKE_WIDTH = 5
ICON_LABEL_FONT_SIZE = 20
ICON_LABEL_SPACING = 12
ICON_BLOCK_SPACING = 36

TAP_FEEDBACK_BORDER_WIDTH = 3
TAP_FEEDBACK_DURATION_MS = 150

FPS = 30


class StatusBar:
    def __init__(self):
        self.y = 0
        self.height = STATUS_BAR_HEIGHT
        
        self.title_x = STATUS_BAR_LEFT_PADDING
        self.title_y = STATUS_BAR_HEIGHT // 2
        
        self.battery_x = DISPLAY_WIDTH - STATUS_BAR_RIGHT_PADDING - STATUS_BAR_ICON_SIZE
        self.battery_y = (STATUS_BAR_HEIGHT - STATUS_BAR_ICON_SIZE) // 2
        self.battery_percent = 85
        
        self.wifi_x = self.battery_x - STATUS_BAR_ICON_SPACING - STATUS_BAR_ICON_SIZE
        self.wifi_y = self.battery_y
        self.wifi_connected = True
    
    def draw_battery_icon(self, surface):
        x = self.battery_x
        y = self.battery_y
        size = STATUS_BAR_ICON_SIZE
        
        body_width = int(size * 0.7)
        body_height = int(size * 0.5)
        body_x = x + (size - body_width) // 2
        body_y = y + (size - body_height) // 2
        
        tip_width = int(size * 0.1)
        tip_height = int(body_height * 0.4)
        tip_x = body_x + body_width
        tip_y = body_y + (body_height - tip_height) // 2
        
        pygame.draw.rect(surface, FOREGROUND_COLOR, 
                        (body_x, body_y, body_width, body_height), 2)
        pygame.draw.rect(surface, FOREGROUND_COLOR, 
                        (tip_x, tip_y, tip_width, tip_height))
        
        fill_margin = 3
        fill_width = int((body_width - fill_margin * 2) * (self.battery_percent / 100.0))
        if fill_width > 0:
            pygame.draw.rect(surface, FOREGROUND_COLOR, 
                           (body_x + fill_margin, body_y + fill_margin, 
                            fill_width, body_height - fill_margin * 2))
    
    def draw_wifi_icon(self, surface):
        x = self.wifi_x
        y = self.wifi_y
        size = STATUS_BAR_ICON_SIZE
        
        center_x = x + size // 2
        bottom_y = y + size - 4
        
        bar_configs = [
            (size * 0.65, 3),
            (size * 0.45, 3),
            (size * 0.25, 3)
        ]
        
        for radius_mult, thickness in bar_configs:
            radius = int(radius_mult)
            points = []
            steps = 12
            start_angle = math.pi * 0.75
            end_angle = math.pi * 0.25
            
            for step in range(steps + 1):
                angle = start_angle + (end_angle - start_angle) * step / steps
                px = center_x + radius * math.cos(angle)
                py = bottom_y + radius * math.sin(angle)
                points.append((int(px), int(py)))
            
            if len(points) > 1:
                pygame.draw.lines(surface, FOREGROUND_COLOR, False, points, thickness)
    
    def draw(self, surface, font_title):
        title_text = font_title.render("Abook", True, FOREGROUND_COLOR)
        title_rect = title_text.get_rect(left=self.title_x, centery=self.title_y)
        surface.blit(title_text, title_rect)
        
        self.draw_battery_icon(surface)
        self.draw_wifi_icon(surface)
        
        pygame.draw.line(surface, FOREGROUND_COLOR, 
                        (0, 63), (DISPLAY_WIDTH, 63), 1)


class AppIcon:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.tile_size = ICON_TILE_SIZE
        
        self.tile_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
        
        self.graphic_size = ICON_GRAPHIC_SIZE
        self.graphic_x = x + (self.tile_size - self.graphic_size) // 2
        self.graphic_y = y + (self.tile_size - self.graphic_size) // 2
        self.center_x = self.graphic_x + self.graphic_size // 2
        self.center_y = self.graphic_y + self.graphic_size // 2
        
        self.label_y = y + self.tile_size + ICON_LABEL_SPACING
        
        self.tap_start_time = 0
        self.is_tapped = False
    
    def draw_notes_icon(self, surface):
        pen_length = int(self.graphic_size * 0.7)
        pen_width = int(self.graphic_size * 0.15)
        angle = math.radians(-45)
        
        center_offset = pen_length // 2
        start_x = self.center_x - int(center_offset * math.cos(angle))
        start_y = self.center_y - int(center_offset * math.sin(angle))
        end_x = self.center_x + int(center_offset * math.cos(angle))
        end_y = self.center_y + int(center_offset * math.sin(angle))
        
        points = []
        perp_angle = angle + math.pi / 2
        half_width = pen_width // 2
        
        p1_x = start_x + int(half_width * math.cos(perp_angle))
        p1_y = start_y + int(half_width * math.sin(perp_angle))
        p2_x = start_x - int(half_width * math.cos(perp_angle))
        p2_y = start_y - int(half_width * math.sin(perp_angle))
        p3_x = end_x - int(half_width * math.cos(perp_angle))
        p3_y = end_y - int(half_width * math.sin(perp_angle))
        p4_x = end_x + int(half_width * math.cos(perp_angle))
        p4_y = end_y + int(half_width * math.sin(perp_angle))
        
        points = [(p1_x, p1_y), (p2_x, p2_y), (p3_x, p3_y), (p4_x, p4_y)]
        pygame.draw.polygon(surface, FOREGROUND_COLOR, points)
        
        tip_length = int(pen_width * 1.2)
        tip_x = end_x + int(tip_length * math.cos(angle))
        tip_y = end_y + int(tip_length * math.sin(angle))
        tip_points = [(p3_x, p3_y), (p4_x, p4_y), (tip_x, tip_y)]
        pygame.draw.polygon(surface, FOREGROUND_COLOR, tip_points)
    
    def draw_read_icon(self, surface):
        book_width = int(self.graphic_size * 0.75)
        book_height = int(self.graphic_size * 0.6)
        book_x = self.center_x - book_width // 2
        book_y = self.center_y - book_height // 2
        
        mid_x = self.center_x
        
        left_page_top = [(book_x, book_y), (mid_x - 3, book_y)]
        left_page_bottom = [(book_x, book_y + book_height), (mid_x - 3, book_y + book_height)]
        
        right_page_top = [(mid_x + 3, book_y), (book_x + book_width, book_y)]
        right_page_bottom = [(mid_x + 3, book_y + book_height), (book_x + book_width, book_y + book_height)]
        
        curve_depth = 8
        
        left_points = [
            (book_x, book_y),
            (book_x, book_y + book_height),
            (mid_x - 3, book_y + book_height + curve_depth),
            (mid_x, book_y + book_height + curve_depth),
            (mid_x + 3, book_y + book_height + curve_depth),
            (book_x + book_width, book_y + book_height),
            (book_x + book_width, book_y),
            (mid_x + 3, book_y - curve_depth),
            (mid_x, book_y - curve_depth),
            (mid_x - 3, book_y - curve_depth),
            (book_x, book_y)
        ]
        
        pygame.draw.polygon(surface, FOREGROUND_COLOR, left_points, ICON_STROKE_WIDTH)
        pygame.draw.line(surface, FOREGROUND_COLOR, (mid_x, book_y - curve_depth), (mid_x, book_y + book_height + curve_depth), ICON_STROKE_WIDTH)
    
    def draw_test_icon(self, surface):
        board_width = int(self.graphic_size * 0.65)
        board_height = int(self.graphic_size * 0.75)
        board_x = self.center_x - board_width // 2
        board_y = self.center_y - board_height // 2
        
        clip_width = int(board_width * 0.35)
        clip_height = int(board_height * 0.12)
        clip_x = self.center_x - clip_width // 2
        clip_y = board_y - clip_height // 2
        
        pygame.draw.rect(surface, FOREGROUND_COLOR, (board_x, board_y, board_width, board_height), ICON_STROKE_WIDTH)
        
        pygame.draw.rect(surface, FOREGROUND_COLOR, (clip_x, clip_y, clip_width, clip_height))
        pygame.draw.rect(surface, BACKGROUND_COLOR, (clip_x + 3, clip_y + 3, clip_width - 6, clip_height - 6))
        
        check_size = int(board_width * 0.4)
        check_x = self.center_x - check_size // 2
        check_y = self.center_y - check_size // 4
        
        check_points = [
            (check_x, check_y + check_size // 3),
            (check_x + check_size // 3, check_y + check_size),
            (check_x + check_size, check_y)
        ]
        
        pygame.draw.lines(surface, FOREGROUND_COLOR, False, check_points, ICON_STROKE_WIDTH)
    
    def draw_settings_icon(self, surface):
        outer_radius = int(self.graphic_size * 0.35)
        inner_radius = int(self.graphic_size * 0.15)
        tooth_count = 6
        tooth_length = int(self.graphic_size * 0.15)
        
        points = []
        for i in range(tooth_count * 2):
            angle = math.pi * 2 * i / (tooth_count * 2) - math.pi / 2
            if i % 2 == 0:
                radius = outer_radius + tooth_length
            else:
                radius = outer_radius
            x = self.center_x + radius * math.cos(angle)
            y = self.center_y + radius * math.sin(angle)
            points.append((int(x), int(y)))
        
        pygame.draw.polygon(surface, FOREGROUND_COLOR, points, ICON_STROKE_WIDTH)
        
        pygame.draw.circle(surface, FOREGROUND_COLOR, (self.center_x, self.center_y), inner_radius, ICON_STROKE_WIDTH)
    
    def draw(self, surface, font_label, current_time):
        tile_surface = pygame.Surface((self.tile_size, self.tile_size))
        tile_surface.fill(BACKGROUND_COLOR)
        
        if self.name == "Notes":
            self.draw_notes_icon(tile_surface)
        elif self.name == "Read":
            self.draw_read_icon(tile_surface)
        elif self.name == "Test":
            self.draw_test_icon(tile_surface)
        elif self.name == "Settings":
            self.draw_settings_icon(tile_surface)
        
        pygame.draw.rect(tile_surface, FOREGROUND_COLOR, 
                        tile_surface.get_rect(), 
                        ICON_BORDER_WIDTH, 
                        border_radius=ICON_CORNER_RADIUS)
        
        if self.is_tapped and (current_time - self.tap_start_time) < TAP_FEEDBACK_DURATION_MS:
            pygame.draw.rect(tile_surface, FOREGROUND_COLOR, 
                           tile_surface.get_rect(), 
                           TAP_FEEDBACK_BORDER_WIDTH, 
                           border_radius=ICON_CORNER_RADIUS)
        elif self.is_tapped:
            self.is_tapped = False
        
        surface.blit(tile_surface, (self.x, self.y))
        
        label_text = font_label.render(self.name, True, FOREGROUND_COLOR)
        label_rect = label_text.get_rect(centerx=self.x + self.tile_size // 2, 
                                        top=self.label_y)
        surface.blit(label_text, label_rect)
    
    def handle_tap(self, pos, current_time):
        if self.tile_rect.collidepoint(pos):
            self.is_tapped = True
            self.tap_start_time = current_time
            print(f"App selected: {self.name}")
            return True
        return False


class HomeScreen:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('Abook OS')
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.font_title = pygame.font.Font(None, STATUS_BAR_FONT_SIZE)
        self.font_label = pygame.font.Font(None, ICON_LABEL_FONT_SIZE)
        
        self.status_bar = StatusBar()
        self.icons = []
        
        self.calculate_icon_positions()
    
    def calculate_icon_positions(self):
        app_names = ["Notes", "Read", "Test", "Settings"]
        
        icon_block_height = ICON_TILE_SIZE + ICON_LABEL_SPACING + ICON_LABEL_FONT_SIZE
        total_height = (icon_block_height * len(app_names) + 
                       ICON_BLOCK_SPACING * (len(app_names) - 1))
        
        available_height = DISPLAY_HEIGHT - STATUS_BAR_HEIGHT
        start_y = STATUS_BAR_HEIGHT + (available_height - total_height) // 2
        
        icon_x = (DISPLAY_WIDTH - ICON_TILE_SIZE) // 2
        
        for i, name in enumerate(app_names):
            icon_y = start_y + i * (icon_block_height + ICON_BLOCK_SPACING)
            self.icons.append(AppIcon(name, icon_x, icon_y))
    
    def handle_events(self):
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for icon in self.icons:
                        if icon.handle_tap(event.pos, current_time):
                            break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        self.status_bar.draw(self.screen, self.font_title)
        
        current_time = pygame.time.get_ticks()
        for icon in self.icons:
            icon.draw(self.screen, self.font_label, current_time)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    home_screen = HomeScreen()
    home_screen.run()
