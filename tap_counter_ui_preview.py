import pygame
import sys
import os
import math

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1024

# ---- Grayscale theme (e-ink friendly) ----
BG_WHITE = (255, 255, 255)
BG_LIGHT = (248, 248, 248)

TEXT_BLACK = (0, 0, 0)
ICON_DARK_GRAY = (90, 90, 90)
FG_GRAY = (120, 120, 120)
BORDER_GRAY = (170, 170, 170)

FPS = 30

HEADER_HEIGHT = 70
CARD_HEIGHT = 100
CARD_SPACING = 16
BOTTOM_NAV_HEIGHT = 70


class StatusBar:
    def __init__(self, width):
        self.width = width
        self.height = HEADER_HEIGHT
        self.padding = 24

        self.profile_size = 36
        self.profile_x = self.width - self.padding - self.profile_size
        self.profile_y = (self.height - self.profile_size) // 2

        self.battery_width = 32
        self.battery_height = 16
        self.battery_x = self.profile_x - 50 - self.battery_width
        self.battery_y = (self.height - self.battery_height) // 2
        self.battery_percent = 85

        self.wifi_size = 20
        self.wifi_x = self.battery_x - 30 - self.wifi_size
        self.wifi_y = (self.height - self.wifi_size) // 2

    def draw_battery_icon(self, surface):
        body_rect = pygame.Rect(
            self.battery_x, self.battery_y,
            self.battery_width - 3, self.battery_height
        )
        pygame.draw.rect(surface, ICON_DARK_GRAY, body_rect, 2)

        tip_x = self.battery_x + self.battery_width - 3
        tip_y = self.battery_y + (self.battery_height - 8) // 2
        pygame.draw.rect(surface, ICON_DARK_GRAY, (tip_x, tip_y, 3, 8))

        fill_width = int((self.battery_width - 9) * (self.battery_percent / 100))
        if fill_width > 0:
            pygame.draw.rect(
                surface,
                ICON_DARK_GRAY,
                (self.battery_x + 3, self.battery_y + 3,
                 fill_width, self.battery_height - 6)
            )

    def draw_wifi_icon(self, surface):
        center_x = self.wifi_x + self.wifi_size // 2
        bottom_y = self.wifi_y + self.wifi_size

        for width, height in [(8, 4), (14, 8), (20, 12)]:
            points = []
            for i in range(9):
                t = i / 8
                x = center_x - width // 2 + width * t
                y = bottom_y - height * (1 - (1 - 2 * abs(t - 0.5)) ** 2)
                points.append((int(x), int(y)))
            pygame.draw.lines(surface, ICON_DARK_GRAY, False, points, 2)

        pygame.draw.circle(surface, ICON_DARK_GRAY, (center_x, bottom_y - 1), 2)

    def draw(self, surface):
        font_title = pygame.font.Font(None, 36)
        title = font_title.render("Dashboard", True, TEXT_BLACK)
        surface.blit(title, (self.padding, self.height // 2 - title.get_height() // 2))

        self.draw_wifi_icon(surface)
        self.draw_battery_icon(surface)

        pygame.draw.circle(
            surface,
            ICON_DARK_GRAY,
            (self.profile_x + self.profile_size // 2,
             self.profile_y + self.profile_size // 2),
            self.profile_size // 2,
            2
        )

        font_initial = pygame.font.Font(None, 28)
        initial = font_initial.render("M", True, TEXT_BLACK)
        surface.blit(
            initial,
            initial.get_rect(center=(
                self.profile_x + self.profile_size // 2,
                self.profile_y + self.profile_size // 2
            ))
        )

        pygame.draw.line(
            surface, BORDER_GRAY,
            (0, self.height - 1),
            (self.width, self.height - 1), 1
        )


class AppIcon:
    def __init__(self, name, y):
        self.name = name
        self.card_width = SCREEN_WIDTH - 48
        self.card_height = CARD_HEIGHT
        self.x = (SCREEN_WIDTH - self.card_width) // 2
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.card_width, self.card_height)

        self.icon_size = 40
        self.icon_x = self.x + 20
        self.icon_y = self.y + (self.card_height - self.icon_size) // 2
        self.icon_cx = self.icon_x + self.icon_size // 2
        self.icon_cy = self.icon_y + self.icon_size // 2

        self.text_x = self.icon_x + self.icon_size + 16
        self.text_y = self.y + self.card_height // 2

        self.subtitle = {
            "Notes": "4 recent notes",
            "Read": "The Great Gatsby (45%)",
            "Test": "Next: Physics 101",
            "Settings": "Preferences & account"
        }.get(name, "")

        self.is_pressed = False

    def draw(self, surface):
        pygame.draw.rect(surface, BG_WHITE, self.rect)
        pygame.draw.rect(surface, BORDER_GRAY, self.rect, 1)

        if self.name == "Notes":
            pygame.draw.rect(
                surface, ICON_DARK_GRAY,
                (self.icon_x + 6, self.icon_y + 6, 28, 28), 2
            )
            for i in range(3):
                pygame.draw.line(
                    surface, ICON_DARK_GRAY,
                    (self.icon_x + 10, self.icon_y + 14 + i * 6),
                    (self.icon_x + 30, self.icon_y + 14 + i * 6), 2
                )

        elif self.name == "Read":
            pygame.draw.line(
                surface, ICON_DARK_GRAY,
                (self.icon_x + 8, self.icon_y + 6),
                (self.icon_x + 8, self.icon_y + 34), 2
            )
            pygame.draw.line(
                surface, ICON_DARK_GRAY,
                (self.icon_x + 32, self.icon_y + 6),
                (self.icon_x + 32, self.icon_y + 34), 2
            )

        elif self.name == "Test":
            pygame.draw.rect(
                surface, ICON_DARK_GRAY,
                (self.icon_x + 6, self.icon_y + 6, 28, 28), 2
            )
            pygame.draw.lines(
                surface, ICON_DARK_GRAY, False,
                [(self.icon_x + 12, self.icon_y + 20),
                 (self.icon_x + 18, self.icon_y + 26),
                 (self.icon_x + 28, self.icon_y + 14)], 2
            )

        elif self.name == "Settings":
            pygame.draw.circle(
                surface, ICON_DARK_GRAY,
                (self.icon_cx, self.icon_cy), 12, 2
            )
            pygame.draw.circle(
                surface, ICON_DARK_GRAY,
                (self.icon_cx, self.icon_cy), 5, 2
            )

        font_title = pygame.font.Font(None, 28)
        font_sub = pygame.font.Font(None, 20)

        surface.blit(
            font_title.render(self.name, True, TEXT_BLACK),
            (self.text_x, self.text_y - 14)
        )
        surface.blit(
            font_sub.render(self.subtitle, True, FG_GRAY),
            (self.text_x, self.text_y + 6)
        )

    def is_tapped(self, pos):
        if self.rect.collidepoint(pos):
            print(f"App tapped: {self.name}")
            return True
        return False


def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Abook OS")
    clock = pygame.time.Clock()

    status_bar = StatusBar(SCREEN_WIDTH)

    font_welcome = pygame.font.Font(None, 48)
    welcome_y = HEADER_HEIGHT + 24

    start_y = welcome_y + 60
    apps = [
        AppIcon("Notes", start_y),
        AppIcon("Read", start_y + CARD_HEIGHT + CARD_SPACING),
        AppIcon("Test", start_y + 2 * (CARD_HEIGHT + CARD_SPACING)),
        AppIcon("Settings", start_y + 3 * (CARD_HEIGHT + CARD_SPACING)),
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for app in apps:
                    if app.is_tapped(event.pos):
                        break

        screen.fill(BG_WHITE)
        status_bar.draw(screen)

        screen.blit(
            font_welcome.render("Welcome back, Reader.", True, TEXT_BLACK),
            (24, welcome_y)
        )

        for app in apps:
            app.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
