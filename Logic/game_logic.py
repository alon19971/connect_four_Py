import pygame
import sys
from Logic.board import Board

class GameLogic:
    """
    Class that handles the game logic for Connect Four.
    """

    def __init__(self, screen, drop_sound, win_sound):
        """
        Initializes the game logic with the screen, drop sound, and win sound.

        Parameters:
        - screen: The pygame screen surface where the game will be displayed.
        - drop_sound: The sound played when a piece is dropped.
        - win_sound: The sound played when a player wins.
        """
        self.screen = screen
        self.running = True
        self.board = Board()
        self.turn = 0
        self.drop_sound = drop_sound
        self.win_sound = win_sound

    def run_game(self):
        """
        Runs the main game loop, handling events and updating the game state.

        Returns:
        - The player number who wins (1 or 2), or 0 in case of a draw.
        """
        self.board.draw(self.screen)
        pygame.display.update()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = posx // 100

                    if self.board.is_valid_location(col):
                        row = self.board.get_next_open_row(col)
                        if row is not None:
                            self.board.animate_drop(self.screen, col, self.turn + 1, self.drop_sound)

                            if self.board.winning_move(self.turn + 1):
                                print(f"Player {self.turn + 1} wins!")
                                self.running = False
                                self.animate_winning_line(self.turn + 1)
                                if self.win_sound:
                                    self.win_sound.play()
                                return self.turn + 1

                            if self.board.is_draw():
                                print("Draw!")
                                self.running = False
                                return 0

                            self.turn += 1
                            self.turn %= 2

                    self.board.draw(self.screen)
                    pygame.display.update()

        return None

    def animate_winning_line(self, piece):
        """
        Animates the winning line when a player wins.

        Parameters:
        - piece: The player's piece (1 or 2) that formed the winning line.
        """
        for c in range(self.board.COLS - 3):
            for r in range(self.board.ROWS):
                if self.board.board[r][c] == piece and self.board.board[r][c + 1] == piece and self.board.board[r][c + 2] == piece and self.board.board[r][c + 3] == piece:
                    self.blink_winning_pieces([(r, c), (r, c + 1), (r, c + 2), (r, c + 3)])
                    return

        for c in range(self.board.COLS):
            for r in range(self.board.ROWS - 3):
                if self.board.board[r][c] == piece and self.board.board[r + 1][c] == piece and self.board.board[r + 2][c] == piece and self.board.board[r + 3][c] == piece:
                    self.blink_winning_pieces([(r, c), (r + 1, c), (r + 2, c), (r + 3, c)])
                    return

        for c in range(self.board.COLS - 3):
            for r in range(self.board.ROWS - 3):
                if self.board.board[r][c] == piece and self.board.board[r + 1][c + 1] == piece and self.board.board[r + 2][c + 2] == piece and self.board.board[r + 3][c + 3] == piece:
                    self.blink_winning_pieces([(r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3)])
                    return

        for c in range(self.board.COLS - 3):
            for r in range(3, self.board.ROWS):
                if self.board.board[r][c] == piece and self.board.board[r - 1][c + 1] == piece and self.board.board[r - 2][c + 2] == piece and self.board.board[r - 3][c + 3] == piece:
                    self.blink_winning_pieces([(r, c), (r - 1, c + 1), (r - 2, c + 2), (r - 3, c + 3)])
                    return

    def blink_winning_pieces(self, pieces):
        """
        Blinks the winning pieces to highlight the winning line.

        Parameters:
        - pieces: A list of tuples representing the coordinates of the winning pieces.
        """
        for _ in range(5):
            self.board.draw(self.screen)
            for (r, c) in pieces:
                pygame.draw.circle(self.screen, (0, 255, 0), (c * self.board.SQUARESIZE + self.board.SQUARESIZE // 2,
                                                              r * self.board.SQUARESIZE + self.board.SQUARESIZE // 2),
                                   self.board.RADIUS)
            pygame.display.update()
            pygame.time.wait(200)
            self.board.draw(self.screen)
            pygame.display.update()
            pygame.time.wait(200)
        self.animate_winning_fireworks(pieces)

    def animate_winning_fireworks(self, pieces):
        """
        Displays a fireworks animation on the winning pieces.

        Parameters:
        - pieces: A list of tuples representing the coordinates of the winning pieces.
        """
        colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]
        for i in range(10):
            self.board.draw(self.screen)
            for (r, c) in pieces:
                color = colors[i % len(colors)]
                pygame.draw.circle(self.screen, color, (c * self.board.SQUARESIZE + self.board.SQUARESIZE // 2,
                                                        r * self.board.SQUARESIZE + self.board.SQUARESIZE // 2),
                                   self.board.RADIUS + i * 2)
            pygame.display.update()
            pygame.time.wait(100)

class Board:
    ROWS = 6
    COLS = 7
    SQUARESIZE = 100
    RADIUS = SQUARESIZE // 2 - 5

    def __init__(self):
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def draw(self, screen):
        for r in range(self.ROWS):
            for c in range(self.COLS):
                pygame.draw.rect(screen, (0, 0, 255), (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                if self.board[r][c] == 0:
                    pygame.draw.circle(screen, (0, 0, 0), (c * self.SQUARESIZE + self.SQUARESIZE // 2, r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE // 2), self.RADIUS)
                elif self.board[r][c] == 1:
                    pygame.draw.circle(screen, (255, 0, 0), (c * self.SQUARESIZE + self.SQUARESIZE // 2, r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE // 2), self.RADIUS)
                else:
                    pygame.draw.circle(screen, (255, 255, 0), (c * self.SQUARESIZE + self.SQUARESIZE // 2, r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE // 2), self.RADIUS)

    def animate_drop(self, screen, col, piece, sound=None):
        row = self.get_next_open_row(col)
        if row is not None:
            for r in range(row + 1):
                self.draw(screen)
                pygame.draw.circle(screen, (255, 0, 0) if piece == 1 else (255, 255, 0), (col * self.SQUARESIZE + self.SQUARESIZE // 2, r * self.SQUARESIZE + self.SQUARESIZE // 2), self.RADIUS)
                pygame.display.update()
                pygame.time.wait(50)
            self.drop_piece(row, col, piece)
            if sound:
                sound.play()
            self.bounce_effect(screen, col, row, piece)

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[0][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROWS - 1, -1, -1):
            if self.board[r][col] == 0:
                return r
        return None

    def winning_move(self, piece):
        for c in range(self.COLS - 3):
            for r in range(self.ROWS):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and self.board[r][c + 3] == piece:
                    return True

        for c in range(self.COLS):
            for r in range(self.ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and self.board[r + 3][c] == piece:
                    return True

        for c in range(self.COLS - 3):
            for r in range(self.ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    return True

        for c in range(self.COLS - 3):
            for r in range(3, self.ROWS):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    return True

        return False

    def is_draw(self):
        for c in range(self.COLS):
            if self.is_valid_location(c):
                return False
        return True

    def bounce_effect(self, screen, col, row, piece):
        for i in range(3):
            self.draw(screen)
            pygame.draw.circle(screen, (255, 0, 0) if piece == 1 else (255, 255, 0), (col * self.SQUARESIZE + self.SQUARESIZE // 2, row * self.SQUARESIZE + self.SQUARESIZE // 2 - 10), self.RADIUS)
            pygame.display.update()
            pygame.time.wait(100)
            self.draw(screen)
            pygame.draw.circle(screen, (255, 0, 0) if piece == 1 else (255, 255, 0), (col * self.SQUARESIZE + self.SQUARESIZE // 2, row * self.SQUARESIZE + self.SQUARESIZE // 2), self.RADIUS)
            pygame.display.update()
            pygame.time.wait(100)

