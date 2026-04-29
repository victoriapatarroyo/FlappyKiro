from dataclasses import dataclass, field
import pygame


@dataclass
class Player:
    x: float = 80.0
    y: float = 300.0
    velocity: float = 0.0
    image: pygame.Surface = field(default=None, repr=False)

    @property
    def rect(self) -> pygame.Rect:
        if self.image is not None:
            w, h = self.image.get_size()
        else:
            w, h = 34, 24
        return pygame.Rect(int(self.x), int(self.y), w, h)
