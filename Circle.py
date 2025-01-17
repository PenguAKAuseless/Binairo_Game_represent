import pygame
from constants import TRANSPARENT

class Circle(pygame.sprite.Sprite):
    def __init__(self, radius: int, color : tuple[int] = TRANSPARENT) -> None:
        """Create a circle with the given radius and color."""
        super().__init__()
        self.radius = radius
        diameter = 2 * radius
        self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()  # Initial rect centered at the top-left (0, 0)
    
    def set_position(self, x: int, y: int) -> None:
        """Position the circle so that its center is at (x, y)."""
        self.rect.center = (x, y)
    
    def color(self, color=TRANSPARENT):
        """Redraw the circle with the given color. Default is transparent."""
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
