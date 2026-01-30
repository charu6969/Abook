"""
Boot sequence animation for ABook application
"""
import pygame
import sys
import random
import math
from config import *


def generate_logo_positions(scale=8):
    """Generate pixel positions for the ABOOK logo - FOR PORTRAIT"""
    positions = []
    x_offset = 0
    letter_spacing = 20  # Increased spacing between letters
    
    # Use portrait dimensions (600x1024)
    portrait_width = 600
    portrait_height = 1024
    
    for char in "ABOOK":
        letter = LETTERS[char]
        for row_idx, row in enumerate(letter):
            for col_idx, pixel in enumerate(row):
                if pixel == '#':
                    positions.append((x_offset + col_idx * scale, row_idx * scale))
        
        # Add spacing after each letter
        x_offset += len(letter[0]) * scale + letter_spacing
    
    # Center the logo in PORTRAIT dimensions
    min_x = min(p[0] for p in positions)
    max_x = max(p[0] for p in positions)
    min_y = min(p[1] for p in positions)
    max_y = max(p[1] for p in positions)
    
    offset_x = (portrait_width - (max_x - min_x)) // 2 - min_x
    offset_y = (portrait_height - (max_y - min_y)) // 2 - min_y
    
    return [(p[0] + offset_x, p[1] + offset_y) for p in positions]


class Particle:
    """Particle for boot animation"""
    def __init__(self, target):
        # Use portrait dimensions
        self.start = (random.randint(0, 600), random.randint(0, 1024))
        self.target = target
        self.pos = list(self.start)
        
        # Calculate dispersion target
        angle = random.uniform(0, 2 * math.pi)
        dist = random.randint(300, 600)
        self.disperse = (
            target[0] + math.cos(angle) * dist,
            target[1] + math.sin(angle) * dist
        )

    def update(self, elapsed):
        """Update particle position based on elapsed time"""
        if elapsed < FORMATION_DURATION:
            # Formation phase
            t = elapsed / FORMATION_DURATION
            self.pos = [
                self.start[i] + (self.target[i] - self.start[i]) * t
                for i in range(2)
            ]
        elif elapsed > FORMATION_DURATION + HOLD_DURATION:
            # Dispersion phase
            t = min(1, (elapsed - FORMATION_DURATION - HOLD_DURATION) / DISPERSE_DURATION)
            self.pos = [
                self.target[i] + (self.disperse[i] - self.target[i]) * t
                for i in range(2)
            ]

    def draw(self, screen):
        """Draw the particle"""
        pygame.draw.circle(
            screen,
            COLOR_BLACK,
            (int(self.pos[0]), int(self.pos[1])),
            4  # Increased from 3 to 4 for better visibility
        )


def run_boot_sequence(screen, clock):
    """Run the boot animation sequence - rotated 90° counter-clockwise"""
    targets = generate_logo_positions()
    # Create more particles for better logo formation
    particles = [Particle(targets[i % len(targets)]) for i in range(800)]
    start_ticks = pygame.time.get_ticks()
    
    # Create portrait surface for boot animation
    portrait_surface = pygame.Surface((600, 1024))
    
    while True:
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
        if elapsed > TOTAL_BOOT_TIME:
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # Draw to portrait surface
        portrait_surface.fill(COLOR_WHITE)
        
        for particle in particles:
            particle.update(elapsed)
            particle.draw(portrait_surface)
        
        # Rotate 90° counter-clockwise
        rotated = pygame.transform.rotate(portrait_surface, 90)
        
        # After rotation: 1024×600 - perfect fit!
        screen.fill((0, 0, 0))
        screen.blit(rotated, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
        