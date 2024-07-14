import random
import pygame as py
import sys

color_of_initial_and_target = "blue"
color_of_grid_background = "black"
color_of_screen_background = "black"
color_of_block_border = (20, 20, 20)
color_of_fs = "pink"
color_of_path = "yellow"
color_of_obstacles = "red"
block_size = 15

screen_size = (1350, 650)
grid_size = (1300, 600)
grid_shift = ((screen_size[0] - grid_size[0]) // 2, screen_size[1] - grid_size[1] - 20)
display = py.display.set_mode((screen_size[0], screen_size[1]))
display.fill(color_of_screen_background)


class Grid:

    def __init__(self):
        self.number_of_obstacles = 200
        self.grid_dimensions = (grid_size[0] // block_size, grid_size[1] // block_size)
        self.grid = self.generate_grid()

    def generate_grid(self):
        no_obstacles_grid = [[1000 for _ in range(self.grid_dimensions[1])] for _ in range(self.grid_dimensions[0])]
        for _ in range(self.number_of_obstacles):
            rand_x = random.randint(0, self.grid_dimensions[0] - 1)
            rand_y = random.randint(0, self.grid_dimensions[1] - 1)
            no_obstacles_grid[rand_x][rand_y] = -1
        py.display.update()
        return no_obstacles_grid

    def draw_grid(self):
        for x in range(0, self.grid_dimensions[0]):
            for y in range(0, self.grid_dimensions[1]):
                rect = py.Rect(x * block_size + grid_shift[0], y * block_size + grid_shift[1], block_size, block_size)
                if self.grid[x][y] == -1:
                    py.draw.rect(display, color_of_obstacles, rect)
                else:
                    py.draw.rect(display, color_of_grid_background, rect)
                    py.draw.rect(display, color_of_block_border, rect, 1)
        py.display.update()


def initialize_beginning():
    position_initialized = False
    while not position_initialized:
        for event in py.event.get():
            if event.type == py.MOUSEBUTTONDOWN:
                mouse_location = py.mouse.get_pos()
                print("Mouse" + str(mouse_location))
                user_initial_position = [0, 0]
                user_initial_position[0] = (mouse_location[0] - mouse_location[0] % block_size - grid_shift[
                    0]) // block_size
                user_initial_position[1] = (mouse_location[1] - mouse_location[1] % block_size - grid_shift[
                    1]) // block_size
                print("Initial_position" + str(user_initial_position))
                initial_position = tuple(user_initial_position)
                return initial_position


def optimal_movements(initial_pos, target_pos):
    directions = {"down": (1, 0), "left": (0, -1), "up": (-1, 0), "right": (0, 1)}
    difference_tuple = tuple(map(lambda i, t: i - t, initial_pos, target_pos))
    movement = ["right", "down", "left", "up"]
    if difference_tuple[0] > 0:
        if difference_tuple[1] > 0:
            # movement = ["down", "right", "up", "left"]
            movement = ["right", "down", "left", "up"]
        elif difference_tuple[1] < 0:
            movement = ["down", "left", "up", "right"]
        else:
            print(1)
            movement = ["down", "right", "up", "left"]
    elif difference_tuple[0] < 0:
        if difference_tuple[1] > 0:
            movement = ["right", "up", "left", "down"]
        elif difference_tuple[1] < 0:
            movement = ["up", "left", "down", "right"]
        else:
            movement = ["left", "up", "right", "down"]
    else:
        if difference_tuple[1] > 0:
            movement = ["down", "right", "up", "left"]
        elif difference_tuple[1] < 0:
            movement = ["up", "left", "down", "right"]
    return list(map(lambda direction: directions[direction], movement))


def fs_grid(breadth, grid, initial_position, target_position, array_dimensions):
    visited = []
    queue = []
    path_list = [[initial_position]]
    steps = 0
    current_position = initial_position
    queue.append(current_position)
    visited.append(current_position)
    while queue:
        path = path_list.pop()
        pos = path[-1]
        if pos == target_position:
            return path, True
        if breadth:
            cur = queue.pop(0)
        else:
            cur = queue.pop()
        possible_movements = optimal_movements(cur, target_position)
        for movement in possible_movements:
            new_position = (cur[0] + movement[0], cur[1] + movement[1])
            if 0 <= new_position[0] <= array_dimensions[0] - 1 and 0 <= new_position[1] <= array_dimensions[
                1] - 1 and new_position not in visited and grid[new_position[0]][new_position[1]] != -1:
                grid[new_position[0]][new_position[1]] = steps
                queue.append(new_position)
                visited.append(new_position)
                steps += 1
                new_path = list(path)
                new_path.append(new_position)
                path_list.append(new_path)
                if new_position == target_position:
                    return new_path, True
                draw_rect_at_current_position(new_position, color_of_fs)
    return [], False


def check_events():
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()


def draw_rect_at_current_position(current_position, color):
    rect = py.Rect(current_position[0] * block_size + grid_shift[0], current_position[1] * block_size + grid_shift[1],
                   block_size, block_size)
    py.draw.rect(display, color, rect)
    py.draw.rect(display, color_of_block_border, rect, 1)
    py.display.update()
    check_events()


def draw_path(path):
    for position in path:
        draw_rect_at_current_position(position, color_of_path)


py.init()
display.fill(color_of_screen_background)
start = False
grid_object = Grid()
grid_object.draw_grid()
initial_position = initialize_beginning()

grid_object.grid[initial_position[0]][initial_position[1]] = 1000
print(initial_position)
draw_rect_at_current_position(initial_position, color_of_initial_and_target)
target_position = initialize_beginning()
draw_rect_at_current_position(target_position, color_of_initial_and_target)
grid_object.grid[target_position[0]][target_position[1]] = 1000
(path, found) = fs_grid(False, grid_object.grid, initial_position, target_position, grid_object.grid_dimensions)
if found:
    draw_path(path)
else:
    print("Not found")
while True:
    for event in py.event.get():
        if event.type == py.KEYDOWN and event.key == py.K_r:
            display.fill(color_of_screen_background)
            start = False
            grid_object = Grid()
            grid_object.draw_grid()
            initial_position = initialize_beginning()
            grid_object.grid[initial_position[0]][initial_position[1]] = 1000
            draw_rect_at_current_position(initial_position, "blue")
            target_position = initialize_beginning()
            grid_object.grid[target_position[0]][target_position[1]] = 1000
            draw_rect_at_current_position(target_position, "blue")
            print((initial_position, target_position))
            (path, found) = fs_grid(False, grid_object.grid, initial_position, target_position,
                                    grid_object.grid_dimensions)
            if found:
                draw_path(path)
            else:
                print("Not found")
    check_events()
