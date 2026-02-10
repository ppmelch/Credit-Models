import random
from typing import List, Tuple

# ===== FUNCIONAL =====

def add_positions(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def is_valid_move(grid: List[List[str]], pos: Tuple[int, int]) -> bool:
    r, c = pos
    return (
        0 <= r < len(grid)
        and 0 <= c < len(grid[0])
        and grid[r][c] != "#"
    )


# ===== MAZE RANDOM =====

class Maze:
    def __init__(self, rows: int, cols: int):
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.grid = [["#" for _ in range(self.cols)] for _ in range(self.rows)]
        self._generate()

    def _generate(self):
        stack = [(1, 1)]
        self.grid[1][1] = " "

        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        while stack:
            r, c = stack[-1]
            random.shuffle(directions)

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1:
                    if self.grid[nr][nc] == "#":
                        self.grid[r + dr // 2][c + dc // 2] = " "
                        self.grid[nr][nc] = " "
                        stack.append((nr, nc))
                        break
            else:
                stack.pop()

        # Colocar meta G en una celda libre random
        free_cells = [
            (r, c)
            for r in range(1, self.rows - 1)
            for c in range(1, self.cols - 1)
            if self.grid[r][c] == " "
        ]
        gr, gc = random.choice(free_cells)
        self.grid[gr][gc] = "G"

    def is_free(self, pos: Tuple[int, int]) -> bool:
        return is_valid_move(self.grid, pos)

    def get_cell(self, pos: Tuple[int, int]) -> str:
        r, c = pos
        return self.grid[r][c]


class Player:
    def __init__(self, start: Tuple[int, int]):
        self.position = start

    def move(self, direction: Tuple[int, int], maze: Maze):
        new_pos = add_positions(self.position, direction)
        if maze.is_free(new_pos):
            self.position = new_pos
            return True
        return False
