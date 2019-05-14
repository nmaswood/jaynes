import scipy.stats as stats

import pymc3 as pm


def a_b():
    p_true = 5 / 100
    N = 1500
    occurrences = stats.bernoulli.rvs(p_true, size=N)

    with pm.Model() as model:
        p = pm.Uniform('p', lower=0, upper=1)
        obs = pm.Bernoulli("obs", p, observed=occurrences)
        # To be explained in chapter 3
        step = pm.Metropolis()
        trace = pm.sample(18000, step=step)
        burned_trace = trace[1000:]
    breakpoint()


a_b()
