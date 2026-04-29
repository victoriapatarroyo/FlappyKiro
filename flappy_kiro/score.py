import dataclasses

from flappy_kiro.player import Player
from flappy_kiro.pipe import Pipe


def update_score(score: int, player: Player, pipes: list[Pipe]) -> tuple[int, list[Pipe]]:
    updated_pipes = []
    for pipe in pipes:
        if pipe.x + pipe.width < player.x and not pipe.passed:
            score += 1
            pipe = dataclasses.replace(pipe, passed=True)
        updated_pipes.append(pipe)
    return score, updated_pipes
