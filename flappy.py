import random
import sys

import pygame

# Inicializa o pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird by Gracy")

# FPS
clock = pygame.time.Clock()
FPS = 60

# Cores
WHITE = (255, 255, 255)

# Carregando imagens
background = pygame.image.load("assets/background.png").convert()
bird = pygame.image.load("assets/bird.png").convert_alpha()
pipe = pygame.image.load("assets/pipe.png").convert_alpha()
base = pygame.image.load("assets/base.png").convert_alpha()

# Escala de imagens
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
bird = pygame.transform.scale(bird, (40, 30))
pipe = pygame.transform.scale(pipe, (70, 400))
base = pygame.transform.scale(base, (SCREEN_WIDTH, 100))

# Posições iniciais
bird_x, bird_y = 60, 300
bird_velocity = 0
gravity = 0.5
jump = -8

pipes = []
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # em milissegundos
last_pipe = pygame.time.get_ticks()

# Fonte
font = pygame.font.SysFont("Arial", 32)
score = 0


def draw_base():
    screen.blit(base, (0, SCREEN_HEIGHT - 100))


def create_pipe():
    height = random.randint(150, 400)
    bottom_pipe = pipe.get_rect(midtop=(SCREEN_WIDTH + 100, height))
    top_pipe = pipe.get_rect(midbottom=(SCREEN_WIDTH + 100, height - PIPE_GAP))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for p in pipes:
        p.centerx -= 4
    return [p for p in pipes if p.right > 0]


def draw_pipes(pipes):
    for p in pipes:
        if p.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe, p)
        else:
            flipped_pipe = pygame.transform.flip(pipe, False, True)
            screen.blit(flipped_pipe, p)


def check_collision(pipes, bird_rect):
    for p in pipes:
        if bird_rect.colliderect(p):
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT - 100:
        return False
    return True


# Loop do jogo
running = True
while running:
    screen.blit(background, (0, 0))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump

    # Movimento do pássaro
    bird_velocity += gravity
    bird_y += bird_velocity
    bird_rect = bird.get_rect(center=(bird_x, bird_y))
    screen.blit(bird, bird_rect)

    # Gerar novos canos
    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > PIPE_FREQUENCY:
        last_pipe = time_now
        pipes.extend(create_pipe())

    # Movimentar e desenhar canos
    pipes = move_pipes(pipes)
    draw_pipes(pipes)

    # Base
    draw_base()

    # Colisão
    if not check_collision(pipes, bird_rect):
        running = False

    # Pontuação
    for p in pipes:
        if p.centerx == bird_x:
            score += 1
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2, 50))

    pygame.display.update()
    clock.tick(FPS)

print(f"Sua pontuação final foi: {score}")
pygame.quit()
