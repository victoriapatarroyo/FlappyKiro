from dataclasses import dataclass
import pygame

from flappy_kiro.constants import SCREEN_HEIGHT


@dataclass
class Pipe:
    x: float
    gap_center_y: float
    gap_height: float = 150.0
    width: int = 60
    passed: bool = False

    @property
    def top_rect(self) -> pygame.Rect:
        top_height = int(self.gap_center_y - self.gap_height / 2)
        return pygame.Rect(int(self.x), 0, self.width, max(0, top_height))

    @property
    def bottom_rect(self) -> pygame.Rect:
        bottom_y = int(self.gap_center_y + self.gap_height / 2)
        return pygame.Rect(int(self.x), bottom_y, self.width, max(0, SCREEN_HEIGHT - bottom_y))
