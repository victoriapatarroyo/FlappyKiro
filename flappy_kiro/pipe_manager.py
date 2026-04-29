import dataclasses
import random

from flappy_kiro.constants import (
    GAP_HEIGHT,
    GAP_MAX_Y,
    GAP_MIN_Y,
    PIPE_SPAWN_INTERVAL,
    PIPE_SPEED,
)
from flappy_kiro.pipe import Pipe


def spawn_pipe(frame_count: int, screen_width: int) -> Pipe | None:
    """Genera un tubo si frame_count % PIPE_SPAWN_INTERVAL == 0 (y frame_count > 0)."""
    if frame_count > 0 and frame_count % PIPE_SPAWN_INTERVAL == 0:
        gap_center_y = random.uniform(GAP_MIN_Y, GAP_MAX_Y)
        return Pipe(x=float(screen_width), gap_center_y=gap_center_y, gap_height=GAP_HEIGHT)
    return None


def move_pipes(pipes: list[Pipe]) -> list[Pipe]:
    """Devuelve una nueva lista con cada tubo desplazado PIPE_SPEED píxeles a la izquierda."""
    return [dataclasses.replace(pipe, x=pipe.x - PIPE_SPEED) for pipe in pipes]


def remove_offscreen(pipes: list[Pipe]) -> list[Pipe]:
    """Devuelve una nueva lista sin los tubos donde pipe.x + pipe.width < 0."""
    return [pipe for pipe in pipes if pipe.x + pipe.width >= 0]
