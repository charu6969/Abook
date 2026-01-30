import pygame
import sys
import os
import random
import math

DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 1024
BACKGROUND_COLOR = (255, 255, 255)
PARTICLE_COLOR = (0, 0, 0)
FPS = 60

FORMATION_DURATION = 2.0
HOLD_DURATION = 1.5
DISPERSE_DURATION = 2.0
TOTAL_DURATION = FORMATION_DURATION + HOLD_DURATION + DISPERSE_DURATION

PARTICLE_SIZE = 3
NUM_PARTICLES = 800

USE_FRAMEBUFFER = len(sys.argv) > 1 and sys.argv[1] == '--fb'

LETTER_A = [
    "   ####   ",
    "  ##  ##  ",
    " ##    ## ",
    " ##    ## ",
    " ######## ",
    "##      ##",
    "##      ##",
    "##      ##",
    "##      ##"
]

LETTER_B = [
    "###### ",
    "#     #",
    "#     #",
    "###### ",
    "#     #",
    "#     #",
    "###### "
]

LETTER_O = [
    " ##### ",
    "#     #",
    "#     #",
    "#     #",
    "#     #",
    "#     #",
    " ##### "
]

LETTER_K = [
    "#    # ",
    "#   #  ",
    "#  #   ",
    "###    ",
    "#  #   ",
    "#   #  ",
    "#    # "
]

LETTERS = {
    'A': LETTER_A,
    'B': LETTER_B,
    'O': LETTER_O,
    'K': LETTER_K
}


def ease_in_out_cubic(t):
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - pow(-2 * t + 2, 3) / 2


def ease_out_quad(t):
    return 1 - (1 - t) * (1 - t)


def generate_text_positions(word, scale=5, letter_spacing=10):
    positions = []
    x_offset = 0
    
    max_letter_height = max(len(LETTERS[char]) for char in word.upper() if char in LETTERS)
    
    for char in word.upper():
        if char in LETTERS:
            letter = LETTERS[char]
            letter_height = len(letter)
            
            y_offset = max_letter_height - letter_height
            
            for row_idx, row in enumerate(letter):
                for col_idx, pixel in enumerate(row):
                    if pixel == '#':
                        x = x_offset + col_idx * scale
                        y = (row_idx + y_offset) * scale
                        positions.append((x, y))
            
            x_offset += len(letter[0]) * scale + letter_spacing
    
    if not positions:
        return positions
    
    min_x = min(p[0] for p in positions)
    max_x = max(p[0] for p in positions)
    min_y = min(p[1] for p in positions)
    max_y = max(p[1] for p in positions)
    
    text_width = max_x - min_x
    text_height = max_y - min_y
    
    center_x = DISPLAY_WIDTH / 2
    center_y = DISPLAY_HEIGHT / 2
    
    offset_x = center_x - text_width / 2 - min_x
    offset_y = center_y - text_height / 2 - min_y
    
    centered_positions = [(p[0] + offset_x, p[1] + offset_y) for p in positions]
    
    return centered_positions


class Particle:
    def __init__(self, start_pos, target_pos):
        self.start_x = start_pos[0]
        self.start_y = start_pos[1]
        self.target_x = target_pos[0]
        self.target_y = target_pos[1]
        self.x = self.start_x
        self.y = self.start_y
        
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(100, 300)
        self.disperse_x = self.target_x + math.cos(angle) * distance
        self.disperse_y = self.target_y + math.sin(angle) * distance
    
    def update(self, elapsed_time):
        if elapsed_time < FORMATION_DURATION:
            t = elapsed_time / FORMATION_DURATION
            t = ease_in_out_cubic(t)
            self.x = self.start_x + (self.target_x - self.start_x) * t
            self.y = self.start_y + (self.target_y - self.start_y) * t
        elif elapsed_time < FORMATION_DURATION + HOLD_DURATION:
            self.x = self.target_x
            self.y = self.target_y
        else:
            t = (elapsed_time - FORMATION_DURATION - HOLD_DURATION) / DISPERSE_DURATION
            t = min(t, 1.0)
            t = ease_out_quad(t)
            self.x = self.target_x + (self.disperse_x - self.target_x) * t
            self.y = self.target_y + (self.disperse_y - self.target_y) * t
    
    def draw(self, surface):
        pygame.draw.circle(surface, PARTICLE_COLOR, (int(self.x), int(self.y)), PARTICLE_SIZE)


class BootAnimation:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        
        if USE_FRAMEBUFFER:
            os.environ['SDL_VIDEODRIVER'] = 'fbcon'
            os.environ['SDL_FBDEV'] = '/dev/fb0'
            self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
        else:
            os.environ['SDL_VIDEODRIVER'] = 'x11'
            self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        
        pygame.display.set_caption('Abook OS Boot')
        
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        
        target_positions = generate_text_positions('Abook', scale=5, letter_spacing=10)
        
        if not target_positions:
            target_positions = [(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)]
        
        self.particles = []
        for i in range(NUM_PARTICLES):
            start_x = random.uniform(0, DISPLAY_WIDTH)
            start_y = random.uniform(0, DISPLAY_HEIGHT)
            target_pos = target_positions[i % len(target_positions)]
            self.particles.append(Particle((start_x, start_y), target_pos))
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0
            
            if elapsed_time >= TOTAL_DURATION:
                running = False
            
            self.screen.fill(BACKGROUND_COLOR)
            
            for particle in self.particles:
                particle.update(elapsed_time)
                particle.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()


if __name__ == '__main__':
    animation = BootAnimation()
    animation.run()
