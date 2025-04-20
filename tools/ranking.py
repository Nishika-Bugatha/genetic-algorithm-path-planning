import numpy as np
import random
from config import Config

def ranking(chr_pop_fitness, pop):
    """
    Tournament selection-based ranking.
    """

    def tournament(k=3):
        selected = random.sample(range(Config.pop_max), k)
        best = selected[0]
        for idx in selected:
            if chr_pop_fitness[idx][0] > chr_pop_fitness[best][0]:
                best = idx
        return best

    new_pop = np.zeros_like(pop)
    for i in range(Config.pop_max):
        winner = tournament()
        new_pop[i] = pop[winner]

    return new_pop
