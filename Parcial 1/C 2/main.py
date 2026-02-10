from player import Maze, Player
from game import Game

if __name__ == "__main__":
    maze = Maze(rows=5, cols=10)   
    player = Player(start=(1, 1))
    game = Game(maze, player, max_attempts=3)

    game.play()
