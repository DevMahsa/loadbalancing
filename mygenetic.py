from random import randint, random
from numpy.core.tests.test_mem_overlap import xrange
from operator import add
from pandas.compat import reduce


def individual(length, min, max):
    'Create a member of the population.'
    return [randint(min, max) for x in xrange(length)]


# print(individual(5,0,100))
# print(individual(5,0,100))

def population(count, length, min, max):
    """
    Create a number of individuals (i.e. a population).
    :param count: the number of individuals in the population
    :param length: the number of values per individual
    :param min: the min possible value in an individual's list of values
    :param max: the max possible value in an individual's list of values
    :return:
    """
    return [individual(length, min, max) for x in xrange(count)]


# print(population(5,5,0,100))


def fitness(individual, target):
    """
     Determine the fitness of an individual. Lower is better.

    :param individual:  the individual to evaluate
    :param target: the sum of numbers that individuals are aiming for
    :return:
    """
    sum = reduce(add, individual, 0)
    return abs(target - sum)


# x = individual(5,0,100)
# print(fitness(x, 200))


def grade(pop, target):
    """
    'Find average fitness for a population.'

    :param pop:
    :param target:
    :return:
    """
    summed = reduce(add, (fitness(x, target) for x in pop), 0)
    return summed / (len(pop) * 1.0)


# x = population(3, 5, 0, 100)
# target = 200
# print(grade(x, target))


def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
    """

    :param pop:
    :param target:
    :param retain:
    :param random_select:
    :param mutate:
    :return:
    """
    graded = [(fitness(x, target), x) for x in pop]
    graded = [x[1] for x in sorted(graded)]
    retain_length = int(len(graded) * retain)
    parents = graded[:retain_length]

    # randomly add other individuals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual) - 1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = int(len(male)/2)
            child = male[:half] + female[half:]
            children.append(child)

    parents.extend(children)
    return parents

def main():

    target = 371
    p_count = 100
    i_length = 5
    i_min = 0
    i_max = 100
    p = population(p_count, i_length, i_min, i_max)
    fitness_history = [grade(p, target),]
    for i in xrange(100):
        p = evolve(p, target)
        fitness_history.append(grade(p, target))
        for datum in fitness_history:
            print(datum)

if __name__ == "__main__":
    main()
