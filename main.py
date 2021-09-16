# Icons made by Freepik from www.flaticon.com.

import config
import pygame
from snake import SnakeGame, Direction, Tiles

# PYGAME INIT
pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Snake's Prey")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
fps_clock = pygame.time.Clock()

# GAME INIT
game = SnakeGame(config.HOW_MANY_BLOCKS_HEIGHT, config.HOW_MANY_BLOCKS_WIDTH)

# visual board
rects = []
point = config.GAP_SIZE
for i in range(1, config.HOW_MANY_BLOCKS_HEIGHT + 1):
    row = []
    top = config.GAP_SIZE * i + config.BLOCK_SIZE * (i - 1)

    for j in range(1, config.HOW_MANY_BLOCKS_WIDTH + 1):
        left = config.GAP_SIZE * j + config.BLOCK_SIZE * (j - 1)

        rect = pygame.Rect(left, top, config.BLOCK_SIZE, config.BLOCK_SIZE)
        row.append(rect)

    rects.append(row)

colors = {
    Tiles.BORDER: config.BORDER_COLOR,
    Tiles.SNAKE: config.SNAKE_COLOR,
    Tiles.PREY: config.PREY_COLOR,
}

# texts
game_over_font = pygame.font.Font(config.FONT, config.GAME_OVER_SIZE)
game_over_text = game_over_font.render(config.GAME_OVER, True, config.TEXT_COLOR)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = config.GAME_OVER_POSITION

score_font = pygame.font.Font(config.FONT, config.SCORE_SIZE)
your_score_text = score_font.render(config.YOUR_SCORE, True, config.TEXT_COLOR)
your_score_rect = your_score_text.get_rect()
your_score_rect.center = config.YOUR_SCORE_POSITION
high_score_text = score_font.render(config.HIGH_SCORE, True, config.TEXT_COLOR)
high_score_rect = high_score_text.get_rect()
high_score_rect.center = config.HIGH_SCORE_POSITION

continue_font = pygame.font.Font(config.FONT, config.CONTINUE_SIZE)
continue_text = continue_font.render(config.CONTINUE, True, config.TEXT_COLOR)
continue_rect = continue_text.get_rect()
continue_rect.center = config.CONTINUE_POSITION

score_text = score_font.render(config.SCORE, True, config.TEXT_COLOR)
score_rect = score_text.get_rect()
score_rect.left = config.SCORE_POSITION[0]
score_rect.top = config.SCORE_POSITION[1]

# surfaces
opaque = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
opaque.set_alpha(config.OPAQUE_ALPHA)
opaque.fill(config.BACKGROUND_COLOR)

# MAIN LOOP
GAME_OVER = pygame.USEREVENT + 1
game_over_event = pygame.event.Event(GAME_OVER)

counter = 1
speed = config.FPS
if_ended = False
if_moved = False
if_continue = True
running = True
while running:
    for event in pygame.event.get():
        # CLOSING
        if event.type == pygame.QUIT:
            running = False
        elif event.type == GAME_OVER:
            # get high score
            try:
                with open(config.SAVEFILE, "r") as f:
                    high_score = int(f.read())

                    if counter > high_score:
                        high_score = counter
            except (ValueError, FileNotFoundError):
                high_score = counter

            with open(config.SAVEFILE, "w") as f:
                f.truncate(0)
                f.write(str(high_score))

            # blit opaque surface
            screen.blit(opaque, (0, 0))

            high_score_score_text = score_font.render(
                str(high_score), True, config.TEXT_COLOR
            )
            high_score_score_rect = high_score_score_text.get_rect()
            high_score_score_rect.center = config.HIGH_SCORE_SCORE_POSITION
            your_score_score_text = score_font.render(
                str(counter), True, config.TEXT_COLOR
            )
            your_score_score_rect = your_score_score_text.get_rect()
            your_score_score_rect.center = config.YOUR_SCORE_SCORE_POSITION

            # texts
            screen.blit(game_over_text, game_over_rect)
            screen.blit(your_score_text, your_score_rect)
            screen.blit(your_score_score_text, your_score_score_rect)
            screen.blit(high_score_text, high_score_rect)
            screen.blit(high_score_score_text, high_score_score_rect)
            screen.blit(continue_text, continue_rect)

            running_inner = True
            while running_inner:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        running_inner = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game = SnakeGame(
                                config.HOW_MANY_BLOCKS_HEIGHT,
                                config.HOW_MANY_BLOCKS_WIDTH,
                            )
                            counter = 1
                            speed = config.FPS
                            if_ended = False
                            if_moved = False
                            if_continue = True
                            running_inner = False
                        elif event.key == pygame.K_q:
                            running_inner = False
                            running = False
                pygame.display.update()
                fps_clock.tick(config.FPS)

    if if_continue:
        if not if_moved:
            # PLAYER MOVES
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if game.move_prey(Direction.UP):
                    pygame.event.post(game_over_event)
                if_moved = True
            elif keys[pygame.K_DOWN]:
                if game.move_prey(Direction.DOWN):
                    pygame.event.post(game_over_event)
                if_moved = True
            elif keys[pygame.K_RIGHT]:
                if game.move_prey(Direction.RIGHT):
                    pygame.event.post(game_over_event)
                if_moved = True
            elif keys[pygame.K_LEFT]:
                if game.move_prey(Direction.LEFT):
                    pygame.event.post(game_over_event)
                if_moved = True

        # reset if_moved so that player can move
        if counter % (config.FPS * config.PLAYER_SPEED) == 0:
            if_moved = False

        # move snake every 1 second, then 1/2 second, then 1/4 second, etc.
        if counter % speed == 0:
            if game.move_snake():
                pygame.event.post(game_over_event)

        # make snake bigger and faster every 5 second
        if counter % (config.FPS * config.ACCELERATION_INTERVAL) == 0:
            game.enlarge_snake()
            speed /= config.ACCELERATION

        # filling with color
        screen.fill(config.BACKGROUND_COLOR)
        for row_idx, row in enumerate(rects):
            for col_idx, rect in enumerate(row):
                # ignore empty tiles
                tile = game.board[row_idx, col_idx]
                if tile not in (Tiles.EMPTY, Tiles.SNAKE):
                    color = colors[tile]
                    rect = rects[row_idx][col_idx]

                    screen.fill(color, rect)
        # fill snake
        color = pygame.Color((0, 0, 0))
        color.hsva = config.SNAKE_COLOR
        for segment in game.snake:
            rect = rects[segment.y][segment.x]
            screen.fill(color, rect)

            new_color = color.hsva[2] + config.HSV_STEP
            if new_color < 100:
                color.hsva = color.hsva[:2] + (new_color,) + color.hsva[3:]

        # update score
        score_score_text = score_font.render(str(counter), True, config.TEXT_COLOR)
        score_score_rect = score_score_text.get_rect()
        score_score_rect.left = config.SCORE_SCORE_POSITION[0]
        score_score_rect.top = config.SCORE_SCORE_POSITION[1]
        screen.blit(score_text, score_rect)
        screen.blit(score_score_text, score_score_rect)

    pygame.display.update()
    fps_clock.tick(config.FPS)
    counter += 1

pygame.quit()
