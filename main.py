# import numpy as np
# import matplotlib.pyplot as plt
# def visualize_map(data):
#     print(data)
#     cave_map = [[0 for x in range(18)] for y in range(12)]
#     for i, line in enumerate(data):
#         for j, tile in enumerate(line):
#             if tile == 'S':
#                 cave_map[i][j] = 15
#             elif tile == 'P':
#                 cave_map[i][j] = 10
#             elif tile == ' ':
#                 cave_map[i][j] = 5
#             elif tile == 'X':
#                 cave_map[i][j] = 0
#
#     h = np.array(cave_map)
#     plt.imshow(h, interpolation='none')
#     plt.show()


def create_map(data):
    portal_coor = {}
    portal_num = 0
    cave_map = [[0 for x in range(18)] for y in range(12)]
    for i, line in enumerate(data):
        for j, tile in enumerate(line):
            cave_map[i][j] = tile
            if tile == "P":
                portal_coor[f"portal_{portal_num}_row"] = i
                portal_coor[f"portal_{portal_num}_col"] = j
                portal_num += 1
    return cave_map, portal_coor


def find_start(cave_map):
    possible_starts = []
    start_flag = False
    start_cell = {"row": 0,
                  "col": 0}
    for i in range(len(cave_map)):
        for j in range(len(cave_map[i])):
            cell = cave_map[i][j]
            if cell == " ":
                possible_starts.append(f"{i},{j}")
            elif cell == "S":
                start_cell["row"] = i
                start_cell["col"] = j
                start_flag = True

    if start_flag:
        return start_cell
    else:
        return possible_starts


def get_neighbors(cave_map, cc):
    if type(cc) == dict:
        i, j = cc["row"], cc["col"]
    else:
        i, j = cc

    n = cave_map[i - 1][j]
    e = cave_map[i][j + 1]
    s = cave_map[i + 1][j]
    w = cave_map[i][j - 1]

    return {
        "E": e,
        "S": s,
        "W": w,
        "N": n
    }


def teleport(cc, pc):
    if cc["row"] == pc["portal_0_row"] and cc["col"] == pc["portal_0_col"]:
        cc["row"] = pc["portal_1_row"]
        cc["col"] = pc["portal_1_col"]
    elif cc["row"] == pc["portal_1_row"] and cc["col"] == pc["portal_1_col"]:
        cc["row"] = pc["portal_0_row"]
        cc["col"] = pc["portal_0_col"]
    return cc


def move(map, dir, cc, pc, type="check"):
    if dir == "N":
        next_cell = map[cc["row"] - 1][cc["col"]]
        if next_cell == "P":
            cc["row"] -= 1
            cc = teleport(cc, pc)
        elif next_cell != "X":
            if next_cell != "S":
                map[cc["row"] - 1][cc["col"]] = "O"
            cc["row"] -= 1

    elif dir == "E":
        next_cell = map[cc["row"]][cc["col"] + 1]
        if next_cell == "P":
            cc["col"] += 1
            cc = teleport(cc, pc)
        elif next_cell != "X":
            if next_cell != "S":
                map[cc["row"]][cc["col"] + 1] = "O"
            cc["col"] += 1

    elif dir == "S":
        next_cell = map[cc["row"] + 1][cc["col"]]
        if next_cell == "P":
            cc["row"] += 1
            cc = teleport(cc, pc)
        elif next_cell != "X":
            if next_cell != "S":
                map[cc["row"] + 1][cc["col"]] = "O"
            cc["row"] += 1

    elif dir == "W":
        next_cell = map[cc["row"]][cc["col"] - 1]
        if next_cell == "P":
            cc["col"] -= 1
            cc = teleport(cc, pc)
        elif next_cell != "X":
            if next_cell != "s":
                map[cc["row"]][cc["col"] - 1] = "O"
            cc["col"] -= 1

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

    cave_map, portal_coor = create_map(data[2:])

    current_cell = find_start(cave_map)
    if type(current_cell) == dict:
        for direction in plan:
            cave_map, current_cell = move(cave_map, direction, current_cell, portal_coor)

        res = check_cave(cave_map)
        return res
    elif type(current_cell) == list:
        res = set([])
        for possible_start in current_cell:
            x = possible_start.split(",")
            possible_current_cell = {"row": int(x[0]), "col": int(x[1])}
            temp_cave_map = [x[:] for x in cave_map]
            temp_cave_map[possible_current_cell["row"]][possible_current_cell["col"]] = "S"
            for direction in plan:
                temp_cave_map, possible_current_cell = move(temp_cave_map, direction, possible_current_cell,
                                                            portal_coor)

            blank_cells = check_cave(temp_cave_map)
            for cells in blank_cells:
                res.add(cells)
        return res


