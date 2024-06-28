import pygame
import sys


class GameOver:
    """
    Class to handle the game over screen display and interactions.
    """

    def __init__(self, screen, winner):
        """
        Initializes the game over screen with the screen and winner information.

        Parameters:
        - screen: The pygame screen surface where the game over screen will be displayed.
        - winner: The player who won the game (1 or 2). If 0, it indicates a draw.
        """
        self.screen = screen
        self.winner = winner
        self.background = pygame.image.load("assets/images/game over background.jpg")
        self.background = pygame.transform.scale(self.background,
                                                 (700, 600))  # Resize the background image to fit the screen size

    def display_game_over(self):
        """
        Displays the game over screen and waits for user interaction.

        Returns:
        - True if the Enter key is pressed to restart the game.
        - False if the Escape key is pressed to quit the game.
        """
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background,
                         (0, 50))  # Display the background image with a padding of 50 pixels from the top

        font = pygame.font.Font(None, 74)
        if self.winner == 0:
            text = font.render("Draw!", True, (255, 255, 255))
        else:
            text = font.render(f"Player {self.winner} wins!", True, (255, 255, 255))
        self.screen.blit(text, (200, 100))  # Center the text

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press Enter to Restart", True, (255, 255, 255))
        quit_text = font.render("Press Esc to Quit", True, (255, 255, 255))
        self.screen.blit(restart_text, (200, 550))  # Center the restart text below "Game Over"
        self.screen.blit(quit_text, (200, 500))  # Center the quit text below the restart text

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False
            pygame.time.wait(10)
