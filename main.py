import pygame
import sys
import random
import asyncio

pygame.init()

WIDTH, HEIGHT = 720, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
paddle_speed = 7
paddle = pygame.Rect(random.randint(0, WIDTH - PADDLE_WIDTH), HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)

BALL_RADIUS = 10
ball_speed_x, ball_speed_y = 4, -4
ball = pygame.Rect(random.randint(0, WIDTH - BALL_RADIUS * 2), HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)

BRICK_ROWS, BRICK_COLS = 5, 8
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 30

def regenerate_bricks():
    new_bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick = pygame.Rect(
                col * BRICK_WIDTH,
                row * BRICK_HEIGHT + 50,
                BRICK_WIDTH - 2,
                BRICK_HEIGHT - 2
            )
            new_bricks.append(brick)
    return new_bricks

bricks = regenerate_bricks()
score = 0
last_speed_milestone = 0

clock = pygame.time.Clock()
running = True
game_over = False

async def main():
    global game_over
    global bricks
    global ball
    global paddle
    global ball_speed_x
    global ball_speed_y
    global score
    global last_speed_milestone
    global paddle_speed
    
    try:
        font = pygame.font.Font("Press_Start_2P_Font/PressStart2P-Regular.ttf", 24)
    except:
        font = pygame.font.SysFont(None, 24)

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if game_over:
            screen.fill(BLACK)

            game_over_text = font.render("GAME OVER - Press SPACE to Restart", True, WHITE)
            score_text = font.render(f"Final Score: {score}", True, GREEN)

            screen.blit(game_over_text, (WIDTH//2 - 250, HEIGHT//2 - 40))
            screen.blit(score_text, (WIDTH//2 - 100, HEIGHT//2 + 10))

            pygame.display.flip()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                ball.x = random.randint(0, WIDTH - BALL_RADIUS * 2)
                ball.y = HEIGHT // 2
                ball_speed_x, ball_speed_y = 4, -4
                paddle.x = random.randint(0, WIDTH - PADDLE_WIDTH)
                paddle.y = HEIGHT - 40
                score = 0
                paddle_speed = 7
                last_speed_milestone = 0
                bricks = regenerate_bricks()
                game_over = False

            clock.tick(60)
            await asyncio.sleep(0)
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += paddle_speed

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed_x *= -1
        if ball.top <= 0:
            ball_speed_y *= -1
        if ball.bottom >= HEIGHT:
            game_over = True

        if ball.colliderect(paddle):
            ball_speed_y *= -1

        hit_index = ball.collidelist(bricks)
        if hit_index != -1:
            bricks.pop(hit_index)
            ball_speed_y *= -1
            score += 10

        if score >= last_speed_milestone + 20:
            ball_speed_x += 0.1 if ball_speed_x > 0 else -0.1
            ball_speed_y += 0.1 if ball_speed_y > 0 else -0.1
            paddle_speed += 0.1
            last_speed_milestone += 20

        if len(bricks) == 0:
            bricks = regenerate_bricks()

        pygame.draw.rect(screen, BLUE, paddle)
        pygame.draw.ellipse(screen, WHITE, ball)

        for brick in bricks:
            pygame.draw.rect(screen, RED, brick)

        score_text = font.render(f"Score: {score}", True, GREEN)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
