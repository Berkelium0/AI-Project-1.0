# Repository for AI Project 1.0

**Topic:** Clean the Monster Cave

**Link to Assignment:** https://kwarc.info/teaching/AISysProj/SS24/assignment-1.0.A.pdf
## Dependencies

My code is written with Python 3.11, but it would probably work on older versions too. I have not used any external
libraries for this project.

## Repository Structure

- `example-problems` and `example-solutions` are the example data for this project. They have not been altered in any
  way and were only used for debugging purposes.
- `my-example-solutions` file is used to store the answers I generated. I compared these answers with the example
  solutions with the help of the `verify.py` script.
- `problems` file holds the problem data that needs to be solved. It has 120 problems that need to be solved, divided
  into 6 by the first 6 letters of the alphabet.
- `solutions` file has the answers I generated for the problems mentioned in the previous file.
- `main.py` script is the code I have written to read the problems, solve them, and write the answers.

## How to Run?

To run this code with other data, edit the loop at the bottom of the script. The structure of the loop is the same as
the `verify.py` script, so it should be familiar.

## The Problem

In this assignment, the task is to clean a monster cave using a vacuum cleaner robot controlled by a sequence of
instructions. The cave is represented as a grid of squares, where walls are marked with 'X', empty squares with spaces,
the starting position of the vacuum cleaner with 'S', and portals with 'P'. The instructions include moving the vacuum
cleaner north, south, east, or west. The challenge is to ensure that the entire cave is cleaned, accounting for walls
and portals that affect movement. There are six parts to this task, as shown in the table below. "Check Mode" tasks give
you a map and a plan and ask you to test the map and return if the plan is a good one or a bad one. "Find Mode" tasks
give you only a map and ask you to return a good plan.

| Problems  | Mode  | Challenges                      |
|-----------|-------|---------------------------------|
| problem a | check | —                               |
| problem b | check | portals                         |
| problem c | check | unknown start position, portals |
| problem d | find  | —                               |
| problem e | find  | portals                         |
| problem f | find  | unknown start position, portals |

I will explain my approach to each problem separately, building on the previous one.

## My Approach

### Problem a

I started by structuring the read and write aspect of the code, where it would read the problems from a to f, 0 to 19,
and write to the given file the solutions. Because the "check" and "find" modes have different input and outputs, the
code checks for the type of the mode and calls the relevant function, `check_plan` and `find_plan`, respectively. For
this problem, I started by implementing the `check_plan`.

The `check_plan` function takes the data we read from the problem file and puts the plan into a variable. Then, it sends
the map data to the `create_map` function to create a 2D array version of it. Then, it sends the newly created array to
the `find_start` function to get the coordinates of the starting cell and put it into the `current_cell` variable.
Afterward, a loop goes through the plan char by char and sends the directions to the `move` function, along with the map
and current cell data, where it moves the current cell according to the direction, if possible, and puts an "O" char in
the places where the vacuum has been.

When the loop ends, the resulting map is then sent to the `check_cave` function. If this function finds any empty cells,
it returns the missing cell coordinates. The result is then sent back. If the result is empty, "GOOD PLAN" is written as
the solution. If not, "BAD PLAN" is written with the empty cells.

### Problem b

Problem b introduces portals to the monster map. To keep track of this, I added a check to the `create_map` function
where it also returns the coordinates of the portals, if they exist.

Next, I updated the `move` function so that it checks if the current location of the vacuum is a portal and calls
the `teleport` function to teleport the vacuum to the other portal's location.

### Problem c

This problem removes the starting location and asks if the plan works regardless of it. To deal with this, I changed
the `find_start` function so that it puts every empty cell into a list and returns it, unless it finds an "S" cell.
The `check_plan` function checks if the returned starting point is a list. If so, it starts a loop of that list and acts
as the given coordinate is the starting point. Then, it goes through the plan and keeps track of all the cells that have
not been cleaned by the vacuum and returns the result.

### Problem d

This is the first problem where the plan is not given. Therefore, I needed to come up with an algorithm that finds dirty
cells and directs the vacuum in that direction. I started by calling the `check_cave` function to get a list of dirty
cells. Then, I created a while loop that will continue until there are no dirty cells left.

In this loop, I check the neighbors of the current cell with the `get_neighbors` function. Then, I check if there is an
empty cell in the neighbors. If so, I move the vacuum there and note the direction. If there are no empty cells nearby,
then I call the `dfs` function.

Before choosing the DFS search, I tried using a simpler algorithm where it would check the nearest dirty cell and try to
go there from the shortest path. However, it broke down whenever there was a wall on the path. After this failure, I
decided to go with a grid-based DFS algorithm. This function creates a stack of the neighbors and goes to the first one,
checks if it is the goal tile, if not, it puts the neighbors on top of the stack and checks the first neighbor. This
process goes on until it reaches the goal and returns the coordinates it passed through. Afterward, the `find_direction`
function goes through the coordinates and returns the path taken in directions. After there are no dirty cells left, the
loop ends, and the resulting path is returned.

### Problem e

This problem reintroduces portals to the map. To handle this, I updated the `dfs` function so that it teleports
correctly. Also, the `find_direction` function had to be updated, so it calculated the correct directions.

### Problem f

In the final problem, the starting point is once again unknown. As I have done with problem c, I created a list of empty
cells and iterated over all of them. I took the first cell and created a plan for it. Then, I set the second empty cell
as the starting point and called the `check_plan` function. If this function returned a list of empty cells, I used
the `find_plan` function to come up with a path plan so that the vacuum can go to the empty cells from its last
location, and add the new directions to the "master plan". After doing this for each starting point, the "master plan"
consisted of a path that went to every cell, regardless of its starting position.
