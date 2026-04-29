from dataclasses import dataclass

from flappy_kiro.player import Player
from flappy_kiro.pipe import Pipe


@dataclass
class ScreenBounds:
    width: int
    height: int


def check_pipe_collision(player: Player, pipes: list[Pipe]) -> bool:
    player_rect = player.rect
    for pipe in pipes:
        if player_rect.colliderect(pipe.top_rect) or player_rect.colliderect(pipe.bottom_rect):
            return True
    return False


def check_boundary_collision(player: Player, bounds: ScreenBounds) -> bool:
    rect = player.rect
    return rect.top < 0 or rect.bottom > bounds.height


def check_any_collision(player: Player, pipes: list[Pipe], bounds: ScreenBounds) -> bool:
    return check_pipe_collision(player, pipes) or check_boundary_collision(player, bounds)
