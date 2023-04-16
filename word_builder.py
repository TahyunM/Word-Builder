import pygame
import random
import string
import time
from enchant.checker import SpellChecker
import pygame.mixer
import os
import pickle

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Builder Game")

# Initialize Pygame mixer
pygame.mixer.init()

# Load and play music
music_path = 'C:/Users/Tahyun/Desktop/COSC 231/carefree.mp3'
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)  
pygame.mixer.music.set_volume(0.5)


# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Set up fonts
FONT = pygame.font.Font(None, 36)

HIGH_SCORES_FILE ='high_scores.pk1'

import os
import pickle

# Other imports and initializations

HIGH_SCORES_FILE = 'high_scores.pkl'

def save_high_score(new_score):
    high_scores = load_high_scores()
    high_scores.append(new_score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:10]  # Keep only the top 10 scores
    
    with open(HIGH_SCORES_FILE, 'wb') as file:
        pickle.dump(high_scores, file)

def load_high_scores():
    if os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, 'rb') as file:
            high_scores = pickle.load(file)
    else:
        high_scores = []
    
    return high_scores

def display_high_scores():
    running = True

    high_scores = load_high_scores()

    while running:
        WINDOW.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Draw the high scores
        for i, score in enumerate(high_scores):
            score_line = f"{i + 1}. {score}"
            score_surface = FONT.render(score_line, True, BLACK)
            score_rect = score_surface.get_rect(topleft=(100, 100 + i * 50))
            WINDOW.blit(score_surface, score_rect)

        pygame.display.flip()



def main_menu():
    running = True
    exit_game = False
    menu_options = ['New Game', 'High Scores', 'Credits', 'Options', 'Exit']
    selected_option = 0

    while running:
        WINDOW.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        exit_game = game_loop()
                        if exit_game:
                            running = False
                    elif selected_option == 1:
                        display_high_scores()
                    elif selected_option == 2:
                        display_credits()
                    elif selected_option == 3:
                        display_options()
                    elif selected_option ==4:
                        running = False

        # Draw menu elements on the screen
        for i, option in enumerate(menu_options):
            color = GREEN if i == selected_option else BLACK
            option_surface = FONT.render(option, True, color)
            option_rect = option_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + i * 50))
            WINDOW.blit(option_surface, option_rect)

        pygame.display.flip()

    pygame.quit()
    return exit_game


def display_credits():
    show_credits = True

    credit_text = ("The following music was used for this media project:\n"
                   "Music: Carefree by Kevin MacLeod\n"
                   "Free download: https://filmmusic.io/song/3476-carefree\n"
                   "License (CC BY 4.0): https://filmmusic.io/standard-license")

    while show_credits:
        WINDOW.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_credits = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_credits = False

        # Draw credits on the screen
        credit_lines = credit_text.split("\n")
        for i, line in enumerate(credit_lines):
            line_surface = FONT.render(line, True, BLACK)
            line_rect = line_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + i * 50))
            WINDOW.blit(line_surface, line_rect)

        pygame.display.flip()


def game_loop():
    # Generate random letters
    NUM_LETTERS = 7
    letters = [random.choice(string.ascii_uppercase) for _ in range(NUM_LETTERS)]

    # Timer settings
    GAME_DURATION = 60
    start_time = time.time()

    # Game loop
    game_running = True
    user_input = ""
    score = 0
    exit_game = False
    while game_running:
        WINDOW.fill(WHITE)
        current_time = time.time()
        elapsed_time = current_time - start_time
        remaining_time = int(GAME_DURATION - elapsed_time)

        if remaining_time <= 0:
            game_running = False
            save_high_score(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                exit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    game_running = False
                elif event.key == pygame.K_RETURN:
                    checker = SpellChecker("en_US")
                    if not checker.check(user_input):
                        user_input = ""
                    else:
                        score += len(user_input) * 10
                        user_input = ""
                else:
                    user_input += event.unicode.upper()

        # Draw random letters, user input, score, and timer
        for i, letter in enumerate(letters):
            letter_surface = FONT.render(letter, True, BLACK)
            letter_rect = letter_surface.get_rect(center=(100 + i * 80, 200))
            WINDOW.blit(letter_surface, letter_rect)
        # Draw user input
        user_input_surface = FONT.render(user_input, True, BLACK)
        user_input_rect = user_input_surface.get_rect(topleft=(100, 300))
        WINDOW.blit(user_input_surface, user_input_rect)

        # Draw score
        score_surface = FONT.render(f"Score: {score}", True, BLACK)
        score_rect = score_surface.get_rect(topleft=(100, 50))
        WINDOW.blit(score_surface, score_rect)

        # Draw timer
        timer_surface = FONT.render(f"Time: {remaining_time}", True, BLACK)
        timer_rect = timer_surface.get_rect(topright=(WIDTH - 100, 50))
        WINDOW.blit(timer_surface, timer_rect)

        pygame.display.flip()

    return exit_game

def display_high_scores():
    running = True

    high_scores = load_high_scores()

    while running:
        WINDOW.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Draw the high scores
        for i, score in enumerate(high_scores):
            score_line = f"{i + 1}. {score}"
            score_surface = FONT.render(score_line, True, BLACK)
            score_rect = score_surface.get_rect(topleft=(100, 100 + i * 50))
            WINDOW.blit(score_surface, score_rect)

        pygame.display.flip()

def display_options():
    running = True
    volume = pygame.mixer.music.get_volume()

    while running:
        WINDOW.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    volume = max(volume - 0.1, 0)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_RIGHT:
                    volume = min(volume + 0.1, 1)
                    pygame.mixer.music.set_volume(volume)

        # Draw volume text on the screen
        volume_text = f"Music volume: {int(volume * 100)}%"
        volume_surface = FONT.render(volume_text, True, BLACK)
        volume_rect = volume_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WINDOW.blit(volume_surface, volume_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main_menu()

