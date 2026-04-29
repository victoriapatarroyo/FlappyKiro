import pygame

from flappy_kiro.constants import SCREEN_WIDTH, SCREEN_HEIGHT

SKY_BLUE = (135, 206, 235)
PIPE_GREEN = (70, 160, 70)
PLAYER_YELLOW = (255, 220, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Renderer:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        self.screen = screen
        self.font = font

    def draw_start(self) -> None:
        self.screen.fill(SKY_BLUE)

        title = self.font.render("Flappy Kiro", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(title, title_rect)

        subtitle = self.font.render("Press Space or Click to Start", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(subtitle, subtitle_rect)

    def draw_playing(self, player, pipes, score: int) -> None:
        self.screen.fill(SKY_BLUE)

        for pipe in pipes:
            pygame.draw.rect(self.screen, PIPE_GREEN, pipe.top_rect)
            pygame.draw.rect(self.screen, PIPE_GREEN, pipe.bottom_rect)

        if player.image is not None:
            self.screen.blit(player.image, (int(player.x), int(player.y)))
        else:
            pygame.draw.rect(self.screen, PLAYER_YELLOW, player.rect)

        score_text = str(int(score))
        shadow = self.font.render(score_text, True, BLACK)
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 2, 42))
        self.screen.blit(shadow, shadow_rect)

        label = self.font.render(score_text, True, WHITE)
        label_rect = label.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(label, label_rect)

    def draw_game_over(self, score: int) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = self.font.render(f"Score: {int(score)}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        restart_text = self.font.render("Press Space or Click to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
