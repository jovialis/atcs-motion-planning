import random
import math

# SETUP VARIABLES
SIZE = 100
GRID = None

START_COORDINATES = (-1, -1)
END_COORDINATES = (-1, -1)

def main():
    # INITIAL VARIABLES
    reset_grid()

    while not do_user_interface():
        pass

    print('Thanks for running!')

##############################
# Interface
##############################

# https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
# An enum which represents string color values.
class Color:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLACK = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Formats and prints a UI page with a given title
def user_interface_header(title):
    print(Color.BLACK + '')
    print(''.join([ '*' for i in range(SIZE) ]))
    print(Color.BOLD + title.upper().strip() + Color.BLACK)

# Gets the user's selected menu option.
def get_user_input(inputs):
    user_in = ''

    while user_in not in inputs:
        user_in = input().upper().strip()

        if user_in not in inputs:
            print('Select a valid option.')

    return inputs[user_in]

# Fetches user coordinates. If multiple, more than one. If separateSingleLine multiple coordinate pairs can be entered on a single line.
def get_user_input_coordinates(multiple = True, separateSingleLine = True, message = None):
    user_interface_header('Enter Coordinates - X,Y')

    if message is not None:
        print(message)

    if multiple:
        print('X > Exit')

    print('')

    coordinates = []

    # Allow input on one line or multiple
    while multiple or (len(coordinates) < 1):
        line_in = input().upper().strip()

        if line_in == 'X':
            break

        # Allow entering multiple coordinates one line
        line_in = line_in.split(' ')

        # For nonseparated coordinates, append all coordinates on this line to line_list
        line_list = []
        for unparsed in line_in:
            try:
                split = unparsed.split(',')
                x = int(split[0])
                y = int(split[1])

                if x > SIZE or y > SIZE or x < 0 or y < 0:
                    print('Coordinate', unparsed, 'is outside graph bounds.')
                    continue

                # If we separate it, we append the coordinate to the main list
                if separateSingleLine:
                    coordinates.append((x, y))
                # Otherwise append the coordinates from this line to a smaller list
                else:
                    line_list.append((x, y))
            except:
                print('Coordinate', unparsed, 'should be formatted X,Y')

        if not separateSingleLine and len(line_list) > 0:
            coordinates.append(line_list)

    if multiple:
        return coordinates

    return coordinates[0]

# UI Entry point
def do_user_interface():
    user_interface_header('Graph Theory - Lab 5')

    print('A > Graph Setup')

    operations = {
        'A': do_user_interface_graph,
        'B': do_user_interface_points,
        'Q': None
    }

    # Handles whether or not the program can be run, as well as the 'red' for unfinished menus.
    if start_end_ready():
        print('B > Set Start/End Points')

        print('C > Run')
        operations['C'] = do_user_interface_run
    else:
        print(Color.RED + 'B > Set Start/End Points' + Color.BLACK)

    print('')
    print('Q > Quit')

    operation = get_user_input(operations)

    # We picked the exit function
    if operation is None:
        return True

    while not operation():
        pass

    return False

# UI Graph menu
def do_user_interface_graph():
    user_interface_header('Graph Setup')

    print('A > Print Current Graph')
    print('B > Add Obstacle')
    print('C > Generate Obstacles')
    print('D > Reset Graph')
    print('')
    print('X > Exit')

    operation = get_user_input({
        'A': do_user_interface_graph_print,
        'B': do_user_interface_graph_obstacle_add,
        'C': do_user_interface_graph_obstacle_generate,
        'D': do_user_interface_graph_reset,
        'X': None
    })

    # We picked the exit function
    if operation is None:
        return True

    while not operation():
        pass

    return False

# Print graph option
def do_user_interface_graph_print():
    user_interface_header('GRAPH PRINTOUT')
    print_grid()
    return True

# Add obstacles menu.
def do_user_interface_graph_obstacle_add():
    global GRID

    coordinates = get_user_input_coordinates(True, separateSingleLine=False, message='(Enter two coordinates on a line to define corners)')

    for coordinate_list in coordinates:
        # Corners given
        if len(coordinate_list) > 1:
            corner_a = coordinate_list[0]
            corner_b = coordinate_list[1]

            # Iterate through each item between the points.
            for x in range(min(corner_a[0], corner_b[0]), max(corner_a[0], corner_b[0]) + 1):
                for y in range(min(corner_a[1], corner_b[1]), max(corner_a[1], corner_b[1]) + 1):
                    if grid_empty_at((x, y)):
                        set_grid_value_at((x, y), 1)
        # Single point addition
        else:
            coordinate = coordinate_list[0]

            if grid_empty_at((coordinate[0], coordinate[1])):
                set_grid_value_at((coordinate[0], coordinate[1]), 1)

    return True

