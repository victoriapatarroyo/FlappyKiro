from dataclasses import dataclass
import pygame


@dataclass
class Actions:
    jump: bool = False
    quit: bool = False
    restart: bool = False


def process_events(events: list, game_state=None) -> Actions:
    """
    Mapea eventos pygame a Actions del dominio.
    - QUIT → quit=True
    - KEYDOWN K_SPACE o MOUSEBUTTONDOWN button=1 → jump=True
    - KEYDOWN K_ESCAPE → quit=True
    """
    actions = Actions()
    for event in events:
        if event.type == pygame.QUIT:
            actions.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                actions.jump = True
            elif event.key == pygame.K_ESCAPE:
                actions.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            actions.jump = True
    return actions
