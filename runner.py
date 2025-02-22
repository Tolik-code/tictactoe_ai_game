import pygame
import sys
import time
import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False
ai_vs_ai = False  # Новий флаг для AI проти AI


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Let user choose a player.
    if user is None and not ai_vs_ai:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect(center=((width / 2), 50))
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2 - 60), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playX.get_rect(center=playXButton.center))

        playOButton = pygame.Rect(5 * (width / 8), (height / 2 - 60), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playO.get_rect(center=playOButton.center))

        aiVsAiButton = pygame.Rect((width / 4), (height / 2 + 20), width / 2, 50)
        aiVsAi = mediumFont.render("AI vs AI", True, black)
        pygame.draw.rect(screen, white, aiVsAiButton)
        screen.blit(aiVsAi, aiVsAi.get_rect(center=aiVsAiButton.center))

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O
            elif aiVsAiButton.collidepoint(mouse):
                time.sleep(0.2)
                ai_vs_ai = True

    else:

        # Draw game board
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

        # Show title
        if game_over:
            winner = ttt.winner(board)
            title = f"Game Over: {winner} wins." if winner else "Game Over: Tie."
        else:
            if ai_vs_ai:
                title = "AI vs AI: Thinking..."
            elif user == player:
                title = f"Play as {user}"
            else:
                title = "Computer thinking..."

        title = largeFont.render(title, True, white)
        screen.blit(title, title.get_rect(center=((width / 2), 30)))

        # AI vs AI logic
        if ai_vs_ai and not game_over:
            time.sleep(0.5)
            move = ttt.minimax(board)
            if move:
                board = ttt.result(board, move)

        # Regular AI move
        elif user != player and not game_over:
            if ai_turn:
                time.sleep(0.1)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # User move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                        board = ttt.result(board, (i, j))

        # Play Again button
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, again.get_rect(center=againButton.center))

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1 and againButton.collidepoint(pygame.mouse.get_pos()):
                time.sleep(0.2)
                user = None
                board = ttt.initial_state()
                ai_turn = False
                ai_vs_ai = False

    pygame.display.flip()
