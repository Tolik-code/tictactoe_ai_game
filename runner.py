import pygame
import sys
import time
import random
import tictactoe as ttt
import os

pygame.init()
size = width, height = 600, 400

# Colors
black = (20, 20, 20)
white = (240, 240, 240)
blue = (100, 149, 237)
green = (50, 205, 50)
red = (255, 69, 0)
yellow = (255, 215, 0)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Fonts
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

mediumFont = pygame.font.Font(resource_path("OpenSans-Regular.ttf"), 28)
largeFont = pygame.font.Font(resource_path("OpenSans-Regular.ttf"), 40)
moveFont = pygame.font.Font(resource_path("OpenSans-Regular.ttf"), 60)

# Game state
user = None
board = ttt.initial_state()
ai_turn = False
ai_vs_ai = False
human_vs_human = False
winning_animation = False
confetti = []
show_bug_button = True
current_player = ttt.X

# Bug button
bug_button = pygame.Rect(width / 4, 330, 200, 50)

# Create confetti
for _ in range(100):
    confetti.append([
        random.randint(0, width),
        random.randint(0, height),
        random.choice([red, blue, yellow, green]),
        random.randint(2, 5)
    ])

def draw_confetti():
    for i, piece in enumerate(confetti):
        pygame.draw.circle(screen, piece[2], (piece[0], piece[1]), piece[3])
        piece[1] += 5
        if piece[1] > height:
            confetti[i][1] = random.randint(-20, -5)
            confetti[i][0] = random.randint(0, width)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Main menu
    if user is None and not ai_vs_ai and not human_vs_human:
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        screen.blit(title, title.get_rect(center=(width / 2, 50)))

        buttons = [
            (pygame.Rect((width / 8), 120, width / 4, 50), "Play as X"),
            (pygame.Rect(5 * (width / 8), 120, width / 4, 50), "Play as O"),
            (pygame.Rect((width / 4), 190, width / 2, 50), "AI vs AI"),
            (pygame.Rect((width / 4), 260, width / 2, 50), "Human vs Human")
        ]

        for button, text in buttons:
            pygame.draw.rect(screen, blue, button, border_radius=10)
            label = mediumFont.render(text, True, black)
            screen.blit(label, label.get_rect(center=button.center))

        # Show bug button only on main menu
        if show_bug_button:
            mouse = pygame.mouse.get_pos()
            if bug_button.collidepoint(mouse):
                new_x = random.randint(0, width - bug_button.width)
                new_y = random.randint(330, height - bug_button.height)
                bug_button.x = min(max(new_x, 0), width - bug_button.width)
                bug_button.y = min(max(new_y, 330), height - bug_button.height)

            pygame.draw.rect(screen, red, bug_button, border_radius=10)
            bug_text = mediumFont.render("Report Bugs", True, white)
            screen.blit(bug_text, bug_text.get_rect(center=bug_button.center))

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttons[0][0].collidepoint(mouse):
                user = ttt.X
                show_bug_button = False
            elif buttons[1][0].collidepoint(mouse):
                user = ttt.O
                show_bug_button = False
            elif buttons[2][0].collidepoint(mouse):
                ai_vs_ai = True
                show_bug_button = False
            elif buttons[3][0].collidepoint(mouse):
                human_vs_human = True
                current_player = ttt.X
                show_bug_button = False
            time.sleep(0.2)

    else:
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
        tiles = []

        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)
                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    screen.blit(move, move.get_rect(center=rect.center))
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        if game_over:
            winner = ttt.winner(board)
            title = f"Game Over: {winner} wins!" if winner else "Game Over: Tie."
            if winner and not winning_animation:
                winning_animation = True
            draw_confetti()
        else:
            if human_vs_human:
                title = f"Human vs Human: {current_player}"
            else:
                title = "AI vs AI: Thinking..." if ai_vs_ai else f"Play as {user}" if user == player else "Computer thinking..."

        screen.blit(largeFont.render(title, True, white), (width / 2 - 150, 30))

        if ai_vs_ai and not game_over:
            time.sleep(0.5)
            move = ttt.minimax(board)
            if move:
                board = ttt.result(board, move)

        elif user != player and not game_over and not ai_vs_ai and not human_vs_human:
            if ai_turn:
                time.sleep(0.1)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        if (human_vs_human or user) and not game_over:
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                            board = ttt.result(board, (i, j))
                            if human_vs_human:
                                current_player = ttt.O if current_player == ttt.X else ttt.X
                            break

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            pygame.draw.rect(screen, green, againButton, border_radius=10)
            again = mediumFont.render("Play Again", True, black)
            screen.blit(again, again.get_rect(center=againButton.center))

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1 and againButton.collidepoint(pygame.mouse.get_pos()):
                user, ai_vs_ai, human_vs_human, winning_animation = None, False, False, False
                board = ttt.initial_state()
                current_player = ttt.X
                show_bug_button = True
                time.sleep(0.2)

    pygame.display.flip()
    clock.tick(30)
