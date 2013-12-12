#!/usr/bin/env python

from __future__ import division

import sys
from math import pow

def _shRNA_prod(lacI, parameters):
    lacI_k_I_1 = 700
    tetR_k_I = 7000
    cI_k_I = 7000

    tetR_prod_1, \
      tetR_prod_2, \
      cI_prod = parameters

    lacI_k_I_2 = lacI_k_I_1 * 15

    tetR_n = 2
    lacI_n = 2
    cI_n = 2

    tetR_1 = tetR_prod_1 * (1 / (1 + pow(lacI / lacI_k_I_1, lacI_n)) + 0.001)
    cI = cI_prod * (1 / (1 + pow(lacI / lacI_k_I_2, lacI_n)) + 0.001)
    tetR_2 = tetR_prod_2 * (1 / (1 + pow(cI / cI_k_I, cI_n)) + 0.001)
    tetR = tetR_1 + tetR_2
    sh_prod = 1 / (1 + pow(tetR / tetR_k_I, tetR_n))

    return sh_prod, tetR_1, cI, tetR_2

def _gen_parameters():
    from itertools import permutations
    return permutations(
        [i * pow(10, 2) for i in xrange(1, 10)] +
        [i * pow(10, 3) for i in xrange(1, 15)] +
        [], 4)

def _score_shs(sh_prods):
    return (min(sh_prods[2:5]) / max(sh_prods[0:2] + sh_prods[5:])) if sh_prods[3] > 0.8 else 0

NOISE = 100

def _lac_range(med):
    return map(int, [0, NOISE,
                     med - NOISE, med, med + NOISE,
                     med * 2 - NOISE, med * 2])

def _print_data(lac_range, parameters):
    for i in xrange(min(lac_range), max(lac_range) + 1, (max(lac_range) - min(lac_range)) // 20):
        print i, zip(_shRNA_prod(i, parameters), ["shRNA", "TetR 1", "cI", "tetR 2"])

def _main(args):
    med = 1500
    best = max(_gen_parameters(),
               key = lambda x: _score_shs([_shRNA_prod(lacI, x[1:])[0]
                                           for lacI in _lac_range(x[0])]))
    med = best[0]
    lac_range = _lac_range(med)
    best = best[1:]
    print "lac_range:", lac_range
    print "best parameters:", zip(["tetR1 v_max:", "tetR2 v_max:", "cI v_max:"], map(int, best))
    print "score:", _score_shs([_shRNA_prod(i, best)[0] for i in lac_range])
    print

    _print_data(lac_range, best)

if __name__ == "__main__":
    _main(sys.argv[1:])
