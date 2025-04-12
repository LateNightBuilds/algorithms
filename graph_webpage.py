import json
from typing import List, Dict

from flask import Flask, render_template, request, jsonify

from graph.shortest_path.methods import ShortestPathMethod
from graph.utils import GridCellType
from graph.utils.utils import grid_to_graph
from graph_client import run_shortest_path

app = Flask(__name__)

grid = []


# Initialize grid
def initialize_grid():
    global grid
    grid = [['open_path' for _ in range(5)] for _ in range(5)]
    grid[0][0] = 'start'
    grid[4][4] = 'end'


@app.route('/')
def index():
    return render_template('grid.html')


@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    row, col, brick_type = data['row'], data['col'], data['type']
    grid[row][col] = brick_type
    return jsonify({"message": "Grid updated!"})


@app.route('/reset', methods=['POST'])
def reset():
    initialize_grid()
    return jsonify({"message": "Grid reset!"})


@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    try:
        data = request.get_json()
        algorithm = data['algorithm']
        grid_data = data['grid']

        # Verify that start and end are present
        has_start = False
        has_end = False
        for cell in grid_data:
            if cell['type'] == 'start':
                has_start = True
            elif cell['type'] == 'end':
                has_end = True

            if has_start and has_end:
                break

        if not (has_start and has_end):
            missing = []
            if not has_start: missing.append("start")
            if not has_end: missing.append("end")
            return jsonify({
                "message": f"Missing required bricks: {', '.join(missing)}"
            }), 400

        input_data = convert_html_cell_type_to_grid_cell_type(html_grid=grid_data)
        method = convert_html_algorithm_type_to_algorithm_method(html_algorithm_type=algorithm)
        graph = grid_to_graph(input_data=input_data)
        cost, history = run_shortest_path(g=graph, method=method)

        # Create the result object to save
        result_data = {
            'algorithm': algorithm,
            'grid': grid_data
        }

        # Save the grid data as JSON for future reference
        with open('grid_data.json', 'w') as f:
            json.dump(result_data, f, indent=2)

        return jsonify({
            "message": f"Algorithm {algorithm} completed successfully. Graph saved as graph.gml and grid saved as grid_data.json"
        })

    except Exception as e:
        print(f"Error in run_algorithm: {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"}), 500


def convert_html_cell_type_to_grid_cell_type(html_grid: List[Dict]) -> List[List[GridCellType]]:
    processed_grid = [[GridCellType.OPEN_PATH for _ in range(5)] for _ in range(5)]

    html_cell_type_to_grid_cell_type = {'start': GridCellType.START,
                                        'end': GridCellType.END,
                                        'open_path': GridCellType.OPEN_PATH,
                                        'block': GridCellType.BLOCK,
                                        'obstacle': GridCellType.OBSTACLE}

    for cell in html_grid:
        row = cell['row']
        col = cell['col']
        cell_type = cell['type']
        processed_grid[row][col] = html_cell_type_to_grid_cell_type[cell_type]

    return processed_grid


def convert_html_algorithm_type_to_algorithm_method(html_algorithm_type: str) -> ShortestPathMethod:
    if html_algorithm_type == 'dijkstra':
        return ShortestPathMethod.DIJKSTRA
    elif html_algorithm_type == 'a_star':
        return ShortestPathMethod.A_STAR


if __name__ == '__main__':
    initialize_grid()
    app.run(debug=True, port=8081)
