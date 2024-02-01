import time

def create_vehicle_map(rows, cols, vehicle_position, goal_position, obstacles):
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    grid[vehicle_position[0]][vehicle_position[1]] = 'V'
    grid[goal_position[0]][goal_position[1]] = 'G'

    for obstacle in obstacles:
        grid[obstacle[0]][obstacle[1]] = 'X'

    return grid

def display_map(grid):
    for row in grid:
        print(' '.join(row))
    print()

def move_vehicle(grid, current_position, target_position):
    x, y = current_position
    tx, ty = target_position

    if x < tx:
        x += 1  
    elif x > tx:
        x -= 1  

    if y < ty:
        y += 1 
    elif y > ty:
        y -= 1

    if grid[x][y] == 'X':
        
        y = current_position[1] + 1 if y < current_position[1] else current_position[1] - 1

    if grid[x][y] == 'X':
        print("Obstacle detected! Vehicle cannot move.")
        return current_position

    grid[current_position[0]][current_position[1]] = '.'
    grid[x][y] = 'V'

    return (x, y)

rows, cols = 10, 10

vehicle_position = (0, 1)
goal_position = (8, 7)

obstacles = [(2, 2), (4, 6), (2,4),(5,3), (7, 3), (8, 8), (5,7)]

grid = create_vehicle_map(rows, cols, vehicle_position, goal_position, obstacles)
display_map(grid)

while vehicle_position != goal_position:
    time.sleep(1)
    vehicle_position = move_vehicle(grid, vehicle_position, goal_position)
    display_map(grid)

print("Vehicle reached the goal!")
