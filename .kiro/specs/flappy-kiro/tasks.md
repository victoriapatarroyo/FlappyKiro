# Implementation Plan: Flappy Kiro

## Overview

Implementación incremental de Flappy Kiro en Python con pygame. Se construye de abajo hacia arriba: primero las estructuras de datos y constantes, luego la física y los tubos, después la detección de colisiones y puntuación, y finalmente el coordinador principal con renderizado y audio. Cada módulo se valida con tests antes de continuar.

## Tasks

- [x] 1. Configurar estructura del proyecto y constantes
  - Crear el directorio `flappy_kiro/` con todos los módulos vacíos (`__init__.py`, `constants.py`, `player.py`, `pipe.py`, `physics.py`, `pipe_manager.py`, `collision.py`, `score.py`, `sound_manager.py`, `input_handler.py`, `renderer.py`, `game.py`, `main.py`) y el directorio `flappy_kiro/tests/`
  - Crear `constants.py` con todas las constantes globales: `SCREEN_WIDTH=400`, `SCREEN_HEIGHT=600`, `FPS=60`, `PLAYER_X=80.0`, `GRAVITY=0.5`, `JUMP_VELOCITY=-8.0`, `MAX_FALL_SPEED=10.0`, `PIPE_SPEED=3.0`, `PIPE_SPAWN_INTERVAL=90`, `GAP_HEIGHT=150.0`, `GAP_MIN_Y=150`, `GAP_MAX_Y=450`
  - Crear `requirements.txt` con `pygame>=2.0` y `pytest` y `hypothesis`
  - _Requirements: 1.1, 2.1, 2.2, 2.5, 3.1, 3.2, 3.3, 3.4, 7.1_

- [x] 2. Implementar modelos de datos: Player y Pipe
  - [x] 2.1 Implementar dataclass `Player` en `player.py`
    - Campos: `x: float = 80.0`, `y: float = 300.0`, `velocity: float = 0.0`, `image: pygame.Surface = None`
    - Propiedad `rect` que devuelve `pygame.Rect` basado en `(x, y)` y dimensiones de la imagen (o fallback 34×24)
    - _Requirements: 2.4, 4.4_

  - [x] 2.2 Implementar dataclass `Pipe` en `pipe.py`
    - Campos: `x: float`, `gap_center_y: float`, `gap_height: float = 150.0`, `width: int = 60`, `passed: bool = False`
    - Propiedades `top_rect` y `bottom_rect` que devuelven `pygame.Rect` para cada tubo
    - _Requirements: 3.3, 4.4_

- [x] 3. Implementar PhysicsEngine
  - [x] 3.1 Implementar funciones puras en `physics.py`
    - `apply_gravity(player) -> Player`: incrementa `velocity` en `GRAVITY`
    - `apply_jump(player) -> Player`: establece `velocity = JUMP_VELOCITY`
    - `clamp_velocity(player) -> Player`: limita `velocity` a `MAX_FALL_SPEED`
    - `update_position(player) -> Player`: suma `velocity` a `y`
    - _Requirements: 2.1, 2.2, 2.4, 2.5_

  - [ ]* 3.2 Escribir property test: Property 1 — La gravedad incrementa la velocidad de forma constante
    - **Property 1: La gravedad incrementa la velocidad de forma constante**
    - **Validates: Requirements 2.1**
    - Usar `@given(floats, floats)` para velocidad e `y` iniciales arbitrarios; verificar `updated.velocity == initial_velocity + GRAVITY`

  - [ ]* 3.3 Escribir property test: Property 2 — El salto establece la velocidad a -8
    - **Property 2: El salto establece la velocidad a -8**
    - **Validates: Requirements 2.2**
    - Usar `@given(floats, floats)` para cualquier estado inicial; verificar `updated.velocity == JUMP_VELOCITY`

  - [ ]* 3.4 Escribir property test: Property 3 — La posición horizontal del jugador es siempre 80
    - **Property 3: La posición horizontal del jugador es siempre 80**
    - **Validates: Requirements 2.4**
    - Aplicar secuencias arbitrarias de gravedad, salto y `update_position`; verificar `player.x == 80.0` en todo momento

  - [ ]* 3.5 Escribir property test: Property 4 — La velocidad vertical nunca supera el máximo de caída
    - **Property 4: La velocidad vertical nunca supera el máximo de caída**
    - **Validates: Requirements 2.5**
    - Usar `@given(floats)` para velocidades arbitrarias (incluyendo > 10); verificar `clamped.velocity <= MAX_FALL_SPEED`

  - [ ]* 3.6 Escribir tests unitarios para `physics.py`
    - Casos concretos: gravedad desde velocidad 0, salto desde velocidad positiva, clamp en exactamente 10, `update_position` suma correctamente
    - _Requirements: 2.1, 2.2, 2.5_

- [x] 4. Checkpoint — Asegurarse de que todos los tests de física pasan
  - Asegurarse de que todos los tests pasan, preguntar al usuario si surgen dudas.

