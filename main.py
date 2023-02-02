import pygame
import numpy as np
from minimax import Minimax
from board import Board

bg_color =      (100, 98, 97)
bottom_color =  (47, 47, 47)
empty =         (62, 62, 62)
player =        (89, 189, 107)
ai =            (184, 92, 99) 

radius = 45
board_shape = (6,7)
width, height = 900, 700
pygame.init() 
pygame.display.set_caption('Connect-four')
surface = pygame.display.set_mode((width, height))
surface.fill(bg_color)
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
                if move > 7 or move < 0 or not board_funcs.is_valid_move(move, board):
                    print('not a valid move pick again')
                else:
                    return move

def play():
    running = True
    board = np.zeros(board_shape, dtype=int)
    player_turn = 1
    reward = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        print(player_turn)
        if player_turn == 1:
            print('your turn')
            move = get_player_move(board)
            if move == -1:
                return 
            board, reward = board_funcs.drop_piece(board, move, 1)
        else:
            print('bots turn')
            move = minimax.get_move(board)
            board, reward = board_funcs.drop_piece(board, move, -1)

        player_turn = player_turn * -1

        render(board)
        if not reward == 0:

            running = False

def show_results():
    pass



def main():
    setup()
    winner = play()
    show_results()


if __name__ == '__main__':
    main()