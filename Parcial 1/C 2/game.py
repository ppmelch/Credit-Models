from player import Maze, Player

class Game:
    MOVES = {
        "w": (-1, 0),
        "s": (1, 0),
        "a": (0, -1),
        "d": (0, 1),
    }

    INSULTS = [
        "💥 Te estrellaste con la pared, idiota",
        "🧱 Te estrellaste con la pared, pendejo",
        "🤡 Te estrellaste con la pared, wey",
    ]

    def __init__(self, maze: Maze, player: Player, max_attempts: int = 5):
        self.maze = maze
        self.player = player
        self.attempts_left = max_attempts
        self.insult_index = 0

    def render(self):
        print(f"Intentos restantes: {self.attempts_left}")
        for r, row in enumerate(self.maze.grid):
            for c, cell in enumerate(row):
                if (r, c) == self.player.position:
                    print("P", end="")
                else:
                    print(cell, end="")
            print()
        print()

    def finished(self):
        return self.maze.get_cell(self.player.position) == "G"

    def play(self):
        while not self.finished() and self.attempts_left > 0:
            self.render()
            move = input("Move (WASD): ").lower()

            if move in self.MOVES:
                moved = self.player.move(self.MOVES[move], self.maze)

                if not moved:
                    print(self.INSULTS[self.insult_index])
                    self.insult_index += 1
                    self.attempts_left -= 1

        if self.finished():
            print("🏁 Saliste del laberinto. Increíble.")
        else:
            print("☠️ GAME OVER. La pared te humilló.")
