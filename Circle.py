import pygame
from constants import TRANSPARENT

class Circle(pygame.sprite.Sprite):
    def __init__(self, radius: int, position: tuple[int] = (0, 0), color : tuple[int] = TRANSPARENT) -> None:
        """Create a circle with the given radius and color."""
        super().__init__()
        self.radius = radius
        self.color = color
        diameter = 2 * radius
        self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()  # Initial rect centered at the top-left (0, 0)
        self.set_position(position)

    def set_position(self, position: tuple[int]) -> None:
        """Position the circle so that its center is at (x, y)."""
        self.rect.center = position
    
    def set_color(self, color: tuple[int] = TRANSPARENT) -> None:
        """Redraw the circle with the given color."""
        self.image.fill(TRANSPARENT)  # Clear the image with transparency
        self.color = color
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)

    def update(self, pos: tuple[int] = None, color: tuple[int] = None) -> None:
        """Update the circle's position and color."""
        if pos:  # Only set position if a new one is provided
            self.set_position(pos)
        if color:  # Only update color if a new one is provided
            self.set_color(color)