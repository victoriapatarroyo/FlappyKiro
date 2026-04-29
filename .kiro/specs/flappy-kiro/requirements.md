# Requirements Document

## Introduction

Flappy Kiro es un juego de un solo jugador estilo Flappy Bird implementado en Python. El jugador controla a Ghosty (la mascota de Kiro) a través de una serie de tubos generados proceduralmente. El objetivo es sobrevivir el mayor tiempo posible evitando colisiones con los tubos y los bordes de la pantalla, acumulando puntos por cada tubo superado. El juego incluye efectos de sonido para el salto y el fin de partida.

## Glossary

- **Game**: El sistema principal que gestiona el bucle de juego, el estado y la coordinación de todos los componentes.
- **Player**: El personaje controlado por el usuario, representado por el sprite `assets/ghosty.png`.
- **Pipe**: Obstáculo vertical compuesto por un tubo superior y uno inferior con un hueco entre ellos por el que el Player debe pasar.
- **Score**: Contador numérico que registra cuántos pares de Pipes ha superado el Player en la partida actual.
- **Collision**: Contacto entre el hitbox del Player y el hitbox de un Pipe o con los límites superior/inferior de la pantalla.
- **Game_Over**: Estado del juego que se activa cuando ocurre una Collision.
- **HUD**: Interfaz en pantalla que muestra el Score actual durante la partida.
- **Sound_Manager**: Componente responsable de reproducir los efectos de sonido del juego.
- **Gravity**: Fuerza constante que acelera al Player hacia abajo en cada frame.
- **Jump**: Acción que aplica una velocidad vertical hacia arriba al Player cuando el usuario presiona la tecla de control.

---

## Requirements

### Requirement 1: Inicialización del juego

**User Story:** As a player, I want the game to start with a clear initial screen, so that I know when the game is ready to play.

#### Acceptance Criteria

1. THE Game SHALL initialize a window with a resolution de 400x600 píxeles y el título "Flappy Kiro".
2. THE Game SHALL load the sprite `assets/ghosty.png` as the Player image before the game loop starts.
3. THE Game SHALL load `assets/jump.wav` and `assets/game_over.wav` into the Sound_Manager before the game loop starts.
4. IF any required asset file is not found, THEN THE Game SHALL display an error message and exit gracefully.
5. THE Game SHALL display a start screen with instructions to press a key to begin before the first game loop iteration.

---

### Requirement 2: Física del jugador

**User Story:** As a player, I want Ghosty to fall due to gravity and jump when I press a key, so that I can control the character's vertical position.

#### Acceptance Criteria

1. WHILE the game loop is active, THE Player SHALL accelerate downward at a constant Gravity rate of 0.5 pixels per frame squared.
2. WHEN the player presses the Space key or the left mouse button, THE Player SHALL receive an upward velocity of -8 pixels per frame.
3. WHEN the player presses the Space key or the left mouse button, THE Sound_Manager SHALL play `assets/jump.wav`.
4. THE Player SHALL be horizontally fixed at x = 80 pixels throughout the entire game session.
5. WHILE the game loop is active, THE Player SHALL clamp its vertical velocity to a maximum downward speed of 10 pixels per frame.

---

### Requirement 3: Generación y movimiento de tubos

**User Story:** As a player, I want pipes to appear continuously and move toward me, so that the game presents an ongoing challenge.

#### Acceptance Criteria

1. THE Game SHALL spawn a new Pipe pair every 90 frames.
2. WHEN a Pipe pair is spawned, THE Game SHALL place the gap center at a random vertical position between 150 and 450 pixels from the top of the screen.
3. THE Game SHALL set the gap height between the upper and lower Pipe to 150 pixels.
4. WHILE the game loop is active, THE Game SHALL move all active Pipes to the left at a speed of 3 pixels per frame.
5. WHEN a Pipe pair moves completely off the left edge of the screen (x + pipe_width < 0), THE Game SHALL remove it from the active Pipe list.

---

### Requirement 4: Detección de colisiones

**User Story:** As a player, I want the game to detect when Ghosty hits a pipe or the screen boundary, so that the game ends fairly when I make a mistake.

#### Acceptance Criteria

1. WHEN the Player's hitbox intersects with the hitbox of any Pipe, THE Game SHALL transition to the Game_Over state.
2. WHEN the Player's vertical position causes its hitbox to go below the bottom edge of the screen, THE Game SHALL transition to the Game_Over state.
3. WHEN the Player's vertical position causes its hitbox to go above the top edge of the screen (y < 0), THE Game SHALL transition to the Game_Over state.
4. THE Game SHALL use rectangular hitboxes for both the Player and all Pipes for collision detection.

---

### Requirement 5: Sistema de puntuación

**User Story:** As a player, I want to see my score increase as I pass through pipes, so that I have a clear measure of my progress.

#### Acceptance Criteria

1. WHEN the Player's horizontal position passes the right edge of a Pipe pair without a Collision, THE Game SHALL increment the Score by 1.
2. WHILE the game loop is active, THE HUD SHALL display the current Score as an integer in the top-center area of the screen.
3. THE HUD SHALL render the Score using a font size of at least 32 points with high contrast against the background.
4. WHEN the Game_Over state is active, THE HUD SHALL display the final Score on the Game_Over screen.

---

### Requirement 6: Estado de Game Over

**User Story:** As a player, I want a clear game over screen with my final score, so that I know the game has ended and can choose to play again.

#### Acceptance Criteria

1. WHEN the Game transitions to the Game_Over state, THE Sound_Manager SHALL play `assets/game_over.wav`.
2. WHEN the Game transitions to the Game_Over state, THE Game SHALL display a "Game Over" message and the final Score on screen.
3. WHEN the Game_Over state is active and the player presses the Space key or the left mouse button, THE Game SHALL reset all game state and return to the start screen.
4. WHEN the Game_Over state is active and the player presses the Escape key, THE Game SHALL close the window and exit.

---

### Requirement 7: Bucle de juego y rendimiento

**User Story:** As a player, I want the game to run smoothly at a consistent frame rate, so that the experience is fair and enjoyable.

#### Acceptance Criteria

1. THE Game SHALL run the main game loop at a target frame rate of 60 frames per second.
2. WHILE the game loop is active, THE Game SHALL process all pending input events each frame before updating game state.
3. WHEN the player closes the window, THE Game SHALL exit the process cleanly.
