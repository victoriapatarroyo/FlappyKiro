import pytest
from flappy_kiro.player import Player
from flappy_kiro.constants import GRAVITY, JUMP_VELOCITY, MAX_FALL_SPEED
from flappy_kiro.physics import apply_gravity, apply_jump, clamp_velocity, update_position


def make_player(**kwargs):
    return Player(image=None, **kwargs)


# --- apply_gravity ---

def test_apply_gravity_increases_velocity():
    p = make_player(velocity=0.0)
    result = apply_gravity(p)
    assert result.velocity == pytest.approx(GRAVITY)

def test_apply_gravity_does_not_mutate():
    p = make_player(velocity=2.0)
    apply_gravity(p)
    assert p.velocity == 2.0

def test_apply_gravity_returns_new_instance():
    p = make_player(velocity=0.0)
    result = apply_gravity(p)
    assert result is not p

def test_apply_gravity_preserves_position():
    p = make_player(x=80.0, y=200.0, velocity=1.0)
    result = apply_gravity(p)
    assert result.x == 80.0
    assert result.y == 200.0


# --- apply_jump ---

def test_apply_jump_sets_jump_velocity():
    p = make_player(velocity=5.0)
    result = apply_jump(p)
    assert result.velocity == pytest.approx(JUMP_VELOCITY)

def test_apply_jump_does_not_mutate():
    p = make_player(velocity=5.0)
    apply_jump(p)
    assert p.velocity == 5.0

def test_apply_jump_returns_new_instance():
    p = make_player(velocity=0.0)
    result = apply_jump(p)
    assert result is not p

def test_apply_jump_preserves_position():
    p = make_player(x=80.0, y=150.0, velocity=3.0)
    result = apply_jump(p)
    assert result.x == 80.0
    assert result.y == 150.0


# --- clamp_velocity ---

def test_clamp_velocity_above_max():
    p = make_player(velocity=15.0)
    result = clamp_velocity(p)
    assert result.velocity == pytest.approx(MAX_FALL_SPEED)

def test_clamp_velocity_at_max():
    p = make_player(velocity=MAX_FALL_SPEED)
    result = clamp_velocity(p)
    assert result.velocity == pytest.approx(MAX_FALL_SPEED)

def test_clamp_velocity_below_max():
    p = make_player(velocity=5.0)
    result = clamp_velocity(p)
    assert result.velocity == pytest.approx(5.0)

def test_clamp_velocity_negative():
    p = make_player(velocity=-8.0)
    result = clamp_velocity(p)
    assert result.velocity == pytest.approx(-8.0)

def test_clamp_velocity_does_not_mutate():
    p = make_player(velocity=20.0)
    clamp_velocity(p)
    assert p.velocity == 20.0


# --- update_position ---

def test_update_position_adds_velocity_to_y():
    p = make_player(y=100.0, velocity=5.0)
    result = update_position(p)
    assert result.y == pytest.approx(105.0)

def test_update_position_negative_velocity():
    p = make_player(y=100.0, velocity=-8.0)
    result = update_position(p)
    assert result.y == pytest.approx(92.0)

def test_update_position_does_not_mutate():
    p = make_player(y=100.0, velocity=3.0)
    update_position(p)
    assert p.y == 100.0

def test_update_position_preserves_x():
    p = make_player(x=80.0, y=100.0, velocity=2.0)
    result = update_position(p)
    assert result.x == pytest.approx(80.0)