- [x] 5. Implementar PipeManager
  - [x] 5.1 Implementar funciones en `pipe_manager.py`
    - `spawn_pipe(frame_count, screen_width) -> Pipe | None`: genera un tubo si `frame_count % PIPE_SPAWN_INTERVAL == 0`, con `gap_center_y` aleatorio en `[GAP_MIN_Y, GAP_MAX_Y]` y `x = screen_width`
    - `move_pipes(pipes) -> list[Pipe]`: resta `PIPE_SPEED` a la `x` de cada tubo
    - `remove_offscreen(pipes) -> list[Pipe]`: elimina tubos donde `x + width < 0`
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ]* 5.2 Escribir property test: Property 5 — Los tubos spawneados tienen propiedades válidas
    - **Property 5: Los tubos spawneados tienen propiedades válidas**
    - **Validates: Requirements 3.1, 3.2, 3.3**
    - Usar `@given(integers)` para `frame_count` múltiplos de 90; verificar `GAP_MIN_Y <= pipe.gap_center_y <= GAP_MAX_Y` y `pipe.gap_height == 150.0`

  - [ ]* 5.3 Escribir property test: Property 6 — El movimiento de tubos desplaza exactamente 3 píxeles a la izquierda
    - **Property 6: El movimiento de tubos desplaza exactamente 3 píxeles a la izquierda**
    - **Validates: Requirements 3.4, 3.5**
    - Usar `@given(lists of Pipe)` con posiciones arbitrarias; verificar que cada `x` disminuye en `PIPE_SPEED` y que los tubos fuera de pantalla son eliminados

  - [ ]* 5.4 Escribir tests unitarios para `pipe_manager.py`
    - Verificar que no se genera tubo en frames no múltiplos de 90, que `remove_offscreen` elimina correctamente, y que `move_pipes` no muta la lista original
    - _Requirements: 3.1, 3.4, 3.5_

- [x] 6. Implementar CollisionDetector
  - [x] 6.1 Implementar funciones en `collision.py`
    - Dataclass `ScreenBounds(width, height)`
    - `check_pipe_collision(player, pipes) -> bool`: usa `pygame.Rect.colliderect` contra `top_rect` y `bottom_rect` de cada tubo
    - `check_boundary_collision(player, bounds) -> bool`: detecta si `player.rect` sale por borde superior (`y < 0`) o inferior (`y + height > bounds.height`)
    - `check_any_collision(player, pipes, bounds) -> bool`: combina ambas funciones
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ]* 6.2 Escribir property test: Property 7 — La detección de colisiones es correcta para tubos y bordes
    - **Property 7: La detección de colisiones es correcta para tubos y bordes**
    - **Validates: Requirements 4.1, 4.2, 4.3**
    - Tres sub-propiedades: (a) superposición de rects implica colisión, (b) jugador dentro de pantalla sin tocar tubos implica no colisión, (c) jugador fuera de bordes implica colisión de borde

  - [ ]* 6.3 Escribir tests unitarios para `collision.py`
    - Casos concretos: colisión exacta con tubo superior, colisión con tubo inferior, salida por borde inferior, salida por borde superior, sin colisión en posición válida
    - _Requirements: 4.1, 4.2, 4.3_

- [x] 7. Implementar ScoreTracker
  - [x] 7.1 Implementar `update_score` en `score.py`
    - `update_score(score, player, pipes) -> tuple[int, list[Pipe]]`: incrementa score en 1 por cada tubo cuyo borde derecho (`x + width`) sea menor que `player.x` y que no esté marcado como `passed`; marca esos tubos como `passed=True`
    - _Requirements: 5.1_

  - [ ]* 7.2 Escribir property test: Property 8 — El score se incrementa exactamente en 1 al superar un tubo
    - **Property 8: El score se incrementa exactamente en 1 al superar un tubo**
    - **Validates: Requirements 5.1**
    - Usar `@given` con configuraciones de jugador y tubos donde el jugador acaba de pasar el borde derecho de un tubo no marcado; verificar incremento exacto de 1 y `passed=True`

  - [ ]* 7.3 Escribir tests unitarios para `score.py`
    - Casos: tubo ya marcado como `passed` no incrementa score, múltiples tubos superados en un frame, tubo aún no superado no incrementa score
    - _Requirements: 5.1_

- [x] 8. Checkpoint — Asegurarse de que todos los tests de lógica de juego pasan
  - Asegurarse de que todos los tests pasan, preguntar al usuario si surgen dudas.

