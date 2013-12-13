#!/usr/bin/env python

from __future__ import division

import sys
import numpy as np
import random

M = None

def _rand_flip(lst):
    hix_1 = random.randint(0, M)
    hix_2 = random.randint(0, M)

    if hix_1 > hix_2:
        hix_1, hix_2 = hix_2, hix_1

    return _flip(lst, hix_1, hix_2)

def _flip(lst, left, right):
    output = []

    for index in xrange(M):
        if index >= left and index < right:
            output.append(-lst[right - (index - left + 1)])
        else:
            output.append(lst[index])

    return output

def _randomize(lst):
    random.shuffle(lst)
    for index, val in enumerate(lst):
        lst[index] = random.choice([-1, 1]) * val
    return lst

def _main(args):
    if len(args) < 1:
        print "Usage: python {} edge_count".format(__file__)
        sys.exit(1)

    global M
    M = int(args[0])
    particle_count = 10 ** 7

    start = range(1, M + 1)
    correct = range(1, M + 1)
    random.shuffle(start)

    for index, val in enumerate(start):
        start[index] = val * random.choice([-1, 1])

    # print start
    # particles = np.array([_randomize(range(M)) for i in xrange(particle_count)])
    particles = np.array([start for i in xrange(particle_count)])

    iterations = 100
    for i in xrange(iterations):
        print "Iteration {:3} ...".format(i),

        count = 0

        for index in xrange(particle_count):
            particles[index] = _rand_flip(particles[index])
            if all(i == j for i, j in zip(particles[index], correct)):
                count += 1

        print "Correct:", count / particle_count

if __name__ == "__main__":
    _main(sys.argv[1:])
