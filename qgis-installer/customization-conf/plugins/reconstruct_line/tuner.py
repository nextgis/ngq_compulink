# -*- coding: utf-8 -*-

import numpy as np


class Tuner():
    def __init__(self, data):
        self.data = data

    @property
    def size(self):
        return len(self.data)

    def penalty(self, order):
        '''Return sum of distances between units
        '''
        x1 = np.take(self.data, order)
        x2 = np.roll(x1, 1)
        d = np.sum(abs(x1 - x2)[1:])  # (x1 - x2)[0] is the distance between the first and the last points
        return d

    def roll_to_max_distance(self, order):
        # Roll the order that,
        # so the first and the last points are the most distance
        x1 = np.take(self.data, order)
        x2 = np.roll(x1, 1)
        d = abs(x1 - x2)
        idx = np.argmax(d)
        return np.roll(order, -idx)


    def permute(self, index, order):
        tests = np.empty((self.size, self.size), dtype=np.int)
        num = order[index]
        base = np.delete(order, index)

        for i in range(self.size):
            tests[i, :] = np.insert(base, i, num)

        return tests

    def local_opt(self, init_order):
        '''Reorder some points to find local optimum
        '''
        best_penalty = self.penalty(init_order)
        best_order = init_order

        final = False
        while not final:
            final = True
            for idx in range(self.size):
                for order in self.permute(idx, best_order):
                    if self.penalty(order) < best_penalty:
                        best_order = order
                        best_penalty = self.penalty(order)
                        final = False
                        break

        return (best_penalty, best_order)

    def reorder(self, init_order):

        # List of candidates (good start points) for optimize.
        # Candidate 1: eliminate the biggest distance from the point list
        cand1 = self.roll_to_max_distance(init_order)
        if np.all(cand1 == init_order):
            candidates = [init_order]
        else:
            candidates = [init_order, cand1]

        # TODO: This line can ne done in 2 threads
        penalties = [self.local_opt(order) for order in candidates]

        if len(penalties) == 1:
            return penalties[0][1]

        if penalties[0][0] < penalties[1][0]:
            return penalties[0][1]
        else:
            return penalties[1][1]
