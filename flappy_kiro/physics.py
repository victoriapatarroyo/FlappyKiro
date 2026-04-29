from dataclasses import replace

from flappy_kiro.player import Player
from flappy_kiro.constants import GRAVITY, JUMP_VELOCITY, MAX_FALL_SPEED


def apply_gravity(player: Player) -> Player:
    """Retorna un nuevo Player con velocity incrementada en GRAVITY."""
    return replace(player, velocity=player.velocity + GRAVITY)


def apply_jump(player: Player) -> Player:
    """Retorna un nuevo Player con velocity = JUMP_VELOCITY."""
    return replace(player, velocity=JUMP_VELOCITY)


def clamp_velocity(player: Player) -> Player:
    """Retorna un nuevo Player con velocity limitada a MAX_FALL_SPEED."""
    return replace(player, velocity=min(player.velocity, MAX_FALL_SPEED))


def update_position(player: Player) -> Player:
    """Retorna un nuevo Player con y incrementada en velocity."""
    return replace(player, y=player.y + player.velocity)
