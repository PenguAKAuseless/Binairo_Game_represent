import pygame
from Circle import Circle

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Draw Circles")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create circles
circle1 = Circle(1, (0, 0), RED)
circle2 = Circle(60, (500, 400), BLUE)

# Main loop
running = True
all_sprites = pygame.sprite.Group(circle1, circle2)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    window.fill(WHITE)

    # Draw circles
    all_sprites.draw(window)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()