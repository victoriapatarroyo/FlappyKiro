from enum import Enum, auto
import sys
import pygame

from flappy_kiro.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
)
from flappy_kiro.player import Player
from flappy_kiro.pipe import Pipe
from flappy_kiro.physics import apply_gravity, apply_jump, clamp_velocity, update_position
from flappy_kiro.pipe_manager import spawn_pipe, move_pipes, remove_offscreen
from flappy_kiro.collision import check_any_collision, ScreenBounds
from flappy_kiro.score import update_score
from flappy_kiro.sound_manager import SoundManager
from flappy_kiro.input_handler import process_events
from flappy_kiro.renderer import Renderer


class GameState(Enum):
    START = auto()
    PLAYING = auto()
    GAME_OVER = auto()


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Kiro")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.renderer = Renderer(self.screen, self.font)
        self.sound_manager = SoundManager()
        # Solo procesar eventos relevantes, ignorar MOUSEMOTION para reducir lag
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
        pygame.mouse.set_visible(False)
        self._reset()

    def _reset(self) -> None:
        # Preserve the player image across resets (assigned externally from main.py)
        saved_image = getattr(self, "player", None)
        saved_image = saved_image.image if saved_image is not None else None

        self.player = Player()
        if saved_image is not None:
            self.player.image = saved_image

        self.pipes: list[Pipe] = []
        self.score: int = 0
        self.frame_count: int = 0
        self.state = GameState.START

    def run(self) -> None:
        bounds = ScreenBounds(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

        while True:
            events = pygame.event.get()
            actions = process_events(events)

            if self.state == GameState.START:
                self._handle_start(actions)
                self.renderer.draw_start()
            elif self.state == GameState.PLAYING:
                self._handle_playing(actions, bounds)
                self.renderer.draw_playing(self.player, self.pipes, self.score)
            elif self.state == GameState.GAME_OVER:
                self._handle_game_over(actions)
                self.renderer.draw_playing(self.player, self.pipes, self.score)
                self.renderer.draw_game_over(self.score)

            pygame.display.flip()
            self.clock.tick(FPS)

    def _handle_start(self, actions) -> None:
        if actions.quit:
            pygame.quit()
            sys.exit(0)
        if actions.jump:
            self.state = GameState.PLAYING

    def _handle_playing(self, actions, bounds: ScreenBounds) -> None:
        if actions.quit:
            pygame.quit()
            sys.exit(0)
        if actions.jump:
            self.player = apply_jump(self.player)
            self.sound_manager.play_jump()

        # Physics
        self.player = apply_gravity(self.player)
        self.player = clamp_velocity(self.player)
        self.player = update_position(self.player)

        self.frame_count += 1

        # Pipe lifecycle
        new_pipe = spawn_pipe(self.frame_count, SCREEN_WIDTH)
        if new_pipe is not None:
            self.pipes.append(new_pipe)
        self.pipes = move_pipes(self.pipes)
        self.pipes = remove_offscreen(self.pipes)

        # Score
        self.score, self.pipes = update_score(self.score, self.player, self.pipes)

        # Collision
        if check_any_collision(self.player, self.pipes, bounds):
            self.state = GameState.GAME_OVER
            self.sound_manager.play_game_over()

    def _handle_game_over(self, actions) -> None:
        if actions.quit:
            pygame.quit()
            sys.exit(0)
        if actions.restart or actions.jump:
            self._reset()