# Generate obstacles option
def do_user_interface_graph_obstacle_generate():
    user_interface_header('GENERATE OBSTACLES')
    print('How many obstacles would you like to generate?')

    user_in = -1

    while user_in is -1:
        user_in = int(input())

        try:

            if user_in < 0:
                print('Obstacles must be positive.')
                user_input = -1
        except:
            print('Number', user_in, 'is not valid.')

    generate_random_obstacles(user_in)

    print('Generated obstacles.')

    return True

# Reset graph option
def do_user_interface_graph_reset():
    reset_grid()
    print('Graph reset.')
    return True

# Change start/endpoint menu
def do_user_interface_points():
    global GRID
    global START_COORDINATES

    # Objects which are displayed in the menu
    start = START_COORDINATES
    end = END_COORDINATES

    # If unset, just set the objs to None to make it prettier
    if START_COORDINATES == (-1, -1):
        start = None

    if END_COORDINATES == (-1, -1):
        end = None

    user_interface_header('Enter Key Points')

    print('A > Edit Start:', start)
    print('B > Edit End:', end)
    print('')
    print('X > Exit')

    # Edit start option
    def edit_start():
        global GRID
        global START_COORDINATES

        set_grid_value_at(START_COORDINATES, 0)
        START_COORDINATES = (-1, -1)

        coordinate = get_user_input_coordinates(False)
        set_grid_value_at(coordinate, 2)

        START_COORDINATES = coordinate

    def edit_end():
        global GRID
        global END_COORDINATES

        set_grid_value_at(END_COORDINATES, 0)
        END_COORDINATES = (-1, -1)

        coordinate = get_user_input_coordinates(False)
        set_grid_value_at(coordinate, 3)

        END_COORDINATES = coordinate

    operation = get_user_input({
        'A': edit_start,
        'B': edit_end,
        'X': None
    })

    if operation == None:
        return True

    operation()
    return False

# Move operation to the graph methods!
def do_user_interface_run():
    intermediary_points = do_route()
    print_grid(intermediary_points)

    if intermediary_points is None:
        print('Could not find a pathway. Is something detached?')

    return True

##################################
# Graph Methods
##################################

# Regenerates the GRID object with a matrix of zeroes.
def reset_grid():
    global GRID
    global OBSTACLE_COUNT

    GRID = []
    for x in range(SIZE):
        r = []
        for y in range(SIZE):
            r.append(0)
        GRID.append(r)

    OBSTACLE_COUNT = 0

    # Legacy start/end points
    set_grid_value_at(START_COORDINATES, 2)
    set_grid_value_at(END_COORDINATES, 3)

# Generates random objects by finding a random point on the grid, selecting a size, then going out size/2 in all directions.
def generate_random_obstacles(number):
    global GRID
    global OBSTACLE_COUNT

    # Number of obstacles generated
    i = 0

    # While we still have obstacles to generate and there are still spaces to do so
    while i <= number and OBSTACLE_COUNT <= SIZE**2:
        randx = random.randint(0, len(GRID) - 1)
        randy = random.randint(0, len(GRID[0]) - 1)

        # Generate obstacles of size 1 --> 6
        obstacle_size = random.randint(1, 6)

        for ix in range(int(-math.floor(obstacle_size / 2)), math.ceil(obstacle_size / 2)):
            for iy in range(int(-math.floor(obstacle_size / 2)), math.ceil(obstacle_size / 2)):

                # Ensure that we don't go over.
                if i >= number or OBSTACLE_COUNT > SIZE**2:
                    return

                new_coords = (randx + ix, randy + iy)

                if not within_grid(new_coords):
                    continue

                if not grid_empty_at(new_coords):
                    continue

                set_grid_value_at(new_coords, 1)

                OBSTACLE_COUNT += 1

        i += 1

    return

# Determines whether or not the START and END coordinates are ready to go.
def start_end_ready():
    return START_COORDINATES[0] != -1 and END_COORDINATES[0] != -1

# Actually performs the routing.
def do_route():
    # Build network of nodes
    network = generate_network(START_COORDINATES, END_COORDINATES)
    # Navigate the network
    intermediary_coordinates = perform_routing(network)

    return intermediary_coordinates

def get_grid_value_at(coordinate_pair):
    return GRID[coordinate_pair[0]][coordinate_pair[1]]

def set_grid_value_at(coordinate_pair, value):
    global GRID
    if within_grid(coordinate_pair):
        GRID[coordinate_pair[0]][coordinate_pair[1]] = value

def grid_empty_at(coordinate_pair):
    return get_grid_value_at(coordinate_pair) == 0

def within_grid(coordinate_pair):
    return coordinate_pair[0] >= 0 and coordinate_pair[0] < SIZE and coordinate_pair[1] >= 0 and coordinate_pair[1] < SIZE

###########################
# Routing
###########################

