import numpy as np
import pygame
import sys
import math

SQUARESIZE = 120
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RADIUS = int(SQUARESIZE/2 - 5)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

#Matrix board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

#Pieces
def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

#Stacking pieces in next row
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    """
    Prints the game board with rows shown from bottom to top.
    
    Parameters:
        board (array-like): 2D array representing the board grid (rows x columns), where empty cells and player pieces are stored as numeric values.
    """
    print(np.flip(board, 0))
    
def winning_move(board, piece):
    # Check all possible winning locations
    # Directions: horizontal, vertical, positive diagonal, negative diagonal
    """
    Determine whether the specified piece has four consecutive discs in a row anywhere on the board.
    
    Parameters:
        board (ndarray): 2D array representing the game board; cells equal to `piece` indicate that piece's discs.
        piece (int): Numeric identifier of the piece to check (for example, 1 or 2).
    
    Returns:
        bool: `true` if a horizontal, vertical, or diagonal sequence of four matching `piece` exists, `false` otherwise.
    """
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r_start in range(ROW_COUNT):
        for c_start in range(COLUMN_COUNT):
            for dr, dc in directions:
                if 0 <= r_start + 3*dr < ROW_COUNT and 0 <= c_start + 3*dc < COLUMN_COUNT:
                    if all(board[r_start + i*dr][c_start + i*dc] == piece for i in range(4)):
                        return True
    return False
def draw_board(board):
    #Making a grid
    """
    Render the current game board to the Pygame display surface.
    
    Draws the Connect Four grid and all placed pieces from the provided board state onto the global Pygame screen. Empty cells are shown as black circles inside blue squares; cells with value 1 are drawn as red discs and cells with value 2 as yellow discs. The board's row 0 is treated as the top row of the logical board (display coordinates are flipped vertically so the bottom row appears at the bottom of the window).
    
    Parameters:
        board (2D array-like): Grid representing the board state where 0 = empty, 1 = player 1 piece, 2 = player 2 piece.
    """
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

pygame.init()

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)

myfont = pygame.font.SysFont("monospace", 50)
myfont_result = pygame.font.SysFont("century751", 50)
smallfont = pygame.font.SysFont("monospace", 10,)

player_1_name = ""
player_2_name = ""
current_input_name = ""
input_state = "player1"

#UI
board = create_board()
game_over = False
draw_game = False
turn = 0
player_1_name = ""
player_2_name = ""
current_input_name = ""
input_state = "player1" 

RESTART_BUTTON_WIDTH = 250
RESTART_BUTTON_HEIGHT = 50
restart_button = pygame.Rect((width - RESTART_BUTTON_WIDTH) / 2, height - RESTART_BUTTON_HEIGHT - 50, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)

def reset_game():
    """
    Reset the game state to initial values for starting a new match.
    
    Recreates the empty board, clears game flags and player names, resets the turn and input state, and prints the new board to the console. The following module-level variables are set: board, game_over, draw_game, turn, input_state, player_1_name, player_2_name, current_input_name.
    """
    global board, game_over, draw_game, turn, input_state, player_1_name, player_2_name, current_input_name
    board = create_board()
    game_over = False
    draw_game = False
    turn = 0
    input_state = "player1"
    player_1_name = ""
    player_2_name = ""
    current_input_name = ""
    print_board(board)

reset_game()

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Mouse usage
        if (game_over or draw_game) and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                reset_game()
        
        # Handle keyboard input for name entry
        if input_state != "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_state == "player1":
                        player_1_name = current_input_name
                        current_input_name = ""
                        input_state = "player2"
                    elif input_state == "player2":
                        player_2_name = current_input_name
                        input_state = "game"
                elif event.key == pygame.K_BACKSPACE:
                    current_input_name = current_input_name[:-1]
                else:
                    current_input_name += event.unicode
        
        if input_state == "game" and not game_over and not draw_game:
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    piece = turn + 1 # Player 1 is piece 1, Player 2 is piece 2
                    drop_piece(board, row, col, piece)

                    if winning_move(board, piece):
                        game_over = True
                    
                    # Correctly alternate turns between 0 and 1
                    turn = (turn + 1) % 2
                
                if not game_over:
                    board_full = all(board[ROW_COUNT - 1][c] != 0 for c in range(COLUMN_COUNT))
                    if board_full:
                        draw_game = True

    if input_state != "game":
        screen.fill(BLACK)
        prompt_text = myfont.render(
            "Player 1, enter your name:" if input_state == "player1" else "Player 2, enter your name:", 
            True, WHITE
        )
        name_text = myfont.render(current_input_name, True, RED if input_state == "player1" else YELLOW)
        screen.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, height // 2 - 50))
        screen.blit(name_text, (width // 2 - name_text.get_width() // 2, height // 2))
    
    elif not game_over and not draw_game:
        # Draw the main game board
        draw_board(board)
        
        # Draw the hovering piece
        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
        posx = pygame.mouse.get_pos()[0]
        if turn == 0:
            pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
        else:
            pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
    
    else:
        draw_board(board)
        if game_over:
            label = myfont_result.render(f"{player_1_name if turn == 1 else player_2_name} WINS!", 1, RED if turn == 1 else YELLOW)
        else:
            label = myfont_result.render("IT'S A DRAW!", 1, WHITE)
        
        screen.blit(label, (40, 10))
        pygame.draw.rect(screen, GREEN, restart_button)
        button_text = myfont_result.render("RESTART", True, WHITE)
        text_rect = button_text.get_rect(center=restart_button.center)
        screen.blit(button_text, text_rect)

    pygame.display.update()
    