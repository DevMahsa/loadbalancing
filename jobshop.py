from genetic_toolkit import Population, Chromosome, BiologicalProcessManager, JobManager
import random

# Population Initialization
population = Population(100)
population.initialize_population()

# Rates
crossover_rate = 0.70

# Main Algorithm
generation_counter = 0
while (generation_counter != 200):
    current_population_fitnesses = [chromosome.fitness for chromosome in population.population]
    print("CURRENT GEN FITNESS: {} ".format(current_population_fitnesses))
    new_gen = []
    while (len(new_gen) <= population.population_size):
        # Create tournament for tournament selection process
        tournament = [population.population[random.randint(1, population.population_size - 1)] for individual in
                      range(1, population.population_size)]

        # Obtain two parents from the process of tournament selection
        parent_one, parent_two = population.select_parents(tournament)

        # Create the offspring from those two parents
        child_one, child_two = BiologicalProcessManager.pmx(crossover_rate, parent_one, parent_two)

        # Our algorithm produces only one child or returns back to parents
        # Here we check if only one child was returned or not
        if child_two == 0:

            # Mutate the child
            BiologicalProcessManager.mutate(child_one)

            # Evaluate the child
            child_one.generate_fitness()

            # Add the child to the new generation of chromosomes
            new_gen.append(child_one)

        else:
            # Since the crossover returned back two parents, we'll just put them back into the pop
            new_gen.append(child_one)
            new_gen.append(child_two)

# Replace old generation with the new one
    population.population = new_gen
    generation_counter += 1
