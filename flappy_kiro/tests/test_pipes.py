import pytest

from flappy_kiro.constants import GAP_MAX_Y, GAP_MIN_Y, PIPE_SPEED
from flappy_kiro.pipe import Pipe
from flappy_kiro.pipe_manager import move_pipes, remove_offscreen, spawn_pipe

SCREEN_WIDTH = 400


# --- spawn_pipe ---

def test_spawn_pipe_returns_none_on_non_multiple_frames():
    assert spawn_pipe(0, SCREEN_WIDTH) is None
    assert spawn_pipe(1, SCREEN_WIDTH) is None
    assert spawn_pipe(45, SCREEN_WIDTH) is None
    assert spawn_pipe(89, SCREEN_WIDTH) is None
    assert spawn_pipe(91, SCREEN_WIDTH) is None


def test_spawn_pipe_returns_pipe_on_multiple_of_90():
    for frame in (90, 180, 270):
        pipe = spawn_pipe(frame, SCREEN_WIDTH)
        assert pipe is not None, f"Expected Pipe at frame {frame}"
        assert isinstance(pipe, Pipe)


def test_spawn_pipe_gap_center_y_in_range():
    for _ in range(50):
        pipe = spawn_pipe(90, SCREEN_WIDTH)
        assert pipe is not None
        assert GAP_MIN_Y <= pipe.gap_center_y <= GAP_MAX_Y


def test_spawn_pipe_x_equals_screen_width():
    pipe = spawn_pipe(90, SCREEN_WIDTH)
    assert pipe is not None
    assert pipe.x == float(SCREEN_WIDTH)


# --- move_pipes ---

def test_move_pipes_shifts_each_pipe_left_by_pipe_speed():
    pipes = [Pipe(x=100.0, gap_center_y=300.0), Pipe(x=250.0, gap_center_y=200.0)]
    moved = move_pipes(pipes)
    for original, updated in zip(pipes, moved):
        assert updated.x == pytest.approx(original.x - PIPE_SPEED)


def test_move_pipes_does_not_mutate_original_list():
    pipes = [Pipe(x=100.0, gap_center_y=300.0)]
    original_x = pipes[0].x
    move_pipes(pipes)
    assert pipes[0].x == original_x


def test_move_pipes_returns_new_list():
    pipes = [Pipe(x=100.0, gap_center_y=300.0)]
    moved = move_pipes(pipes)
    assert moved is not pipes


def test_move_pipes_preserves_other_fields():
    pipe = Pipe(x=100.0, gap_center_y=300.0, gap_height=150.0, width=60)
    moved = move_pipes([pipe])
    assert moved[0].gap_center_y == pipe.gap_center_y
    assert moved[0].gap_height == pipe.gap_height
    assert moved[0].width == pipe.width


# --- remove_offscreen ---

def test_remove_offscreen_removes_pipes_past_left_edge():
    # x + width < 0  →  debe eliminarse
    pipe = Pipe(x=-70.0, gap_center_y=300.0, width=60)  # -70 + 60 = -10 < 0
    result = remove_offscreen([pipe])
    assert result == []


def test_remove_offscreen_keeps_pipes_on_screen():
    pipe = Pipe(x=0.0, gap_center_y=300.0, width=60)  # 0 + 60 = 60 >= 0
    result = remove_offscreen([pipe])
    assert len(result) == 1


def test_remove_offscreen_keeps_partially_visible_pipes():
    pipe = Pipe(x=-59.0, gap_center_y=300.0, width=60)  # -59 + 60 = 1 >= 0
    result = remove_offscreen([pipe])
    assert len(result) == 1


def test_remove_offscreen_mixed_list():
    on_screen = Pipe(x=100.0, gap_center_y=300.0, width=60)
    off_screen = Pipe(x=-70.0, gap_center_y=300.0, width=60)
    result = remove_offscreen([on_screen, off_screen])
    assert len(result) == 1
    assert result[0].x == 100.0
