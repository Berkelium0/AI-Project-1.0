import numpy as np
import matplotlib.pyplot as plt


def visualize_map(data):
    print(data)
    cave_map = [[0 for x in range(18)] for y in range(12)]
    for i, line in enumerate(data):
        for j, tile in enumerate(line):
            if tile == 'S':
                cave_map[i][j] = 15
            elif tile == 'P':
                cave_map[i][j] = 10
            elif tile == ' ':
                cave_map[i][j] = 5
            elif tile == 'X':
                cave_map[i][j] = 0

    h = np.array(cave_map)
    plt.imshow(h, interpolation='none')
    plt.show()


def create_map(data):
    cave_map = [[0 for x in range(18)] for y in range(12)]
    for i, line in enumerate(data):
        for j, tile in enumerate(line):
            cave_map[i][j] = tile

    return cave_map


def find_start(cave_map):
    current_cell = {"row": 0,
                    "col": 0}
    for i in range(len(cave_map)):
        for j in range(len(cave_map[i])):
            cell = cave_map[i][j]
            if cell == "S":
                current_cell["row"] = i
                current_cell["col"] = j

    return current_cell


def get_neighbors(cave_map, i, j):
    if i != 0:
        n = cave_map[i - 1][j]
    else:
        n = 'X'
    if j != 17:
        e = cave_map[i][j + 1]
    else:
        e = 'X'
    if i != 11:
        s = cave_map[i + 1][j]
    else:
        s = 'X'
    if j != 0:
        w = cave_map[i][j - 1]
    else:
        w = 'X'

    return {
        "N": n,
        "E": e,
        "S": s,
        "W": w
    }


def move(map, dir, cc):
    if dir == "N":
        try:
            next_cell = map[cc["row"] - 1][cc["col"]]
            if next_cell != "X":
                map[cc["row"] - 1][cc["col"]] = "O"
                cc["row"] -= 1
        except:
            pass
    elif dir == "E":
        try:
            next_cell = map[cc["row"]][cc["col"] + 1]
            if next_cell != "X":
                map[cc["row"]][cc["col"] + 1] = "O"
                cc["col"] += 1
        except:
            pass
    elif dir == "S":
        try:
            next_cell = map[cc["row"] + 1][cc["col"]]
            if next_cell != "X":
                map[cc["row"] + 1][cc["col"]] = "O"
                cc["row"] += 1
        except:
            pass
    elif dir == "W":
        try:
            next_cell = map[cc["row"]][cc["col"] - 1]
            if next_cell != "X":
                map[cc["row"]][cc["col"] - 1] = "O"
                cc["col"] -= 1
        except:
            pass

    return map, cc


def check_cave(cave_map):
    coordinates = []
    for i in range(len(cave_map)):
        for j in range(len(cave_map[i])):
            if cave_map[i][j] == " ":
                coordinates.append(f"{i},{j}")
    return coordinates


def check_plan(data):
    plan = data[1]

    cave_map = create_map(data[2:])

    current_cell = find_start(cave_map)

    for dir in plan:
        cave_map, current_cell = move(cave_map, dir, current_cell)

    result = check_cave(cave_map)
    return result


def find_plan(data):
    cave_map = create_map(data[1:])
    current_cell = find_start(cave_map)

    neighbors = get_neighbors(cave_map, current_cell["row"], current_cell["col"])


raw_data = {}
for letter in 'a':
    for number in range(20):
        path = f"example-problems/problem_{letter}_{number:02d}.txt"
        with open(path) as fp:
            raw_data[path] = fp.read()
            split_data = raw_data[path].split("\n")
            if split_data[0] == "CHECK PLAN":
                result = check_plan(split_data)
                if len(result) == 0:
                    with open(f"my-example-solutions/solution_{letter}_{number:02d}.txt", "w+") as text_file:
                        text_file.write("GOOD PLAN")
                else:
                    with open(f"my-example-solutions/solution_{letter}_{number:02d}.txt", "w+") as text_file:
                        text_file.write("BAD PLAN\n\n")
                        for coor in result:
                            x = coor.split(",")
                            text_file.write(x[1] + ", " + x[0] + "\n")


            elif split_data[0] == "FIND PLAN":
                find_plan(split_data)
