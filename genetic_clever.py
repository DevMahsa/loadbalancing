from random import random
from numpy.core.tests.test_mem_overlap import xrange
from random import randint


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


def objective_function(vector):
    sum = 0
    for val in vector:
        sum += val ** 2
    return sum


def random_bitstring(num_bits):
    bitstring = ""
    for i in [randint(0, 1) for x in range(num_bits)]:
        bitstring += str(i)
    return bitstring

    # return map(lambda x: iif(x < 50, '1', '0'), sample(range(100), num_bits))


def decode(bitstring, search_space, bits_per_param):
    vector = []
    for i, bounds in enumerate(search_space):
        off, sum = i * bits_per_param, 0.0
        param = (bitstring[off:(off + bits_per_param)])[::-1]
        for j in xrange(0, len(param)):
            if param[j].__str__() == '1':
                sum += 1.0 * (2 ** float(j))
            else:
                sum += 0.0 * (2 ** float(j))
        min, max = bounds
        vector.append(min + ((max - min) / ((2.0 ** bits_per_param) - 1.0)) * sum)
    return vector


def fitness(candidate, search_space, param_bits):
    candidate['vector'] = decode(candidate['bitstring'], search_space, param_bits)
    candidate['fitness'] = objective_function(candidate['vector'])
    return candidate


def binary_tournament(pop):
    i, j = randint(0, len(pop) - 1), randint(0, len(pop) - 1)
    while j == i:
        j = randint(0, len(pop) - 1)
    return iif(pop[i]['fitness'] > pop[j]['fitness'], pop[i], pop[j])


def point_mutation(bitstring, rate):
    rate = 1.0 / len(bitstring)
    child = ""
    for i in xrange(0, len(bitstring)):
        bit = bitstring[i]
        child = child + iif(random() < rate, iif(bit == '1', '0', '1'), bit)
    return child


def crossover(parent1, parent2, rate):
    if random() >= rate:
        return parent1
    child = ""
    for i in xrange(0, len(parent1)):
        if random() < 0.5:
            child += parent1[i]
        else:
            child += parent2[i]
    return child


def reproduce(selected, pop_size, p_cross, p_mutation):
    children = []
    for i in xrange(0, len(selected)):
        p1 = selected[i]
        ix = iif(i % 2 == 0, i + 1, i - 1)
        if i == len(selected) - 1:
            ix = 0
        p2 = selected[ix]
        child = {}
        child['bitstring'] = crossover(p1['bitstring'], p2['bitstring'], p_cross)
        child['bitstring'] = point_mutation(child['bitstring'], p_mutation)
        children.append(child)
        if len(children) >= pop_size:
            break
    return children


def bitclimber(child, search_space, p_mut, max_local_gens, bits_per_param):
    current = child
    for _ in range(max_local_gens):
        candidate = {}
        candidate['bitstring'] = point_mutation(current['bitstring'], p_mut)
        current = fitness(candidate, search_space, bits_per_param)
        if candidate['fitness'] <= current['fitness']:
            current = candidate
    return current


def search(max_gens, search_space, pop_size, p_cross, p_mut, max_local_gens, p_local, bits_per_param=16):
    pop = []
    for i in xrange(0, pop_size):
        pop.append({'bitstring': random_bitstring(len(search_space) * bits_per_param)})
        fitness(pop[i], search_space, bits_per_param)
    pop.sort(key=lambda x: x['fitness'])
    gen, best = 0, pop[0]
    for gen in xrange(max_gens):
        selected = [binary_tournament(pop) for i in xrange(0, pop_size)]
        children = reproduce(selected, pop_size, p_cross, p_mut)
        pop = create_populations(bits_per_param, children, max_local_gens, p_mut, pop, search_space, p_local)
        pop.sort(key=lambda x: x['fitness'])
        if pop[0]['fitness'] > best['fitness']:
            best = pop[0]
        print(" > gen %d, best: fitness, best: bitstring: %s, %s" % (gen, best['fitness'], best['bitstring']))

    return best


def create_populations(bits_per_param, children, max_local_gens, p_mut, pop, search_space, p_local):
    for child in children:
        if random() < p_local:
            pop.append(bitclimber(child, search_space, p_mut, max_local_gens,
                                  bits_per_param))
    return pop


def main():
    # problem configuration
    problem_size = 3
    search_space = [[-5, +5] for y in range(problem_size)]
    # algorithm configuration
    max_gens = 100
    pop_size = 100
    p_cross = 0.98
    p_mut = 1.0 / (3 * 16)
    max_local_gens = 20
    p_local = 0.5
    # execute the algorithm
    best = search(max_gens, search_space, pop_size, p_cross, p_mut, max_local_gens, p_local)
    print(
        "done! Solution: f=%s,s=%s,v=%s " % (best['fitness'], str(best['bitstring']), str(best['vector'])))


if __name__ == "__main__":
    main()
