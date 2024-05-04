import pygame
from client.game import Game

def main():
    pygame.init()
    
    game = Game()
    game.start()  

    pygame.quit()


if __name__ == "__main__":
    main()
