
from config import Config
import numpy as np
import math as ma
import random
from tools.draw_plot import define_links_dynamic

def population():
    define_links_dynamic()
    link = Config.links

    link_fit = _link_distance(link)
    link_prob = _link_prob(link_fit)
    link_cum_prob = np.cumsum(link_prob, axis=1)
    initial_pop = _create_pop(link_cum_prob=link_cum_prob)

    return initial_pop

def _link_distance(link):
    link_dist = []
    for pair in link:
        i, j = pair
        pt1 = Config.path_points[i]
        pt2 = Config.path_points[j]
        dist = calculate_distance(pt1, pt2)
        link_dist.append([dist])
    return np.array(link_dist)

def _link_prob(link_fit):
    link_prob = np.zeros((np.shape(link_fit)[0], np.shape(link_fit)[1]))
    for i in range(np.shape(link_fit)[0]):
        for j in range(np.shape(link_fit)[1]):
            link_prob[i][j] = link_fit[i][j] / np.sum(link_fit[i], keepdims=True)
    return link_prob

def _create_pop(link_cum_prob):
    pop = np.zeros((Config.pop_max, Config.chr_len))
    pop[:, 0] = Config.start_index
    pop[:, Config.chr_len - 1] = Config.end_index

    valid_links = {i: [] for i in range(Config.npts)}
    for i, j in Config.links:
        valid_links[i].append(j)

    for k in range(Config.pop_max):
        current = Config.start_index
        path = [current]

        while len(path) < Config.chr_len - 1:
            neighbors = valid_links.get(current, [])
            if not neighbors:
                break
            next_node = random.choice(neighbors)
            path.append(next_node)
            current = next_node
            if current == Config.end_index:
                break

        while len(path) < Config.chr_len:
            path.append(Config.end_index)

        pop[k] = path[:Config.chr_len]

    return pop

def calculate_distance(pt_1, pt_2):
    return ma.sqrt(ma.pow((pt_1[0] - pt_2[0]), 2) + ma.pow((pt_1[1] - pt_2[1]), 2))
