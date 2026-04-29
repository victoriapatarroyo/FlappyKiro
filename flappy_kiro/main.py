import os
import sys
import pygame
from flappy_kiro.game import Game


def load_assets(game: Game) -> None:
    """
    Carga assets/ghosty.png como imagen del player (escalada a 34x34).
    Carga los sonidos via game.sound_manager.load().
    Lanza FileNotFoundError si el archivo de imagen no existe.
    """
    image_path = "assets/ghosty.png"
    if not os.path.exists(image_path):
        raise FileNotFoundError(image_path)

    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (34, 34))
    game.player.image = image

    game.sound_manager.load("assets/jump.wav", "assets/game_over.wav")


def main() -> None:
    """Entry point principal."""
    try:
        game = Game()
        load_assets(game)
        game.run()
    except FileNotFoundError as e:
        print(f"Error: No se encontró un archivo requerido: {e}")
        sys.exit(1)
    except pygame.error as e:
        print(f"Error de pygame: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
