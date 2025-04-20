
from config import Config
from tools.population import calculate_distance
from tools.draw_plot import define_links_dynamic
import numpy as np

def fitness(chr_pop):
    chromo_pts_consec_dist = chr_pts_consecutive_dist(pop=chr_pop)
    chromo_fit_based_dist = chr_fit_based_dist(chr_pts_consec_dist=chromo_pts_consec_dist)
    chromo_conn = chr_conn(chr_pop=chr_pop)
    chromo_fit_based_conn = chr_fit_based_conn(chr_conn=chromo_conn)
    chromo_fit = chr_fit(chr_fit_based_dist=chromo_fit_based_dist, chr_fit_based_conn=chromo_fit_based_conn)

    for i in range(Config.pop_max):
        path = chr_pop[i]
        if int(path[0]) != Config.start_index or int(path[-1]) != Config.end_index:
            chromo_fit[i][0] = 1e-6
        elif chromo_conn[i][0] < Config.chr_len - 2:
            chromo_fit[i][0] *= chromo_conn[i][0] / (Config.chr_len - 2)

    # Small reward boost if path reaches goal early
    for i in range(Config.pop_max):
        if int(chr_pop[i][-1]) == Config.end_index:
            chromo_fit[i][0] *= 1.1

    chromo_best_fit_index = chr_best_fit_ind(chr_fit=chromo_fit)
    return chromo_fit, chromo_best_fit_index

def chr_best_fit_ind(chr_fit):
    temp_chr_fit = np.array(chr_fit, copy=True)
    chr_best_fit_index = []
    while len(chr_best_fit_index) < 3:
        y = np.where(temp_chr_fit == np.amax(temp_chr_fit))[0]
        for i in range(len(y)):
            chr_best_fit_index.append(int(y[i]))
        for i in chr_best_fit_index:
            temp_chr_fit[i][0] = 0
    return chr_best_fit_index

def chr_fit(chr_fit_based_dist, chr_fit_based_conn):
    chr_fit = np.zeros((Config.pop_max, 1))
    for i in range(Config.pop_max):
        chr_fit[i][0] = chr_fit_based_dist[i][0]  # ignore conn, just reward distance
    return chr_fit


def chr_fit_based_conn(chr_conn):
    chr_conn_fit = np.zeros((Config.pop_max, 1))
    for i in range(Config.pop_max):
        chr_conn_fit[i][0] = chr_conn[i][0] / (Config.chr_len - 1)
    return chr_conn_fit

def chr_conn(chr_pop):
    define_links_dynamic()
    link_set = set((a, b) for a, b in Config.links)
    chr_conn = np.zeros((Config.pop_max, 1))

    for i in range(Config.pop_max):
        path = chr_pop[i]
        truncated_path = []
        seen = set()

        for node in path:
            node = int(node)
            if node in seen:
                chr_conn[i][0] = -1  # penalize loop here
                break
            seen.add(node)
            truncated_path.append(node)
            if node == Config.end_index:
                break

        if chr_conn[i][0] == -1:
            continue  # skip if penalized due to loop

        for j in range(len(truncated_path) - 1):
            a = truncated_path[j]
            b = truncated_path[j + 1]
            if (a, b) in link_set:
                chr_conn[i][0] += 1

    return chr_conn


def chr_fit_based_dist(chr_pts_consec_dist):
    chr_pop_fit_based_dist = np.zeros((Config.pop_max, 1))
    for i in range(Config.pop_max):
        total_distance = np.sum(chr_pts_consec_dist[i])
        chr_pop_fit_based_dist[i][0] = 1000.0 / (total_distance + 1e-6)
    return chr_pop_fit_based_dist

def chr_pts_consecutive_dist(pop):
    chr_pop_dist = np.zeros((Config.pop_max, Config.chr_len - 1))
    for i in range(Config.pop_max):
        path = pop[i]
        truncated_path = []
        for node in path:
            truncated_path.append(int(node))
            if int(node) == Config.end_index:
                break
        for j in range(len(truncated_path) - 1):
            chr_pop_dist[i][j] = calculate_distance(
                pt_1=Config.path_points[truncated_path[j + 1]],
                pt_2=Config.path_points[truncated_path[j]])
    return chr_pop_dist
