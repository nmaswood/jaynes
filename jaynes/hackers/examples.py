import numpy as np
from typing import List
import scipy.stats as stats
from matplotlib import pyplot as plt


# Given a coin flip w/ 50 change of
# success, graph in your belief of P(H = 1)

def coin_trial(range_i: int):
    TRUE_PROB = 1/2
    DIST = stats.beta
    X = np.linspace(0, 1, 100)

    trials = [2 ** i for i in range(range_i)]
    data = stats.bernoulli.rvs(
        TRUE_PROB,
        size=trials[-1]
    )

    for k, N in enumerate(trials):
        sx = plt.subplot(
            len(trials) // 2,
            2,
            k + 1)

        plt.xlabel("$p$, prob of heads")
        plt.setp(
            sx.get_yticklabels(),
            visible=False
        )
        heads = data[:N].sum()
        y = DIST.pdf(X, 1 + heads, 1 + N - heads)
        plt.plot(X, y, label="Observe {} tosses, \n {} heads".format(N, heads))
        plt.fill_between(
            X,
            0,
            y,
            color="#348ABD",
            alpha=.4,
        )
        plt.vlines(.5, 0, 4, color="k",
                   linestyles="--",
                   lw=1)
        leg = plt.legend()
        leg.get_frame().set_alpha(.4)
        plt.autoscale(tight=True)
    plt.suptitle(
        "Bayesian updating of posterior",
        y=1.02,
        fontsize=14)
    plt.tight_layout()
    plt.show()

    # continue


coin_trial(10)
