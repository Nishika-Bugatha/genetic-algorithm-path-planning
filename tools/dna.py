
from config import Config
import numpy as np
import random

def dna(chr_pop_fitness, ranked_population, chr_best_fitness_index, last_pop):
    chromo_crossover_pop = _do_crossover(
        ranked_pop=ranked_population,
        chr_best_fit_indx=chr_best_fitness_index,
        pop=last_pop
    )
    chromo_crossover_mutated_pop = _do_mutation(pop=chromo_crossover_pop)
    return chromo_crossover_mutated_pop


def _do_mutation(pop):
    mutated_pop = np.array(pop, copy=True)

    # build valid link dictionary
    valid_links = {i: [] for i in range(Config.npts)}
    for a, b in Config.links:
        valid_links[a].append(b)

    itr = 3
    while itr < Config.pop_max:
        # 🔁 Occasionally rebuild path from scratch
        if random.random() < 0.02:
            current = Config.start_index
            path = [current]

            while len(path) < Config.chr_len:
                nexts = valid_links.get(current, [])
                if not nexts:
                    break
                next_node = random.choice(nexts)
                path.append(next_node)
                current = next_node
                if current == Config.end_index:
                    break

            while len(path) < Config.chr_len:
                path.append(Config.end_index)

            mutated_pop[itr, :] = path

        else:
            # Normal point mutation
            for k in range(1, Config.chr_len - 1):
                if random.random() < 0.05:  # ⬅️ Mutation rate boosted
                    prev_node = int(mutated_pop[itr, k - 1])
                    next_options = valid_links.get(prev_node, [])
                    if next_options:
                        mutated_pop[itr, k] = random.choice(next_options)

        itr += 1

    return mutated_pop


def _do_crossover(ranked_pop, chr_best_fit_indx, pop):
    crossover_pop = np.zeros((Config.pop_max, Config.chr_len))

    # Elitism: carry over top 3
    crossover_pop[0, :] = pop[chr_best_fit_indx[0], :]
    crossover_pop[1, :] = pop[chr_best_fit_indx[1], :]
    crossover_pop[2, :] = pop[chr_best_fit_indx[2], :]

    # 💡 Use only top 10% of population as breeding pool
    elite_cutoff = max(4, int(Config.pop_max * 0.1))
    ranked_elites = ranked_pop[:elite_cutoff]

    valid_links = {i: [] for i in range(Config.npts)}
    for a, b in Config.links:
        valid_links[a].append(b)

    itr = 3
    while itr < Config.pop_max:
        current = Config.start_index
        path = [current]

        while len(path) < Config.chr_len:
            nexts = valid_links.get(current, [])
            if not nexts:
                break
            current = random.choice(nexts)
            path.append(current)
            if current == Config.end_index:
                break

        while len(path) < Config.chr_len:
            path.append(Config.end_index)

        crossover_pop[itr, :] = path
        itr += 1

    return crossover_pop
