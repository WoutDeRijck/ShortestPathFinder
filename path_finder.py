import curses
from curses import wrapper
import queue
import time

from sklearn import neighbors


maze = [
    ["#", "#", "#", "#", "#", "O", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i*2, j*3, "X", RED)
            else:
                stdscr.addstr(i*2, j*3, value, BLUE)

def find_start(maze, startsymbol):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == startsymbol:
                return i, j
    return None

def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    # Tuple (current pos, path to pos)
    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end:
            return path
        
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            
            r, c = neighbor
            if maze[r][c] == "#":
                continue
            
            q.put((neighbor, path + [neighbor]))
            visited.add(neighbor)
        
def find_neighbors(maze, row, col):
    neighbors = []

    # UP
    if row > 0:
        neighbors.append((row - 1, col))

    # DOWN
    if row + 1 < len(maze):
        neighbors.append((row + 1, col))
    
    # LEFT
    if col > 0:
        neighbors.append((row, col - 1))

    # RIGHT
    if col + 1< len(maze[0]):
        neighbors.append((row, col + 1))
    return neighbors

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()

wrapper(main)