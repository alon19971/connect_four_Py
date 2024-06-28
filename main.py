import pygame
from UI.menu import Menu
from UI.game_over import GameOver
from Logic.game_logic import GameLogic


def main():
    """
    Main function that initializes and runs the Connect Four game.
    It sets up the game window, loads sounds, and manages the game loop,
    switching between the menu, game, and game over screens.
    """
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("Connect Four")
    clock = pygame.time.Clock()

    try:
        drop_sound = pygame.mixer.Sound("assets/sounds/drop.wav")
        win_sound = pygame.mixer.Sound("assets/sounds/win.wav")
    except pygame.error:
        print("Sound file not found! Ensure 'drop.wav' and 'win.wav' are in 'assets/sounds' directory.")
        drop_sound = None
        win_sound = None

    menu = Menu(screen)

    while True:
        in_menu = True
        while in_menu:
            in_menu = menu.display_menu()

        game = GameLogic(screen, drop_sound, win_sound)
        winner = game.run_game()
        game_over = GameOver(screen, winner)
        restart = game_over.display_game_over()

        if restart:
            continue
        else:
            break

    pygame.quit()


if __name__ == "__main__":
    main()
