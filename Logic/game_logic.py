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
                if self.board.board[r][c] == piece and self.board.board[r][c + 1] == piece and self.board.board[r][
                        c + 2] == piece and self.board.board[r][c + 3] == piece:
                    self.blink_winning_pieces([(r, c), (r, c + 1), (r, c + 2), (r, c + 3)])
                    return

        for c in range(self.board.COLS):
            for r in range(self.board.ROWS - 3):
                if self.board.board[r][c] == piece and self.board.board[r + 1][c] == piece and self.board.board[r + 2][
                        c] == piece and self.board.board[r + 3][c] == piece:
                    self.blink_winning_pieces([(r, c), (r + 1, c), (r + 2, c), (r + 3, c)])
                    return

        for c in range(self.board.COLS - 3):
            for r in range(self.board.ROWS - 3):
                if self.board.board[r][c] == piece and self.board.board[r + 1][c + 1] == piece and \
                        self.board.board[r + 2][c + 2] == piece and self.board.board[r + 3][c + 3] == piece:
                    self.blink_winning_pieces([(r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3)])
                    return

        for c in range(self.board.COLS - 3):
            for r in range(3, self.board.ROWS):
                if self.board.board[r][c] == piece and self.board.board[r - 1][c + 1] == piece and \
                        self.board.board[r - 2][c + 2] == piece and self.board.board[r - 3][c + 3] == piece:
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
