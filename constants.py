import pygame

DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 800
FPS = 60

COLOR_WHITE = (255, 255, 255)
COLOR_PAPER = (248, 248, 248)
COLOR_BLACK = (20, 20, 20)
COLOR_UI_LIGHT = (230, 230, 230)
COLOR_UI_DARK = (100, 100, 100)

# Hardware status bar helper
def draw_status_bar(screen, font):
    from datetime import datetime
    pygame.draw.rect(screen, COLOR_PAPER, (0, 0, DISPLAY_WIDTH, 25))
    time_str = datetime.now().strftime("%H:%M")
    screen.blit(font.render(time_str, True, COLOR_BLACK), (DISPLAY_WIDTH//2 - 20, 4))
    
    # WiFi
    wx, wy = 15, 12
    pygame.draw.circle(screen, COLOR_BLACK, (wx, wy+3), 2)
    for i in range(1, 3):
        pygame.draw.arc(screen, COLOR_BLACK, (wx-i*4, wy-i*3, i*8, i*8), 0.5, 2.5, 1)
    
    # Battery
    bx, by = DISPLAY_WIDTH - 45, 6
    pygame.draw.rect(screen, COLOR_BLACK, (bx, by, 25, 12), 1)
    pygame.draw.rect(screen, COLOR_BLACK, (bx+25, by+3, 2, 6))
    pygame.draw.rect(screen, COLOR_BLACK, (bx+2, by+2, 18, 8))