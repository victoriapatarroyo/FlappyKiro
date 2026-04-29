"""
Entry point para Pygbag (WebAssembly / browser).

Pygbag requiere que el bucle principal sea una corrutina async con
`await asyncio.sleep(0)` en cada frame para ceder el control al
event loop del browser.
"""
import asyncio
import os
import sys

import pygame

from flappy_kiro.game import Game, GameState
from flappy_kiro.physics import apply_gravity, apply_jump, clamp_velocity, update_position
from flappy_kiro.pipe_manager import spawn_pipe, move_pipes, remove_offscreen
from flappy_kiro.collision import check_any_collision, ScreenBounds
from flappy_kiro.score import update_score
from flappy_kiro.input_handler import process_events
from flappy_kiro.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def load_assets(game: Game) -> None:
    """Carga imagen y sonidos. En WASM los paths son relativos al bundle."""
    image_path = "assets/ghosty.png"
    if os.path.exists(image_path):
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (34, 34))
        game.player.image = image

    # El audio puede no estar disponible en todos los browsers
    try:
        game.sound_manager.load("assets/jump.wav", "assets/game_over.wav")
    except Exception:
        pass  # Continuar sin audio si el browser lo bloquea


async def main() -> None:
    """Bucle principal async compatible con Pygbag."""
    game = Game()
    load_assets(game)

    bounds = ScreenBounds(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    while True:
        events = pygame.event.get()
        actions = process_events(events)

        if game.state == GameState.START:
            game._handle_start(actions)
            game.renderer.draw_start()

        elif game.state == GameState.PLAYING:
            game._handle_playing(actions, bounds)
            game.renderer.draw_playing(game.player, game.pipes, game.score)

        elif game.state == GameState.GAME_OVER:
            game._handle_game_over(actions)
            game.renderer.draw_playing(game.player, game.pipes, game.score)
            game.renderer.draw_game_over(game.score)

        pygame.display.flip()
        game.clock.tick(FPS)

        # Ceder control al event loop del browser en cada frame
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