- [x] 9. Implementar InputHandler y SoundManager
  - [x] 9.1 Implementar `InputHandler` en `input_handler.py`
    - Dataclass `Actions(jump=False, quit=False, restart=False)`
    - `process_events(events) -> Actions`: mapea `QUIT` → `quit=True`, `KEYDOWN K_SPACE` / `MOUSEBUTTONDOWN button=1` → `jump=True`, `KEYDOWN K_ESCAPE` → `quit=True` (en contexto GAME_OVER), `KEYDOWN K_SPACE` / `MOUSEBUTTONDOWN` en GAME_OVER → `restart=True`
    - _Requirements: 2.2, 6.3, 6.4, 7.2, 7.3_

  - [ ]* 9.2 Escribir tests unitarios para `input_handler.py`
    - Verificar mapeo de eventos: Space → jump, clic izquierdo → jump, QUIT → quit, eventos desconocidos → sin acción
    - _Requirements: 2.2, 7.2_

  - [x] 9.3 Implementar `SoundManager` en `sound_manager.py`
    - `__init__`: inicializa `pygame.mixer` si no está inicializado
    - `load(jump_path, game_over_path)`: carga los sonidos con `pygame.mixer.Sound`; si falla, loggea advertencia y continúa sin audio
    - `play_jump()` y `play_game_over()`: reproducen el sonido correspondiente si fue cargado
    - _Requirements: 1.3, 2.3, 6.1_

  - [ ]* 9.4 Escribir tests unitarios para `sound_manager.py` con mocks
    - Usar `unittest.mock.patch` para verificar que `play_jump` y `play_game_over` llaman al método correcto; verificar degradación elegante cuando el archivo no existe
    - _Requirements: 1.3, 2.3, 6.1_

- [x] 10. Implementar Renderer
  - [x] 10.1 Implementar clase `Renderer` en `renderer.py`
    - `__init__(screen, font)`: almacena referencias
    - `draw_start()`: fondo de color sólido + texto "Flappy Kiro" + instrucción "Press Space or Click to Start"
    - `draw_playing(player, pipes, score)`: dibuja fondo, tubos (rects verdes), sprite del jugador, y HUD con score en la parte superior central (fuente ≥ 32pt, alto contraste)
    - `draw_game_over(score)`: fondo semitransparente + "Game Over" + score final + instrucción de reinicio
    - _Requirements: 1.5, 5.2, 5.3, 5.4, 6.2_

- [x] 11. Implementar clase Game y máquina de estados
  - [x] 11.1 Implementar `GameState` enum y clase `Game` en `game.py`
    - `GameState`: `START`, `PLAYING`, `GAME_OVER`
    - `Game.__init__`: inicializa pygame, crea ventana 400×600 con título "Flappy Kiro", instancia todos los subsistemas, llama a `_reset()`
    - `Game._reset()`: restaura `player` a posición inicial, `pipes = []`, `score = 0`, `frame_count = 0`, `state = START`
    - `Game.run()`: bucle principal a 60 FPS con `clock.tick(FPS)`; delega a `_handle_start`, `_handle_playing` o `_handle_game_over` según estado
    - `Game._handle_start(actions)`: transiciona a `PLAYING` si `actions.jump`
    - `Game._handle_playing(actions)`: aplica física, mueve tubos, detecta colisiones, actualiza score; si colisión → `GAME_OVER` + `sound_manager.play_game_over()`; si `actions.jump` → `sound_manager.play_jump()`
    - `Game._handle_game_over(actions)`: si `actions.restart` → `_reset()`; si `actions.quit` → salir
    - _Requirements: 1.1, 1.5, 2.1, 2.2, 2.3, 3.1, 3.4, 3.5, 4.1, 4.2, 4.3, 5.1, 5.2, 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.3_

  - [ ]* 11.2 Escribir property test: Property 9 — El reinicio restaura el estado inicial completo
    - **Property 9: El reinicio restaura el estado inicial completo**
    - **Validates: Requirements 6.3**
    - Usar `@given` con estados arbitrarios de GAME_OVER (score, posición, tubos); verificar que tras `_reset()` el estado es idéntico al inicial

  - [ ]* 11.3 Escribir tests unitarios para transiciones de estado en `game.py`
    - Verificar: START → PLAYING al recibir jump, PLAYING → GAME_OVER al detectar colisión, GAME_OVER → START al recibir restart
    - _Requirements: 6.3, 6.4_

- [x] 12. Implementar entry point y carga de assets
  - [x] 12.1 Implementar `main.py`
    - Función `load_assets(game)`: carga `assets/ghosty.png` como imagen del player y llama a `sound_manager.load()`; lanza `FileNotFoundError` si algún archivo no existe
    - `main()`: llama a `load_assets`, captura `FileNotFoundError` → imprime mensaje descriptivo y llama `sys.exit(1)`, captura errores de inicialización de pygame → salir limpiamente; luego llama a `game.run()`
    - _Requirements: 1.2, 1.3, 1.4, 7.3_

- [x] 13. Checkpoint final — Asegurarse de que todos los tests pasan
  - Asegurarse de que todos los tests pasan, preguntar al usuario si surgen dudas.

## Notes

- Las tareas marcadas con `*` son opcionales y pueden omitirse para un MVP más rápido
- Cada tarea referencia requisitos específicos para trazabilidad
- Los property tests usan Hypothesis con `@settings(max_examples=100)` y el tag `# Feature: flappy-kiro, Property N: descripción`
- Los tests unitarios y los property tests son complementarios: los unitarios cubren casos concretos y los property tests validan invariantes universales
- La física usa funciones puras sobre dataclasses, lo que facilita el testing sin necesidad de mocks de pygame
