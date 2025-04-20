
from tools.population import population
from tools.fitness import fitness
from tools.ranking import ranking
from tools.dna import dna
from tools.draw_plot import show_plot, define_links_dynamic
from config import Config

def main():
    # Step 1: Generate and show obstacles
    dummy_chromosome = [i for i in range(len(Config.path_points))]
    show_plot(dummy_chromosome, draw_obstacles=True)

    # Step 2: Build links
    define_links_dynamic()

    # Step 3: Initialize population
    chr_population = population()
    chr_pop_fitness, chr_best_fitness_index = fitness(chr_pop=chr_population)
    chr_ranked_population = ranking(chr_pop_fitness=chr_pop_fitness, pop=chr_population)
    chr_crossover_mutated_population = dna(
        chr_pop_fitness=chr_pop_fitness,
        ranked_population=chr_ranked_population,
        chr_best_fitness_index=chr_best_fitness_index,
        last_pop=chr_population
    )

    # Step 4: Track best overall
    best_overall_path = chr_crossover_mutated_population[chr_best_fitness_index[0]]
    best_overall_fitness = chr_pop_fitness[chr_best_fitness_index[0], 0]

    show_plot(best_chromosome=best_overall_path, draw_obstacles=False)

    while not Config.stop_generation:
        prev_best_fit = chr_pop_fitness[chr_best_fitness_index[0], 0]

        # Step 5: Re-evaluate next generation
        chr_pop_fitness, chr_best_fitness_index = fitness(chr_pop=chr_crossover_mutated_population)
        chr_ranked_population = ranking(chr_pop_fitness=chr_pop_fitness, pop=chr_crossover_mutated_population)
        chr_crossover_mutated_population = dna(
            chr_pop_fitness=chr_pop_fitness,
            ranked_population=chr_ranked_population,
            chr_best_fitness_index=chr_best_fitness_index,
            last_pop=chr_crossover_mutated_population
        )

        # Step 6: Track best overall
        current_best_fit = chr_pop_fitness[chr_best_fitness_index[0], 0]
        if current_best_fit > best_overall_fitness:
            best_overall_fitness = current_best_fit
            best_overall_path = chr_crossover_mutated_population[chr_best_fitness_index[0]]

        # Step 7: Check stop criteria
        if prev_best_fit == current_best_fit:
            Config.stop_criteria += 1
        else:
            Config.stop_criteria = 0

        if Config.stop_criteria >= 15:
            Config.stop_generation = True

        print(f"Generation {Config.generations} | Best fitness: {current_best_fit:.4f}")
        print(f"Best current path: {chr_crossover_mutated_population[chr_best_fitness_index[0]]}")
        print()

        show_plot(best_chromosome=chr_crossover_mutated_population[0], draw_obstacles=False)
        Config.generations += 1

    # Step 8: Show final best path found
    print("✅ Best overall path found:")
    print(best_overall_path)
    show_plot(best_chromosome=best_overall_path, draw_obstacles=False)


if __name__ == '__main__':
    main()
