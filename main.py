import time
from openai import OpenAI
from stockfish import Stockfish
import pygame
from pygame.locals import *

BACKGROUND_COLOR = (49, 46, 43)


class Game:
    def __init__(self):
        pygame.display.set_caption("ChessTutor (Powered by GPT)")
        self.surface = pygame.display.set_mode((1600,900))
        self.surface.fill(BACKGROUND_COLOR)
        self.clock = pygame.time.Clock()
        self.image = pygame.transform.scale(pygame.image.load("ChessTutor/board.png"), (900,860))
        self.moves = pygame.transform.scale(pygame.image.load("ChessTutor/Moves of the king.png"), (300, 300))
        self.surface.blit(self.image, (0,0))
        self.surface.blit(self.moves, (1000,0))
        pygame.display.flip()

        # Change all of this to be a part of the game object not board

    def run(self):

        # placeholder standard pygame controls
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    time.sleep(0)
                    # self.play()
            except Exception as e:
                # self.show_game_over()
                pause = True
                # self.reset()

            time.sleep(0.3)


if __name__ == "__main__":
    game = Game()
    game.run()
    # Oh boy