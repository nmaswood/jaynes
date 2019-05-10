import numpy as np
from typing import List
import scipy.stats as stats


# Given a coin flip w/ 50 change of
# success, graph in your belief of P(H = 1)

def coin_trial(range_i: int):
    TRUE_PROB = 1/2

    trials = [2 ** i for i in range(range_i)]
    data = stats.bernoulli.rvs(
        TRUE_PROB,
        size=trials[-1]
    )
    # continue


# trials(")
