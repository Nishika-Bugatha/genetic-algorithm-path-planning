import math as ma
import numpy as np
from config import Config
from tools.draw_plot import define_links_dynamic

path_points = [[1, 7], [1, 11], [3, 14], [3, 1], [5, 8], [6, 11], [6, 4], [
    8, 4], [10, 1], [10, 7], [10, 11], [11, 14], [13, 12], [12, 2], [14, 3], [14, 8]]
npts = len(path_points)
pop_max = 1500
mutation_rate = 0.05
start_index = 0
end_index = len(path_points) - 1
generations = 1
prev_best_fitness = 0
nobs = 7
nbits = ma.log10(npts) / ma.log10(2)
chr_len = 10
stop_criteria = 0
stop_generation = False
img_iter_no = 1
plt_tolerance = -1
plt_ax_x_min = -1.0
plt_ax_x_max = 16.0
plt_ax_y_min = -1
plt_ax_y_max = 16.0