def find_direction(dirty_cell, current_cell, portal_coor):
    if current_cell == (portal_coor["portal_0_row"], portal_coor["portal_0_col"]):
        current_cell = portal_coor["portal_1_row"], portal_coor["portal_1_col"]
    elif current_cell == (portal_coor["portal_1_row"], portal_coor["portal_1_col"]):
        current_cell = portal_coor["portal_0_row"], portal_coor["portal_0_col"]
    if type(dirty_cell) == dict:
        dx = dirty_cell["row"] - current_cell["row"]
        dy = dirty_cell["col"] - current_cell["col"]
    elif type(dirty_cell) == tuple:
        dx = dirty_cell[0] - current_cell[0]
        dy = dirty_cell[1] - current_cell[1]
    if abs(dx) > abs(dy):
        dy = 0
    else:
        dx = 0
    print(dx, dy)
    if dx > 0:
        return "S"
    elif dy > 0:
        return "E"
    elif dx < 0:
        return "N"
    elif dy < 0:
        return "W"


def dfs(cave_map, current_cell, dirty_cell, portal_coor):
    visited = [[False for _ in range(len(cave_map[0]))] for _ in range(len(cave_map))]
    stack = [(current_cell["row"], current_cell["col"], [])]
    while stack:
        row, col, path = stack.pop()
        if (row, col) == (dirty_cell["row"], dirty_cell["col"]):
            for r, c in path:
                cave_map[r][c] = "O"
            return path
        visited[row][col] = True
        if (row, col) == (portal_coor["portal_0_row"], portal_coor["portal_0_col"]):
            row, col = portal_coor["portal_1_row"], portal_coor["portal_1_col"]
        elif (row, col) == (portal_coor["portal_1_row"], portal_coor["portal_1_col"]):
            visited[row][col] = True
            row, col = portal_coor["portal_0_row"], portal_coor["portal_0_col"]
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for r, c in neighbors:
            if 0 <= r < len(cave_map) and 0 <= c < len(cave_map[0]) and cave_map[r][c] != "X" and not visited[r][c]:
                # if cave_map[r][c] == "P":
                #     if (r, c) == (portal_coor["portal_0_row"], portal_coor["portal_0_col"]):
                #         visited[r][c] = True
                #         r, c = portal_coor["portal_1_row"], portal_coor["portal_1_col"]
                #     elif (r, c) == (portal_coor["portal_1_row"], portal_coor["portal_1_col"]):
                #         visited[r][c] = True
                #         r, c = portal_coor["portal_0_row"], portal_coor["portal_0_col"]
                stack.append((r, c, path + [(r, c)]))
    return None


def find_plan(data):
    cave_map, portal_coor = create_map(data[1:])
    if not portal_coor:
        portal_coor = {'portal_0_row': -1, 'portal_0_col': -1, 'portal_1_row': -1, 'portal_1_col': -1}
    print(portal_coor)
    current_cell = find_start(cave_map)
    plan = ""
    res = check_cave(cave_map)
    while res:
        neighbors = get_neighbors(cave_map, current_cell)

        next_move = ""
        for key, value in neighbors.items():
            if value == " ":
                next_move = key

        if next_move == "":
            x = res[0].split(",")
            dirty_cell = {
                "row": int(x[0]),
                "col": int(x[1])
            }
            dfs_res = [(current_cell["row"], current_cell["col"])]
            dfs_res += dfs(cave_map, current_cell, dirty_cell, portal_coor)
            for i in range(len(dfs_res) - 1):
                plan += find_direction(dfs_res[i + 1], dfs_res[i], portal_coor)
            current_cell = dirty_cell
            res = check_cave(cave_map)

        else:

            plan += next_move
            cave_map, current_cell = move(cave_map, next_move, current_cell, portal_coor, "plan")
            res = check_cave(cave_map)

    return plan


raw_data = {}
for letter in 'abcde':
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
                plan = find_plan(split_data)
                print(plan)
                with open(f"my-example-solutions/solution_{letter}_{number:02d}.txt", "w+") as text_file:
                    text_file.write(plan)
