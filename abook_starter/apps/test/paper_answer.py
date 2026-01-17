import pygame
import os

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


class PaperAnswerScreen:
    def __init__(self, screen, conn, exam_id, student_id):
        self.screen = screen
        self.conn = conn
        self.exam_id = exam_id
        self.student_id = student_id

        self.clock = pygame.time.Clock()
        self.running = True

        self.page_no = 1
        self.writing = False
        self.erase_mode = False
        self.last_pos = None
        self.undo_stack = []

        self.font = pygame.font.SysFont("arial", 14)

        # -------- Storage --------
        self.base_dir = f"data/exams/exam_{exam_id}/student_{student_id}"
        os.makedirs(self.base_dir, exist_ok=True)

        # -------- Layers --------
        self.paper_bg = pygame.Surface((WIDTH - SIDEBAR_WIDTH, HEIGHT))
        self.ink_layer = pygame.Surface(
            (WIDTH - SIDEBAR_WIDTH, HEIGHT), pygame.SRCALPHA
        )

        self.paper_bg.fill(PAPER_COLOR)
        self.draw_lines()
        self.load_page()

    # ---------------- Paper ----------------
    def draw_lines(self):
        for y in range(0, HEIGHT, LINE_GAP):
            pygame.draw.line(
                self.paper_bg, LINE_COLOR,
                (0, y), (WIDTH, y), 1
            )

    # ---------------- Undo ----------------
    def save_undo(self):
        self.undo_stack.append(self.ink_layer.copy())
        if len(self.undo_stack) > MAX_UNDO:
            self.undo_stack.pop(0)

    # ---------------- Drawing ----------------
    def draw_smooth_line(self, surface, color, start, end, radius):
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

    # ---------------- Buttons ----------------
    def draw_button(self, y, label, active=False):
        rect = pygame.Rect(10, y, 60, 60)
        pygame.draw.rect(self.screen, UI_BG, rect, border_radius=8)
        pygame.draw.rect(self.screen, UI_BORDER, rect, 1, border_radius=8)
        if active:
            pygame.draw.rect(self.screen, (180, 180, 180), rect, border_radius=8)
        text = self.font.render(label, True, (0, 0, 0))
        self.screen.blit(text, text.get_rect(center=rect.center))
        return rect

    # ---------------- Page IO ----------------
    def page_path(self):
        return f"{self.base_dir}/page_{self.page_no}.png"

    def save_page(self):
        pygame.image.save(self.ink_layer, self.page_path())
        self.conn.execute("""
            INSERT OR REPLACE INTO answers
            (student_id, page_number, image_path)
            VALUES (?, ?, ?)
        """, (self.student_id, self.page_no, self.page_path()))
        self.conn.commit()

    def load_page(self):
        self.ink_layer.fill((0, 0, 0, 0))
        self.undo_stack.clear()
        if os.path.exists(self.page_path()):
            img = pygame.image.load(self.page_path())
            self.ink_layer.blit(img, (0, 0))

    # ---------------- Main Loop ----------------
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.screen.fill(PAPER_COLOR)

            # Sidebar
            pygame.draw.rect(self.screen, UI_BG, (0, 0, SIDEBAR_WIDTH, HEIGHT))
            pygame.draw.line(
                self.screen, UI_BORDER,
                (SIDEBAR_WIDTH, 0), (SIDEBAR_WIDTH, HEIGHT), 1
            )

            pen_btn    = self.draw_button(20,  "PEN",  not self.erase_mode)
            eraser_btn = self.draw_button(100, "ERASE", self.erase_mode)
            undo_btn   = self.draw_button(180, "UNDO")
            prev_btn   = self.draw_button(260, "PREV")
            next_btn   = self.draw_button(340, "NEXT")
            exit_btn   = self.draw_button(420, "EXIT")

            # Paper
            self.screen.blit(self.paper_bg, (SIDEBAR_WIDTH, 0))
            self.screen.blit(self.ink_layer, (SIDEBAR_WIDTH, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_page()
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    if pen_btn.collidepoint(mx, my):
                        self.erase_mode = False

                    elif eraser_btn.collidepoint(mx, my):
                        self.erase_mode = True

                    elif undo_btn.collidepoint(mx, my):
                        if self.undo_stack:
                            self.ink_layer.blit(self.undo_stack.pop(), (0, 0))

                    elif prev_btn.collidepoint(mx, my):
                        if self.page_no > 1:
                            self.save_page()
                            self.page_no -= 1
                            self.load_page()

                    elif next_btn.collidepoint(mx, my):
                        self.save_page()
                        self.page_no += 1
                        self.load_page()

                    elif exit_btn.collidepoint(mx, my):
                        self.save_page()
                        self.running = False

                    elif mx > SIDEBAR_WIDTH:
                        self.save_undo()
                        self.writing = True
                        self.last_pos = (mx - SIDEBAR_WIDTH, my)

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.writing = False
                    self.last_pos = None

            if self.writing:
                mx, my = pygame.mouse.get_pos()
                if mx > SIDEBAR_WIDTH:
                    cur = (mx - SIDEBAR_WIDTH, my)
                    if self.erase_mode:
                        self.draw_smooth_line(
                            self.ink_layer, (0, 0, 0, 0),
                            self.last_pos, cur, ERASER_RADIUS
                        )
                    else:
                        self.draw_smooth_line(
                            self.ink_layer, INK_COLOR,
                            self.last_pos, cur, PEN_RADIUS
                        )
                    self.last_pos = cur

            pygame.display.flip()
