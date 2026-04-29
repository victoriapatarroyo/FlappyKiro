import pytest
from flappy_kiro.player import Player
from flappy_kiro.pipe import Pipe
from flappy_kiro.score import update_score


def make_player(x: float = 100.0) -> Player:
    return Player(x=x, y=300.0)


def make_pipe(x: float, width: int = 60, passed: bool = False) -> Pipe:
    return Pipe(x=x, gap_center_y=300.0, width=width, passed=passed)


def test_pipe_passed_increments_score():
    # pipe.x + pipe.width (30 + 60 = 90) < player.x (100), passed=False → score +1
    player = make_player(x=100.0)
    pipe = make_pipe(x=30.0)
    new_score, new_pipes = update_score(0, player, [pipe])
    assert new_score == 1
    assert new_pipes[0].passed is True


def test_pipe_already_passed_no_score_change():
    # pipe already marked passed → score unchanged
    player = make_player(x=100.0)
    pipe = make_pipe(x=30.0, passed=True)
    new_score, new_pipes = update_score(5, player, [pipe])
    assert new_score == 5
    assert new_pipes[0].passed is True


def test_pipe_not_yet_passed_no_score_change():
    # pipe.x + pipe.width (80 + 60 = 140) >= player.x (100) → score unchanged
    player = make_player(x=100.0)
    pipe = make_pipe(x=80.0)
    new_score, new_pipes = update_score(3, player, [pipe])
    assert new_score == 3
    assert new_pipes[0].passed is False


def test_multiple_pipes_passed_in_one_frame():
    player = make_player(x=200.0)
    pipes = [
        make_pipe(x=10.0),   # 10+60=70 < 200, passed=False → +1
        make_pipe(x=50.0),   # 50+60=110 < 200, passed=False → +1
        make_pipe(x=150.0),  # 150+60=210 >= 200 → no change
    ]
    new_score, new_pipes = update_score(0, player, pipes)
    assert new_score == 2
    assert new_pipes[0].passed is True
    assert new_pipes[1].passed is True
    assert new_pipes[2].passed is False


def test_empty_pipe_list_no_score_change():
    player = make_player(x=100.0)
    new_score, new_pipes = update_score(7, player, [])
    assert new_score == 7
    assert new_pipes == []
