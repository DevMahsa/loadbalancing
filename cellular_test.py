from cellpylib.cellpylib import *

cellular_automaton = init_random(149)

# Mitchell et al. discovered this rule using a Genetic Algorithm
rule_number = 6667021275756174439087127638698866559

# evolve the CA, setting r to 3, for a neighbourhood size of 7
cellular_automaton = evolve(cellular_automaton, timesteps=149,
                                apply_rule=lambda n, c, t: binary_rule(n, rule_number), r=3)

plot(cellular_automaton)