from flask import Flask, render_template, request, jsonify
import networkx as nx
import json
import os

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

        # Convert grid data to 2D array format for easier processing
        processed_grid = [['open_path' for _ in range(5)] for _ in range(5)]
        for cell in grid_data:
            row = cell['row']
            col = cell['col']
            cell_type = cell['type']
            processed_grid[row][col] = cell_type

        # Create a graph from the grid
        G = nx.grid_2d_graph(5, 5)  # Create a 5x5 grid graph
        for i in range(5):
            for j in range(5):
                for cell in grid_data:
                    if cell['row'] == i and cell['col'] == j:
                        if cell['type'] == 'block' or cell['type'] == 'obstacle':
                            if (i, j) in G.nodes():
                                G.remove_node((i, j))  # Remove blocked or obstacle nodes

        # Save the graph to a file
        nx.write_gml(G, "graph.gml")

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


if __name__ == '__main__':
    initialize_grid()
    app.run(debug=True, port=8081)