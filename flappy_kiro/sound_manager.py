import logging
import pygame


class SoundManager:
    def __init__(self):
        self._jump_sound = None
        self._game_over_sound = None

    def load(self, jump_path: str, game_over_path: str) -> None:
        """Carga los sonidos. Si falla, loggea advertencia y continúa sin audio."""
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except pygame.error as e:
                logging.warning(f"No se pudo inicializar el mixer de audio: {e}")
                return

        try:
            self._jump_sound = pygame.mixer.Sound(jump_path)
        except (pygame.error, FileNotFoundError) as e:
            logging.warning(f"No se pudo cargar el sonido de salto '{jump_path}': {e}")

        try:
            self._game_over_sound = pygame.mixer.Sound(game_over_path)
        except (pygame.error, FileNotFoundError) as e:
            logging.warning(f"No se pudo cargar el sonido de game over '{game_over_path}': {e}")

    def play_jump(self) -> None:
        """Reproduce el sonido de salto si fue cargado."""
        if self._jump_sound is not None:
            self._jump_sound.play()

    def play_game_over(self) -> None:
        """Reproduce el sonido de game over si fue cargado."""
        if self._game_over_sound is not None:
            self._game_over_sound.play()
