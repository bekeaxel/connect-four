import random
import pygame
import numpy as np
from minimax import Minimax
from board import Board

bg_color =      (100, 98, 97)
bottom_color =  (47, 47, 47)
empty =         (62, 62, 62)
player =        (89, 189, 107)
ai =            (184, 92, 99) 
message_color = (242, 240, 231)

radius = 45
board_shape = (6,7)
width, height = 900, 700
pygame.init() 
pygame.display.set_caption('Connect-four')
surface = pygame.display.set_mode((width, height))
surface.fill(bg_color)
font = pygame.font.SysFont('Verdana', 24)
minimax = Minimax()
board_funcs = Board()
pygame.display.update()

def setup():
    pygame.draw.rect(surface, bottom_color, (0, 600, 900, 100))
    for row in range(board_shape[0]):
        for col in range(board_shape[1]):
            pygame.draw.circle(surface, empty, (150 + col * 100, 50 + row * 100), radius)
    pygame.display.update()

def render(board):
    pygame.draw.rect(surface, bottom_color, (0, 600, 900, 100))
    for row in range(board_shape[0]):
        for col in range(board_shape[1]):
            if board[row, col] == 1:
                pygame.draw.circle(surface, player, (150 + col * 100, 50 + row * 100), radius)
            elif board[row, col] == -1:
                pygame.draw.circle(surface, ai, (150 + col * 100, 50 + row * 100), radius)
            else: 
                pygame.draw.circle(surface, empty, (150 + col * 100, 50 + row * 100), radius)
    pygame.display.update()

def get_player_move(board):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()[0]
                move = pos // 100 - 1
                if not(move > 7 and move < 0 and not board_funcs.is_valid_move(move, board)):
                    return move

def play():
    running = False
    board = np.zeros(board_shape, dtype=int)
    player_turn = random.choice([1,-1])
    reward = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        if player_turn == 1:
            message = font.render('''Computer says: It's your turn...''', 1 , message_color)
            surface.blit(message, (75, 630))
            pygame.display.update()
            move = get_player_move(board)
            if move == -1:
                break
            board, reward = board_funcs.drop_piece(board, move, 1)
        else:
            message = font.render('Computer says: Hmmm what should I play now...?', 1, message_color)
            surface.blit(message, (75, 630))
            pygame.display.update()
            move = minimax.get_move(board)
            board, reward = board_funcs.drop_piece(board, move, -1)
        player_turn = player_turn * -1
        render(board)
        if not reward == 0:
            return player_turn * -1

def show_results(winner):
    pygame.draw.rect(surface, bottom_color, (0, 600, 900, 100))
    if winner == 1:
        message = font.render("Computer says: Wow you won, nice", 1, message_color)
    else:
        message = font.render("Computer says: Better luck next time kid", 1, message_color)
    surface.blit(message, (75, 630))
    pygame.display.update()
    main()

def main():
    running = True
    message = font.render("Press space to play", 1, message_color)
    surface.blit(message, (90, 660))
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == 771:
                setup()
                result = play()
                running = False
                if result == 1 or result == -1:
                    running = True
                    show_results(result)

if __name__ == '__main__':
    setup()
    main()