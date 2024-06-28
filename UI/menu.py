import pygame
import sys


class Menu:
    """
    Class to handle the game menu display and interactions.
    """

    def __init__(self, screen):
        """
        Initializes the menu with the screen and background image.

        Parameters:
        - screen: The pygame screen surface where the menu will be displayed.
        """
        self.screen = screen
        self.background = pygame.image.load("assets/images/connect four template.jpeg")
        self.background = pygame.transform.scale(self.background,
                                                 (700, 600))  # Resize the background image to fit the screen size

    def display_menu(self):
        """
        Displays the menu screen and waits for user interaction.

        Returns:
        - False when the Enter key is pressed to start the game.
        """
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background,
                         (0, 50))  # Display the background image with a padding of 50 pixels from the top

        font = pygame.font.Font(None, 74)
        start_text = font.render("Press Enter to Start", True, (255, 255, 255))
        self.screen.blit(start_text, (150, 650))  # Position the text with a padding of 50 pixels from the bottom

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return False
            pygame.time.wait(10)
