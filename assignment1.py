#Assignment 1 COMP3106
#Kajani Yogarajah 101275130
import csv
from functools import partial

#goal for treasure value to be collected_values
TARGET_VAL = 5
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

#simple file reader function to load grid from csv file and strip each grid line
def load_grid(filepath):
    with open(filepath, newline="") as f:
        return [[cell.strip().upper() for cell in row] for row in csv.reader(f) if row]

#finds coordinates for the target value (ex. "S" or "G") in the provided grid
def find_cells(grid, target):
    return [(r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == target]

#converts treasure values in grid to actual integer values
def convert_value(grid, pos):
    v = grid[pos[0]][pos[1]]
    return int(v) if v in ("1", "2", "3", "4", "5") else 0

#current collected_values nodes
def collected_values(grid, node):
    return frozenset(p for p in node if convert_value(grid, p) > 0)

#total value of explored path
def total_value(grid, node):
    return sum(convert_value(grid, p) for p in collected_values(grid, node))

#identifies a search state by the agent's position and collected_values treasure cells
def node_key(grid, node):
    return (node[-1], collected_values(grid, node))

#expands possible moves agent can take
def expand(grid, node):
    r, c = node[-1]
    children = []
    for dr, dc in MOVES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] != "X":
            children.append(node + [(nr, nc)])
    return children

#idenitfies goal state
def g_isGoal(grid, goals, node):
    return node[-1] in goals and total_value(grid, node) >= TARGET_VAL

#cost of path so far
def g(node):
    return len(node) - 1

#cost of remaining distance (manhattan function)
def h(goals, node):
    r, c = node[-1]
    return min(abs(r - gr) + abs(c - gc) for gr, gc in goals) if goals else 0


# A star search, function take from Zinovi Rabinovich Lesson 4 A star search example (return values altered to match assignment expectation)
def a_star_search(startState, expFun, isGoal, gValue, hValue, keyFun):
    startNode = [startState]
    frontier = {keyFun(startNode): {'node':startNode, 'val':gValue(startNode), 'hval':hValue(startNode)}}
    explored = {}

    while frontier:
        minKey = min(frontier, key=lambda k: frontier[k]['val'] + frontier[k]['hval'])
        data = frontier.pop(minKey)
        explored[minKey] = data
        node = data['node']

        if isGoal(node):
            return node, gValue(node), len(explored)
        for eNode in expFun(node):
            newKey = keyFun(eNode)
            newVal = gValue(eNode)
            newData = {'node': eNode, 'val': newVal, 'hval': hValue(eNode)}
            if newKey in frontier:
                if newVal < frontier[newKey]['val']:
                    frontier[newKey] = newData
            elif newKey in explored:
                if newVal < explored[newKey]['val']:
                    explored[newKey] = newData
            else:
                frontier[newKey] = newData
    return None, None, len(explored)

#pathfinding function, loads grid from csv file and applies A star search function
def pathfinding(filepath):
    grid = load_grid(filepath)
    start = find_cells(grid, "S")[0]
    goals = set(find_cells(grid, "G"))

    optimal_path, optimal_path_cost, num_states_explored = a_star_search(
        startState = start,
        expFun     = partial(expand, grid),
        isGoal = partial(g_isGoal, grid, goals),
        gValue     = g,
        hValue     = partial(h, goals),
        keyFun     = partial(node_key, grid),
    )
    return optimal_path, optimal_path_cost, num_states_explored