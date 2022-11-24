"""A game of pong"""

import pygame
pygame.init()


WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 10


class Paddle:
    """A paddle"""
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        """Draw self to screen"""
        pygame.draw.rect(
            win,
            self.COLOR,
            (self.x, self.y, self.width, self.height)
        )

    def move(self, up=True):
        """Move self up or down"""
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        """Reset position"""
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    """A ball"""
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        """Draw self to screen"""
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        """Move self"""
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        """Reset position"""
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win, paddles, ball, left_score, right_score):
    """Draw everything to screen"""
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", True, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", True, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) -
                                right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    """Handle collision between ball and paddles"""
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    def change_direction(paddle):
        """Change direction of ball"""
        ball.x_vel *= -1
        middle_y = paddle.y + paddle.height / 2
        difference_in_y = middle_y - ball.y
        reduction_factor = (paddle.height / 2) / ball.MAX_VEL
        y_vel = difference_in_y / reduction_factor
        ball.y_vel = -1 * y_vel

    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                change_direction(left_paddle)

    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                change_direction(right_paddle)


def handle_paddle_movement(keys, left_paddle, right_paddle):
    """Handle paddle movement"""
    for up, down, paddle in [
            (pygame.K_w, pygame.K_s, left_paddle),
            (pygame.K_UP, pygame.K_DOWN, right_paddle)
    ]:
        if keys[up] and paddle.y - paddle.VEL >= 0:
            paddle.move(up=True)
        if keys[down] and paddle.y + paddle.VEL + \
                paddle.height <= HEIGHT:
            paddle.move(up=False)


def main():
    """The main loop"""
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
            if left_score >= WINNING_SCORE:
                win_text = "Left Player Won!"
            else:
                win_text = "Right Player Won!"
            text = SCORE_FONT.render(win_text, True, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width() //
                            2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()
