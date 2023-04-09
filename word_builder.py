import pygame
import random
import string
import time
from enchant.checker import SpellChecker

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Builder Game")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Set up fonts
FONT = pygame.font.Font(None, 36)

# Generate random letters
NUM_LETTERS = 10
letters = [random.choice(string.ascii_uppercase) for _ in range(NUM_LETTERS)]

# Timer settings
GAME_DURATION = 60
start_time = time.time()

# Game loop
# Game loop
running = True
user_input = ""
score = 0
while running:
    WINDOW.fill(WHITE)
    current_time = time.time()
    elapsed_time = current_time - start_time
    remaining_time = int(GAME_DURATION - elapsed_time)

    if remaining_time <= 0:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_RETURN:
                checker = SpellChecker("en_US")
                if not checker.check(user_input):
                    user_input = ""
                else:
                    score += len(user_input) * 10
                    user_input = ""
            else:
                user_input += event.unicode.upper()

    # Draw random letters, user input, score, and timer as before

# Display final score and clean up as before


    # Draw random letters
    for i, letter in enumerate(letters):
        letter_surface = FONT.render(letter, True, BLACK)
        letter_rect = letter_surface.get_rect(center=(WIDTH // 2 - (NUM_LETTERS // 2) * 50 + i * 50, HEIGHT // 2))
        WINDOW.blit(letter_surface, letter_rect)

    # Draw user input
    input_surface = FONT.render(user_input, True, BLACK)
    input_rect = input_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    WINDOW.blit(input_surface, input_rect)

    # Draw score
    score_surface = FONT.render(f"Score: {score}", True, BLACK)
    score_rect = score_surface.get_rect(topleft=(20, 20))
    WINDOW.blit(score_surface, score_rect)

    # Draw timer
    timer_surface = FONT.render(f"Time left: {remaining_time}", True, GREEN)
    timer_rect = timer_surface.get_rect(topright=(WIDTH - 20, 20))
    WINDOW.blit(timer_surface, timer_rect)

    # Update display
    pygame.display.flip()

# Display final score
print(f"Your final score: {score}")

# Clean up
pygame.quit()
