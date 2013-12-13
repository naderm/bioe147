#!/usr/bin/env python

from __future__ import division

import sys
import numpy as np
from itertools import product, permutations
from math import pow

def _gen_avg(generator):
    total, length, minv, maxv = 0, 0, None, None
    for i in generator:
        total += i
        length += 1
    return total / length

def _shRNA_prod(lacI, parameters):
    lacI_k_I_1 = 700
    tetR_k_I = 7000
    xylR_k_I = 7000

    tetR_prod_1, \
      tetR_prod_2, \
      xylR_prod, \
      = parameters

    lacI_k_I_2 = lacI_k_I_1 * 15

    vals = np.array([
        lacI_k_I_1, tetR_k_I, xylR_k_I, tetR_prod_1, tetR_prod_2,
        xylR_prod, lacI_k_I_2, lacI
        ])

    tetR_n = 2
    lacI_n = 2
    xylR_n = 5

    def _sh_from_ratios(ratios):
        avals = vals * np.array(ratios)
        tetR_1 = avals[3] * (1 / (1 + pow(avals[7] / avals[0], lacI_n)) + 0.01)
        xylR =   avals[5]   * (1 / (1 + pow(avals[7] / avals[6], lacI_n)) + 0.01)
        tetR_2 = avals[4] * (1 / (1 + pow(xylR / avals[2], xylR_n))   + 0.01)
        tetR = tetR_1 + tetR_2
        sh_prod = 1 / (1 + pow(tetR / avals[1], tetR_n))
        return sh_prod

    sh_prod = _gen_avg(_sh_from_ratios(i) for i in product([0.95, 1, 1.05], repeat = 8))
    # for ratios in

    return sh_prod, 0, 0, 0
    # return sh_prod, tetR_1, xylR, tetR_2

def _gen_parameters():

    # for lacI in xrange(800, 7200, 200):
    #     yield [lacI, 14000, 14000, 14000]
    yield [7000, 14000, 14000, 14000]
    # from itertools import permutations
    # for lacI in xrange(800, 7500, 200):
    #     for rest in permutations(
    #         [i * pow(10, 2) for i in xrange(1, 20, 1)] +
    #         [i * pow(10, 3) for i in xrange(2, 15, 1)] +
    #         [], 3):
    #         yield [lacI] + list(rest)

def _score_shs(sh_prods):
    return (min(sh_prods[2:5]) / max(sh_prods[0:2] + sh_prods[5:])) if sh_prods[3] > 0.8 else 0

NOISE = 200

def _lac_range(med):
    return map(int, [0, NOISE,
                     med - NOISE, med, med + NOISE,
                     med * 2 - NOISE, med * 2])

def _print_data(lac_range, parameters):
    for i in xrange(min(lac_range), max(lac_range) + 1, (max(lac_range) - min(lac_range)) // 20):
        print "lacI: {:6} =>".format(i),
        for name, conc in zip(["shRNA", "TetR 1", "xylR", "tetR 2"], _shRNA_prod(i, parameters)):
            print "{}: {:7.1f},    ".format(name, conc),
        print

def _print_edge_cases():
    with open("output.csv", "w") as f:
        for lacI in xrange(0, 14001, 700):

            lacI_k_I_1 = 700
            tetR_k_I = 7000
            xylR_k_I = 7000

            tetR_prod_1 = 14000
            tetR_prod_2 = 14000
            xylR_prod   = 14000

            lacI_k_I_2 = lacI_k_I_1 * 15

            tetR_n = 2
            lacI_n = 2
            xylR_n = 5

            from itertools import product
            import numpy as np

            vals = np.array([
                lacI_k_I_1, tetR_k_I, xylR_k_I, tetR_prod_1, tetR_prod_2,
                xylR_prod, lacI_k_I_2, lacI
                ])

            for ratios in product([0.975, 1, 1.025], repeat = 8):
                ratios = np.array(ratios)
                avals = vals * ratios

                tetR_1 = avals[3] * (1 / (1 + pow(avals[7] / avals[0], lacI_n)) + 0.01)
                xylR =   avals[5]   * (1 / (1 + pow(avals[7] / avals[6], lacI_n)) + 0.01)
                tetR_2 = avals[4] * (1 / (1 + pow(xylR / avals[2], xylR_n))   + 0.01)
                tetR = tetR_1 + tetR_2
                sh_prod = 1 / (1 + pow(tetR / avals[1], tetR_n))
                print >> f, "{}, {:.3f}".format(lacI, sh_prod)

def _main(args):
    med = 1500
    best = max(_gen_parameters(),
               key = lambda x: _score_shs([_shRNA_prod(lacI, x[1:])[0]
                                           for lacI in _lac_range(x[0])]))
    med = best[0]
    lac_range = _lac_range(med)
    best = best[1:]
    print "lac_range:", lac_range
    print "best parameters:", best
    print "score:", _score_shs([_shRNA_prod(i, best)[0] for i in lac_range])
    print

    _print_data(lac_range, best)
    _print_edge_cases()

if __name__ == "__main__":
    _main(sys.argv[1:])
