#!/usr/bin/env python

"""
Main script

Contains: main function

Author: Yasim Ahmad(yaaximus)

Email: yasim.ahmed63@yahoo.com
"""
from tools.population import population
from tools.fitness import fitness
from tools.ranking import ranking
from tools.dna import dna
from tools.draw_plot import show_plot, define_links_dynamic
from config import Config

def main():
    """
    This function encapsulates the cappbilty of initializing chromosome population
    and then continue calculating fitness, generate ranking, perform crossover and
    mutation & repeating above steps until a defined stopping crietia is not met.
    """

    # STEP 1: Show initial map (with obstacles)
    dummy_chromosome = [i for i in range(len(Config.path_points))]  # any valid dummy path
    show_plot(dummy_chromosome, draw_obstacles=True)

    # STEP 2: Build obstacle-aware links
    define_links_dynamic()

    chr_population = population()
    chr_pop_fitness, chr_best_fitness_index = fitness(chr_pop=chr_population)
    chr_ranked_population = ranking(chr_pop_fitness=chr_pop_fitness, pop=chr_population)
    chr_crossover_mutated_population = dna(
        chr_pop_fitness=chr_pop_fitness,
        ranked_population=chr_ranked_population,
        chr_best_fitness_index=chr_best_fitness_index,
        last_pop=chr_population
    )

    show_plot(best_chromosome=chr_crossover_mutated_population[0], draw_obstacles=False)

    while not Config.stop_generation:

        prev_best_fit = chr_pop_fitness[chr_best_fitness_index[0], 0]

        chr_pop_fitness, chr_best_fitness_index = fitness(
            chr_pop=chr_crossover_mutated_population)

        chr_ranked_population = ranking(
            chr_pop_fitness=chr_pop_fitness,
            pop=chr_crossover_mutated_population)

        chr_crossover_mutated_population = dna(
            chr_pop_fitness=chr_pop_fitness,
            ranked_population=chr_ranked_population,
            chr_best_fitness_index=chr_best_fitness_index,
            last_pop=chr_crossover_mutated_population)

        if prev_best_fit == chr_pop_fitness[chr_best_fitness_index[0], 0]:
            Config.stop_criteria += 1
        else:
            Config.stop_criteria = 0

        if Config.stop_criteria >= 5:
            Config.stop_generation = True

        print("Best chromosome is:", chr_crossover_mutated_population[chr_best_fitness_index[0]])

        show_plot(best_chromosome=chr_crossover_mutated_population[0], draw_obstacles=False)
        Config.generations += 1

    show_plot(best_chromosome=chr_crossover_mutated_population[chr_best_fitness_index[0]], draw_obstacles=False)

if __name__ == '__main__':
    main()
