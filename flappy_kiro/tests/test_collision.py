"""
Unit tests for collision detection (Requirements 4.1, 4.2, 4.3, 4.4).
No pygame.init() required — Rect objects are created directly.
"""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from flappy_kiro.player import Player
from flappy_kiro.pipe import Pipe
from flappy_kiro.collision import ScreenBounds, check_pipe_collision, check_boundary_collision, check_any_collision

BOUNDS = ScreenBounds(width=400, height=600)

# Player with image=None uses 34×24 hitbox.
# Default player: x=80, y=300 → rect = Rect(80, 300, 34, 24)


def make_player(x: float = 80.0, y: float = 300.0) -> Player:
    return Player(x=x, y=y, image=None)


def make_pipe(x: float, gap_center_y: float, gap_height: float = 150.0) -> Pipe:
    return Pipe(x=x, gap_center_y=gap_center_y, gap_height=gap_height)


# ---------------------------------------------------------------------------
# check_pipe_collision
# ---------------------------------------------------------------------------

def test_collision_with_top_pipe():
    """Player overlaps the top pipe rect → collision detected."""
    # top_rect for gap_center_y=300, gap_height=150: Rect(x, 0, 60, 225)
    # Player at y=200 (rect bottom = 224) overlaps top pipe bottom (225)
    player = make_player(x=100, y=200)
    pipe = make_pipe(x=100, gap_center_y=300)
    assert check_pipe_collision(player, [pipe]) is True


def test_collision_with_bottom_pipe():
    """Player overlaps the bottom pipe rect → collision detected."""
    # bottom_rect for gap_center_y=300, gap_height=150: starts at y=375
    # Player at y=370 (rect bottom = 394) overlaps bottom pipe top (375)
    player = make_player(x=100, y=370)
    pipe = make_pipe(x=100, gap_center_y=300)
    assert check_pipe_collision(player, [pipe]) is True


def test_no_collision_player_in_gap():
    """Player is fully inside the gap → no collision."""
    # gap: 225 to 375 for gap_center_y=300, gap_height=150
    # Player at y=280 → rect = Rect(100, 280, 34, 24), bottom=304 — inside gap
    player = make_player(x=100, y=280)
    pipe = make_pipe(x=100, gap_center_y=300)
    assert check_pipe_collision(player, [pipe]) is False


def test_no_collision_player_not_at_pipe_x():
    """Player is horizontally far from the pipe → no collision."""
    player = make_player(x=300, y=300)
    pipe = make_pipe(x=0, gap_center_y=300)
    assert check_pipe_collision(player, [pipe]) is False


def test_no_collision_empty_pipe_list():
    """No pipes → no collision."""
    player = make_player()
    assert check_pipe_collision(player, []) is False


# ---------------------------------------------------------------------------
# check_boundary_collision
# ---------------------------------------------------------------------------

def test_boundary_collision_bottom():
    """Player exits through the bottom edge → collision detected."""
    # Player rect bottom = y + 24; set y so bottom > 600
    player = make_player(x=80, y=580)  # bottom = 604 > 600
    assert check_boundary_collision(player, BOUNDS) is True


def test_boundary_collision_top():
    """Player exits through the top edge → collision detected."""
    player = make_player(x=80, y=-5)  # top = -5 < 0
    assert check_boundary_collision(player, BOUNDS) is True


def test_no_boundary_collision_inside_screen():
    """Player fully inside screen bounds → no boundary collision."""
    player = make_player(x=80, y=300)  # top=300, bottom=324 — well inside 600
    assert check_boundary_collision(player, BOUNDS) is False


def test_boundary_collision_exactly_at_top():
    """Player rect.top == 0 → no collision (boundary is strict <)."""
    player = make_player(x=80, y=0)  # top = 0, not < 0
    assert check_boundary_collision(player, BOUNDS) is False


def test_boundary_collision_exactly_at_bottom():
    """Player rect.bottom == height → no collision (boundary is strict >)."""
    # rect.bottom = y + 24 = height → y = 576
    player = make_player(x=80, y=576)  # bottom = 600, not > 600
    assert check_boundary_collision(player, BOUNDS) is False


# ---------------------------------------------------------------------------
# check_any_collision
# ---------------------------------------------------------------------------

def test_any_collision_detects_pipe():
    """check_any_collision returns True when pipe collision occurs."""
    player = make_player(x=100, y=200)
    pipe = make_pipe(x=100, gap_center_y=300)
    assert check_any_collision(player, [pipe], BOUNDS) is True


def test_any_collision_detects_boundary():
    """check_any_collision returns True when boundary collision occurs."""
    player = make_player(x=80, y=590)  # bottom = 614 > 600
    assert check_any_collision(player, [], BOUNDS) is True


def test_any_collision_no_collision():
    """Player inside screen with no pipes → no collision."""
    player = make_player(x=80, y=300)
    assert check_any_collision(player, [], BOUNDS) is False
