from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)

# Global variables
rows, cols = 10, 10
vehicle_position = (rows // 2, cols // 2)
goal_position = (0, 2)
obstacles = [(2, 2), (4, 6), (7, 3), (8, 8)]  # Added four obstacles
grid = [['.' for _ in range(cols)] for _ in range(rows)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_map', methods=['GET'])
def get_map():
    return jsonify({'grid': grid, 'vehicle_position': vehicle_position, 'goal_position': goal_position})

@app.route('/move_vehicle', methods=['POST'])
def move_vehicle():
    global vehicle_position
    time.sleep(1)  # Simulating a delay for better visualization
    vehicle_position = move_vehicle_logic(vehicle_position, goal_position)
    if vehicle_position == goal_position:
        stop_simulation()
    return jsonify({'success': True})

def move_vehicle_logic(current_position, target_position):
    x, y = current_position
    tx, ty = target_position

    if x < tx:
        x += 1
    elif x > tx:
        x -= 1

    # Allow the vehicle to move forward even if there's an obstacle
    if y < ty:
        y += 1
    elif y > ty:
        y -= 1

    if grid[x][y] == 'X':
        # If there's an obstacle, try sideward movement instead
        y = current_position[1] + 1 if y < current_position[1] else current_position[1] - 1

    if grid[x][y] == 'X':
        return current_position

    grid[current_position[0]][current_position[1]] = '.'
    grid[x][y] = 'V'

    return (x, y)

def stop_simulation():
    print("Goal reached! Stopping the simulation.")
    global vehicle_position
    vehicle_position = goal_position  # Stop the vehicle at the goal

if __name__ == '__main__':
    app.run(debug=True)
