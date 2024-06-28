import pygame


class Board:
    """
    Class that handles the board logic for Connect Four.
    """
    ROWS = 6
    COLS = 7
    SQUARESIZE = 100
    RADIUS = SQUARESIZE // 2 - 5

    def __init__(self):
        """
        Initializes an empty board.
        """
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def draw(self, screen):
        """
        Draws the board on the screen.

        Parameters:
        - screen: The pygame screen surface where the board will be drawn.
        """
        for r in range(self.ROWS):
            for c in range(self.COLS):
                pygame.draw.rect(screen, (0, 0, 255), (
                c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                if self.board[r][c] == 0:
                    pygame.draw.circle(screen, (0, 0, 0), (c * self.SQUARESIZE + self.SQUARESIZE // 2,
                                                           r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE // 2),
                                       self.RADIUS)
                elif self.board[r][c] == 1:
                    pygame.draw.circle(screen, (255, 0, 0), (c * self.SQUARESIZE + self.SQUARESIZE // 2,
                                                             r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE // 2),
                                       self.RADIUS)
                else:
                    pygame.draw.circle(screen, (255, 255, 0), (c * self.SQUARESIZE + self.SQUARESIZE // 2,
                                                               r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE // 2),
                                       self.RADIUS)

    def animate_drop(self, screen, col, piece, sound=None):
        """
        Animates the drop of a piece into the board.

        Parameters:
        - screen: The pygame screen surface where the animation will be drawn.
        - col: The column where the piece will be dropped.
        - piece: The player's piece (1 or 2) to be dropped.
        - sound: The sound to play when the piece is dropped (optional).
        """
        row = self.get_next_open_row(col)
        if row is not None:
            for r in range(row + 1):
                self.draw(screen)
                pygame.draw.circle(screen, (255, 0, 0) if piece == 1 else (255, 255, 0), (
                    col * self.SQUARESIZE + self.SQUARESIZE // 2, r * self.SQUARESIZE + self.SQUARESIZE // 2), self.RADIUS)
                pygame.display.update()
                pygame.time.wait(50)
            self.drop_piece(row, col, piece)
            if sound:
                sound.play()
            self.bounce_effect(screen, col, row, piece)

    def drop_piece(self, row, col, piece):
        """
        Drops a piece into the board at the specified location.

        Parameters:
        - row: The row where the piece will be placed.
        - col: The column where the piece will be placed.
        - piece: The player's piece (1 or 2) to be placed.
        """
        self.board[row][col] = piece

    def is_valid_location(self, col):
        """
        Checks if the column can accept another piece.

        Parameters:
        - col: The column to check.

        Returns:
        - True if the column can accept another piece, False otherwise.
        """
        return self.board[0][col] == 0

    def get_next_open_row(self, col):
        """
        Gets the next open row in the column.

        Parameters:
        - col: The column to check.

        Returns:
        - The row number of the next open row, or None if the column is full.
        """
        for r in range(self.ROWS - 1, -1, -1):
            if self.board[r][col] == 0:
                return r
        return None

    def winning_move(self, piece):
        """
        Checks if the given piece has a winning move.

        Parameters:
        - piece: The player's piece (1 or 2) to check.

        Returns:
        - True if the piece has a winning move, False otherwise.
        """
        for c in range(self.COLS - 3):
            for r in range(self.ROWS):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and \
                        self.board[r][c + 3] == piece:
                    return True

        for c in range(self.COLS):
            for r in range(self.ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and \
                        self.board[r + 3][c] == piece:
                    return True

        for c in range(self.COLS - 3):
            for r in range(self.ROWS - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][
                       c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    return True

        for c in range(self.COLS - 3):
            for r in range(3, self.ROWS):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][
                       c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    return True

        return False

    def is_draw(self):
        """
        Checks if the game is a draw.

        Returns:
        - True if the game is a draw, False otherwise.
        """
        for c in range(self.COLS):
            if self.is_valid_location(c):
                return False
        return True

    def bounce_effect(self, screen, col, row, piece):
        """
        Animates a bounce effect when a piece is dropped.

        Parameters:
        - screen: The pygame screen surface where the animation will be drawn.
        - col: The column where the piece was dropped.
        - row: The row where the piece was placed.
        - piece: The player's piece (1 or 2) that was placed.
        """
        for i in range(3):
            self.draw(screen)
            pygame.draw.circle(screen, (255, 0, 0) if piece == 1 else (255, 255, 0), (
                col * self.SQUARESIZE + self.SQUARESIZE // 2, row * self.SQUARESIZE + self.SQUARESIZE // 2 - 10),
                               self.RADIUS)
            pygame.display.update()
            pygame.time.wait(100)
            self.draw(screen)
            pygame.draw.circle(screen, (255, 0, 0) if piece == 1 else (255, 255, 0), (
                col * self.SQUARESIZE + self.SQUARESIZE // 2, row * self.SQUARESIZE + self.SQUARESIZE // 2), self.RADIUS)
            pygame.display.update()
            pygame.time.wait(100)
