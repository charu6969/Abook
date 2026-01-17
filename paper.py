import pygame
import sys
import math

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 600, 900
SIDEBAR_WIDTH = 80
FPS = 120

PAPER_COLOR = (245, 245, 240)
LINE_COLOR = (120, 120, 120)
INK_COLOR = (0, 0, 0)
UI_BG = (220, 220, 220)
UI_BORDER = (100, 100, 100)

LINE_GAP = 40
PEN_RADIUS = 3
ERASER_RADIUS = 15
MAX_UNDO = 20

# ----------------------------------------

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Abook OS – Paper Mode")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 14)

# -------- LAYERS --------
paper_bg = pygame.Surface((WIDTH - SIDEBAR_WIDTH, HEIGHT))
ink_layer = pygame.Surface((WIDTH - SIDEBAR_WIDTH, HEIGHT), pygame.SRCALPHA)

paper_bg.fill(PAPER_COLOR)

def draw_lines():
    for y in range(0, HEIGHT, LINE_GAP):
        pygame.draw.line(paper_bg, LINE_COLOR, (0, y), (WIDTH, y), 1)

draw_lines()

undo_stack = []
writing = False
erase_mode = False
last_pos = None

# ---------------- FUNCTIONS ----------------
def save_undo():
    undo_stack.append(ink_layer.copy())
    if len(undo_stack) > MAX_UNDO:
        undo_stack.pop(0)

def draw_smooth_line(surface, color, start, end, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = int(max(abs(dx), abs(dy)))

    if distance == 0:
        pygame.draw.circle(surface, color, start, radius)
        return

    for i in range(distance):
        x = int(start[0] + dx * i / distance)
        y = int(start[1] + dy * i / distance)
        pygame.draw.circle(surface, color, (x, y), radius)

def draw_button(y, label, active=False):
    rect = pygame.Rect(10, y, 60, 60)
    pygame.draw.rect(screen, UI_BG, rect, border_radius=8)
    pygame.draw.rect(screen, UI_BORDER, rect, 1, border_radius=8)
    if active:
        pygame.draw.rect(screen, (180, 180, 180), rect, border_radius=8)

    text = font.render(label, True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=rect.center))
    return rect

# ---------------- LOOP ----------------
while True:
    clock.tick(FPS)
    screen.fill(PAPER_COLOR)

    # Sidebar
    pygame.draw.rect(screen, UI_BG, (0, 0, SIDEBAR_WIDTH, HEIGHT))
    pygame.draw.line(screen, UI_BORDER, (SIDEBAR_WIDTH, 0), (SIDEBAR_WIDTH, HEIGHT), 1)

    pen_btn = draw_button(20, "PEN", not erase_mode)
    eraser_btn = draw_button(100, "ERASE", erase_mode)
    undo_btn = draw_button(180, "UNDO")
    exit_btn = draw_button(260, "EXIT")

    # Paper + Ink layers
    screen.blit(paper_bg, (SIDEBAR_WIDTH, 0))
    screen.blit(ink_layer, (SIDEBAR_WIDTH, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if pen_btn.collidepoint(mx, my):
                erase_mode = False

            elif eraser_btn.collidepoint(mx, my):
                erase_mode = True

            elif undo_btn.collidepoint(mx, my):
                if undo_stack:
                    ink_layer.blit(undo_stack.pop(), (0, 0))

            elif exit_btn.collidepoint(mx, my):
                pygame.quit()
                sys.exit()

            elif mx > SIDEBAR_WIDTH:
                save_undo()
                writing = True
                last_pos = (mx - SIDEBAR_WIDTH, my)

        if event.type == pygame.MOUSEBUTTONUP:
            writing = False
            last_pos = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if undo_stack:
                    ink_layer.blit(undo_stack.pop(), (0, 0))

    if writing:
        mx, my = pygame.mouse.get_pos()
        if mx > SIDEBAR_WIDTH:
            current_pos = (mx - SIDEBAR_WIDTH, my)

            if erase_mode:
                draw_smooth_line(
                    ink_layer,
                    (0, 0, 0, 0),
                    last_pos,
                    current_pos,
                    ERASER_RADIUS
                )
            else:
                draw_smooth_line(
                    ink_layer,
                    INK_COLOR,
                    last_pos,
                    current_pos,
                    PEN_RADIUS
                )

            last_pos = current_pos

    pygame.display.flip()
