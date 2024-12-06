import pygame
import random

# Constants
WIDTH = 400
HEIGHT = 400
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
PATH_ANIMATION_SPEED = 10

# Cell states
EMPTY = 0
WALL = 1
START = 2
END = 3
PATH = 4

# Directions for movement
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = EMPTY
        self.previous = None

    def draw(self, win):
        colors = {
            EMPTY: (255, 255, 255),
            WALL: (0, 0, 0),
            START: (0, 0, 255),
            END: (255, 0, 0),
            PATH: (0, 255, 0),
        }
        color = colors[self.state]
        pygame.draw.rect(win, color, (self.col * CELL_SIZE, self.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Grid:
    def __init__(self):
        self.grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]
        self.start = self.grid[1][1]
        self.end = self.grid[ROWS - 2][COLS - 2]
        self.start.state = START
        self.end.state = END
        self.generate_maze()

    def generate_maze(self):
        for row in range(ROWS):
            for col in range(COLS):
                if random.random() < 0.3 and (row, col) != (1, 1) and (row, col) != (ROWS - 2, COLS - 2):
                    self.grid[row][col].state = WALL

    def draw(self, win):
        for row in self.grid:
            for cell in row:
                cell.draw(win)

    def find_path(self):
        open_set = [self.start]
        closed_set = set()
        
        while open_set:
            current = open_set.pop(0)
            closed_set.add(current)

            if current == self.end:
                return self.reconstruct_path(current)

            for direction in DIRECTIONS:
                neighbor_row = current.row + direction[0]
                neighbor_col = current.col + direction[1]
                
                if 0 <= neighbor_row < ROWS and 0 <= neighbor_col < COLS:
                    neighbor = self.grid[neighbor_row][neighbor_col]

                    if neighbor.state == WALL or neighbor in closed_set:
                        continue
                    
                    if neighbor not in open_set:
                        open_set.append(neighbor)
                        neighbor.previous = current

        return []  # No path found

    def reconstruct_path(self, current):
        path = []
        while current:
            path.append(current)
            current = current.previous
        return path[::-1]  # Reverse the path

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Solver")
    grid = Grid()
    path = grid.find_path()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        win.fill((0, 0, 0))
        grid.draw(win)

        # Draw the path
        for cell in path:
            cell.state = PATH
            cell.draw(win)
            pygame.display.update()
            pygame.time.delay(PATH_ANIMATION_SPEED)

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
