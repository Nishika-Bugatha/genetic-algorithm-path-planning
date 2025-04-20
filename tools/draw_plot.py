
# Generates dynamic obstacles, checks line-obstacle intersections, and updates valid links accordingly.

from config import Config
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from shapely.geometry import LineString, box

# Store obstacle rectangles and fixed points globally
obstacle_rects = []
fixed_start = None
fixed_goal = None


def show_plot(best_chromosome, inf_time=False, draw_obstacles=False):
    plt.figure(num=1)
    plt.clf()
    plt.axis([Config.plt_ax_x_min, Config.plt_ax_x_max, Config.plt_ax_y_min,
              Config.plt_ax_y_max])

    _draw_path_points()
    if draw_obstacles:
        _draw_obstacles()
    else:
        # Redraw previously generated obstacles
        for x, y, w, h in obstacle_data:
            rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='black', facecolor='red')
            plt.gca().add_patch(rect)

    # draw path
    best_path_x = []
    best_path_y = []

    for element in best_chromosome:
        best_path_x.append(Config.path_points[int(element)][0])
        best_path_y.append(Config.path_points[int(element)][1])

    plt.plot(best_path_x, best_path_y, "g-")

    # Use fixed start and goal for annotation
    if fixed_start:
        plt.annotate('Start', xy=(fixed_start[0] + 0.2, fixed_start[1] + 0.2), color='green', fontsize=9)
    if fixed_goal:
        plt.annotate('Goal', xy=(fixed_goal[0] + 0.2, fixed_goal[1] + 0.2), color='red', fontsize=9)

    plt.draw()
    plt.savefig(f"./docs/images/{Config.img_iter_no}.png")
    Config.img_iter_no += 1

    if not inf_time:
        plt.pause(0.01)
    else:
        plt.show()


def _draw_path_points():
    node_x = []
    node_y = []

    for element in Config.path_points:
        node_x.append(element[0])
        node_y.append(element[1])

    plt.plot(node_x, node_y, "ko")


def _draw_obstacles():
    global obstacle_rects, obstacle_data, fixed_start, fixed_goal
    obstacle_rects = []
    obstacle_data = []

    map_width = 16
    map_height = 16
    num_obstacles = 6
    obstacle_size_range = (1, 3)
    fixed_start = (Config.path_points[0][0], Config.path_points[0][1])
    fixed_goal = (Config.path_points[-1][0], Config.path_points[-1][1])

    for _ in range(num_obstacles):
        while True:
            width = random.randint(*obstacle_size_range)
            height = random.randint(*obstacle_size_range)
            x = random.randint(0, map_width - width)
            y = random.randint(0, map_height - height)

            if (abs(x - fixed_start[0]) < 2 and abs(y - fixed_start[1]) < 2) or \
               (abs(x - fixed_goal[0]) < 2 and abs(y - fixed_goal[1]) < 2):
                continue

            obstacle_data.append((x, y, width, height))
            break



def line_intersects_obstacles(p1, p2, obstacles):
    line = LineString([p1, p2])
    for x, y, w, h in obstacle_data:
        box_obj = box(x, y, x + w, y + h)
        if line.intersects(box_obj):
            return True
    return False



def define_links_dynamic():
    Config.links = []
    num_points = len(Config.path_points)
    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                p1 = Config.path_points[i]
                p2 = Config.path_points[j]
                if not line_intersects_obstacles(p1, p2, obstacle_data):
                    Config.links.append([i, j])
    return Config.links