# Represents an edge from one node to another.
class Edge:
    to = None
    length = None

    def __init__(self, to, length):
        self.to = to
        self.length = length

# Represents a node.
class Node:
    coordinates = None
    distance = -1
    predecessor = None

    def __init__(self):
        self.distance = math.inf
        self.predecessor = None
        self.coordinates = None

# Generates a map of node: [edge] where the edges are a wrapper for an adjacent node.
def generate_network(start_coords, end_coords):
    # Maps coordinates to nodes for easy access
    coords_node_map = {}
    # Maps nodes to edges
    node_edge_map = {}

    for x in range(SIZE):
        for y in range(SIZE):
            coords = (x, y)

            # Ignore barriers
            if get_grid_value_at(coords) == 1:
                continue

            # Find the node for this point
            node = get_node_for_coords(coords, coords_node_map)

            edges = []

            # Get blocks around this point.
            for oX in range(-1, 2):
                for oY in range(-1, 2):
                    # Ignore origin point
                    if oX == 0 and oY == 0:
                        continue

                    adjusted_coords = (x + oX, y + oY)

                    # Ignore if the point is outside bounds
                    if not within_grid(adjusted_coords):
                        continue

                    # Ignore if the point is an obstacle
                    if get_grid_value_at(adjusted_coords) == 1:
                        continue

                    # Find the node this edge goes to
                    to_node = get_node_for_coords(adjusted_coords, coords_node_map)

                    # Distance formula to get distance between things.
                    distance = math.sqrt(oX ** 2 + oY ** 2)

                    edge = Edge(to_node, distance)
                    edges.append(edge)

            node_edge_map[node] = edges

    # Store start/end nodes for easy access.
    start_node = coords_node_map[start_coords]
    end_node = coords_node_map[end_coords]

    # If we for some reason don't have a node for the start/end coordinates, something went wrong. This should never happen.
    if start_node is None or end_node is None:
        print('An error occurred while generating network.')
        return

    return (node_edge_map, start_node, end_node)

# Generates a node object and maps it to the coordinates if it doesn't already exist.
def get_node_for_coords(coords, map):
    if coords not in map:
        node = Node()
        node.coordinates = coords
        map[coords] = node
    return map[coords]

# Recieves the network, performs routing using Dijkstra's algorithm.
def perform_routing(network_package):
    node_map = network_package[0]
    starting_node = network_package[1]
    ending_node = network_package[2]

    # Starting node is the first node we work with.
    cur_node = starting_node
    cur_node.distance = 0

    # Store visited/unvisited nodes.
    visited_nodes = set()
    unvisited_nodes = list(node_map.keys())

    while True:
        # Update whether the current node has been visited
        visited_nodes.add(cur_node)
        unvisited_nodes.remove(cur_node)

        edges = node_map[cur_node]

        for edge in edges:
            # Ignore nodes we've already visited
            if edge.to in visited_nodes:
                continue

            # Calculate the distance to that new node
            distance = cur_node.distance + edge.length

            # If the distance is less than what it currently has, the child node has this as its parent.
            if distance < edge.to.distance:
                edge.to.distance = distance
                edge.to.predecessor = cur_node

        # If ending node has been visited, we can quit
        if ending_node.predecessor is not None:
            break

        # If no nodes left unvisited we return
        if len(unvisited_nodes) == 0:
            return None

        # Discover next cur_node as the one with the least distance
        def sort_by(node):
            return node.distance

        unvisited_nodes.sort(key=sort_by)
        least_node = unvisited_nodes[0]

        # If the least node has a distance of infinity, something's messed up and we're not connected to the rest of the graph anymore.
        if least_node.distance == math.inf:
            return None

        cur_node = least_node

    # Go back up through the coordinate chain starting with the end node and getting its parents, etc.
    intermediary_coordinates = []
    cur_backtrace_node = ending_node
    while cur_backtrace_node is not None:
        cur_backtrace_node = cur_backtrace_node.predecessor

        if cur_backtrace_node is None:
            break

        intermediary_coordinates.append(cur_backtrace_node.coordinates)

    return intermediary_coordinates

# Prints the grid.
def print_grid(intermediary_coordinates = None):
    for ix in range(SIZE):
        line = ''

        for iy in range(SIZE):
            # Have to flip x and y to ensure that we orient correctly.
            p = GRID[iy][ix]

            character = ''

            if p == 2:
                character += Color.BLUE + Color.BOLD + '● '
            elif p == 3:
                character += Color.BLUE + Color.BOLD + 'X '
            elif intermediary_coordinates is not None and (iy, ix) in intermediary_coordinates:
                character += Color.RED + '● '
            elif p == 1:
                character += Color.BLACK + '█ '
            else:
                character += Color.BLACK + '. '

            line += character

        print(line.strip(), Color.BLACK)

main()