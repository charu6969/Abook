import pygame
import sys
import os

from exam_db import get_connection
from paper_answer import PaperAnswerScreen

# ---------------- CONFIG ----------------
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1024

BG_WHITE = (255, 255, 255)
TEXT_BLACK = (0, 0, 0)
FG_GRAY = (120, 120, 120)
BORDER_GRAY = (170, 170, 170)

FPS = 60
MAX_CODE_LEN = 6

SIGNATURE_DIR = os.path.join("data", "signatures")
os.makedirs(SIGNATURE_DIR, exist_ok=True)
# ---------------------------------------


# =========================================================
# STEP 1: EXAM CODE ENTRY
# =========================================================
class ExamCodeEntry:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.code = ""
        self.error = ""
        self.exam_id = None

        self.font_title = pygame.font.Font(None, 48)
        self.font_code = pygame.font.Font(None, 64)
        self.font_hint = pygame.font.Font(None, 28)
        self.font_error = pygame.font.Font(None, 26)

        self.conn = get_connection()

    def validate_exam_code(self):
        row = self.conn.execute(
            "SELECT exam_id FROM exams WHERE exam_code = ?",
            (self.code,)
        ).fetchone()
        if row:
            self.exam_id = row[0]
            return True
        return False

    def handle_key(self, key):
        if key == pygame.K_BACKSPACE:
            self.code = self.code[:-1]
            self.error = ""

        elif key == pygame.K_RETURN:
            if len(self.code) != MAX_CODE_LEN:
                self.error = "Enter 6-digit exam code"
                return

            if self.validate_exam_code():
                self.running = False
            else:
                self.error = "Invalid exam code"
                self.code = ""

        elif pygame.K_0 <= key <= pygame.K_9:
            if len(self.code) < MAX_CODE_LEN:
                self.code += chr(key)
                self.error = ""

    def draw(self):
        self.screen.fill(BG_WHITE)

        title = self.font_title.render("Enter Exam Code", True, TEXT_BLACK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))

        box = pygame.Rect(SCREEN_WIDTH // 2 - 200, 320, 400, 90)
        pygame.draw.rect(self.screen, BORDER_GRAY, box, 2)

        display = self.code.ljust(MAX_CODE_LEN, "•")
        txt = self.font_code.render(display, True, TEXT_BLACK)
        self.screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 335))

        hint = self.font_hint.render(
            "Enter exam code • Press Enter",
            True, FG_GRAY
        )
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 440))

        if self.error:
            err = self.font_error.render(self.error, True, TEXT_BLACK)
            self.screen.blit(err, (SCREEN_WIDTH // 2 - err.get_width() // 2, 500))

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            self.draw()
            self.clock.tick(30)

        return self.exam_id, self.conn


# =========================================================
# STEP 2: STUDENT DETAILS
# =========================================================
class StudentDetailsScreen:
    def __init__(self, screen, conn, exam_id):
        self.screen = screen
        self.conn = conn
        self.exam_id = exam_id

        self.clock = pygame.time.Clock()
        self.running = True

        self.name = ""
        self.usn = ""
        self.active = "name"
        self.error = ""

        self.font_title = pygame.font.Font(None, 44)
        self.font_input = pygame.font.Font(None, 36)
        self.font_hint = pygame.font.Font(None, 26)

    def handle_key(self, key, uni):
        if key == pygame.K_TAB:
            self.active = "usn" if self.active == "name" else "name"

        elif key == pygame.K_BACKSPACE:
            if self.active == "name":
                self.name = self.name[:-1]
            else:
                self.usn = self.usn[:-1]

        elif key == pygame.K_RETURN:
            if not self.name or not self.usn:
                self.error = "All fields required"
                return

            cur = self.conn.execute(
                "INSERT INTO students (exam_id, name, usn) VALUES (?, ?, ?)",
                (self.exam_id, self.name.strip(), self.usn.strip())
            )
            self.conn.commit()
            self.student_id = cur.lastrowid
            self.running = False

        else:
            if uni.isprintable():
                if self.active == "name":
                    self.name += uni
                else:
                    self.usn += uni

    def draw_field(self, label, value, y, active):
        self.screen.blit(
            self.font_input.render(label, True, TEXT_BLACK), (120, y)
        )
        box = pygame.Rect(120, y + 40, 360, 56)
        pygame.draw.rect(self.screen, BORDER_GRAY, box, 2 if active else 1)
        self.screen.blit(
            self.font_input.render(value, True, TEXT_BLACK), (130, y + 52)
        )

    def draw(self):
        self.screen.fill(BG_WHITE)

        title = self.font_title.render("Student Details", True, TEXT_BLACK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 160))

        self.draw_field("Name", self.name, 260, self.active == "name")
        self.draw_field("USN", self.usn, 360, self.active == "usn")

        hint = self.font_hint.render(
            "TAB to switch • Enter to continue",
            True, FG_GRAY
        )
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 470))

        if self.error:
            err = self.font_hint.render(self.error, True, TEXT_BLACK)
            self.screen.blit(err, (SCREEN_WIDTH // 2 - err.get_width() // 2, 520))

        pygame.display.flip()

    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    self.handle_key(e.key, e.unicode)

            self.draw()
            self.clock.tick(30)

        return self.student_id


# =========================================================
# STEP 3: SIGNATURE CAPTURE
# =========================================================
class SignatureScreen:
    def __init__(self, screen, conn, student_id):
        self.screen = screen
        self.conn = conn
        self.student_id = student_id

        self.clock = pygame.time.Clock()
        self.running = True
        self.drawing = False

        self.canvas = pygame.Surface((500, 300))
        self.canvas.fill(BG_WHITE)

        self.font_title = pygame.font.Font(None, 40)
        self.font_btn = pygame.font.Font(None, 28)

    def draw(self):
        self.screen.fill(BG_WHITE)

        title = self.font_title.render("Sign Below", True, TEXT_BLACK)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        canvas_rect = pygame.Rect(50, 250, 500, 300)
        pygame.draw.rect(self.screen, BORDER_GRAY, canvas_rect, 2)
        self.screen.blit(self.canvas, (50, 250))

        clear_btn = pygame.Rect(150, 600, 120, 50)
        ok_btn = pygame.Rect(330, 600, 120, 50)

        pygame.draw.rect(self.screen, BORDER_GRAY, clear_btn, 2)
        pygame.draw.rect(self.screen, BORDER_GRAY, ok_btn, 2)

        self.screen.blit(self.font_btn.render("Clear", True, TEXT_BLACK),
                         (clear_btn.x + 30, clear_btn.y + 12))
        self.screen.blit(self.font_btn.render("Confirm", True, TEXT_BLACK),
                         (ok_btn.x + 20, ok_btn.y + 12))

        pygame.display.flip()
        return clear_btn, ok_btn

    def run(self):
        last_pos = None

        while self.running:
            clear_btn, ok_btn = self.draw()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if clear_btn.collidepoint(e.pos):
                        self.canvas.fill(BG_WHITE)

                    elif ok_btn.collidepoint(e.pos):
                        path = os.path.join(SIGNATURE_DIR, f"student_{self.student_id}.png")
                        pygame.image.save(self.canvas, path)

                        self.conn.execute(
                            "UPDATE students SET signature_path = ? WHERE student_id = ?",
                            (path, self.student_id)
                        )
                        self.conn.commit()
                        self.running = False

                    else:
                        self.drawing = True
                        last_pos = (e.pos[0] - 50, e.pos[1] - 250)

                elif e.type == pygame.MOUSEBUTTONUP:
                    self.drawing = False
                    last_pos = None

                elif e.type == pygame.MOUSEMOTION and self.drawing:
                    pos = (e.pos[0] - 50, e.pos[1] - 250)
                    if last_pos:
                        pygame.draw.line(self.canvas, TEXT_BLACK, last_pos, pos, 3)
                    last_pos = pos

            self.clock.tick(FPS)


# =========================================================
# ENTRY POINT
# =========================================================
def run():
    pygame.init()
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Abook Test")

    exam_id, conn = ExamCodeEntry(screen).run()
    student_id = StudentDetailsScreen(screen, conn, exam_id).run()
    SignatureScreen(screen, conn, student_id).run()

    # ✅ PAPER MODE ANSWER WRITING
    PaperAnswerScreen(
        screen,
        conn,
        exam_id,
        student_id
    ).run()

    print("✅ Exam completed for student:", student_id)
    conn.close()


if __name__ == "__main__":
    run()
