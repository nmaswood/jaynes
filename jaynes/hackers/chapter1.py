import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt

# Given a coin flip w/ 50 change of
# success, graph in your belief of P(H = 1)
# as you observe more data

COLOURS = ["#348ABD", "#A60628"]


def coin_trial(range_i: int):
    TRUE_PROB = 1 / 2
    DIST = stats.beta
    X = np.linspace(0, 1, 100)

    trials = [2**i for i in range(range_i)]
    data = stats.bernoulli.rvs(TRUE_PROB, size=trials[-1])

    for k, N in enumerate(trials):
        sx = plt.subplot(len(trials) // 2, 2, k + 1)

        plt.xlabel("$p$, prob of heads")
        plt.setp(sx.get_yticklabels(), visible=False)
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
        plt.vlines(.5, 0, 4, color="k", linestyles="--", lw=1)
        leg = plt.legend()
        leg.get_frame().set_alpha(.4)
        plt.autoscale(tight=True)
    plt.suptitle("Bayesian updating of posterior", y=1.02, fontsize=14)
    plt.tight_layout()
    plt.show()

    # continue


# posterior probability of code has bugs giving ci has passed


def code_bug_free():
    p = np.linspace(0, 1, 50)
    plt.plot(p, 2 * p / (1 + p), color="#348ABD", lw=3)
    plt.fill_between(p, 2 * p / (1 + p), alpha=.5, facecolor=["#A60628"])
    plt.scatter(0.2, 2 * (0.2) / 1.2, s=140, c="#348ABD")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel("Prior, $P(A) = p$")
    plt.ylabel("Posterior, $P(A|X)$, with $P(A) = p$")
    plt.title("Is my code bug-free?")
    plt.show()


def prior_and_posterior():

    colours = ["#348ABD", "#A60628"]

    prior = [0.20, 0.80]
    posterior = [1. / 3, 2. / 3]
    plt.bar([0, .7],
            prior,
            alpha=0.70,
            width=0.25,
            color=colours[0],
            label="prior distribution",
            lw="3",
            edgecolor=colours[0])

    plt.bar([0 + 0.25, .7 + 0.25],
            posterior,
            alpha=0.7,
            width=0.25,
            color=colours[1],
            label="posterior distribution",
            lw="3",
            edgecolor=colours[1])

    plt.ylim(0, 1)
    plt.xticks([0.20, .95], ["Bugs Absent", "Bugs Present"])
    plt.title("Prior and Posterior probability of bugs present")
    plt.ylabel("Probability")
    plt.legend(loc="upper left")
    plt.show()


# prior_and_posterior()


def poison_example():
    a = np.arange(16)
    poi = stats.poisson
    lambda_ = [1.5, 4.25]
    colours = ["#348ABD", "#A60628"]

    plt.bar(a,
            poi.pmf(a, lambda_[0]),
            color=colours[0],
            label="$\lambda = %.1f$" % lambda_[0],
            alpha=0.60,
            edgecolor=colours[0],
            lw="3")

    plt.bar(a,
            poi.pmf(a, lambda_[1]),
            color=colours[1],
            label="$\lambda = %.1f$" % lambda_[1],
            alpha=0.60,
            edgecolor=colours[1],
            lw="3")

    plt.xticks(a + 0.4, a)
    plt.legend()
    plt.ylabel("probability of $k$")
    plt.xlabel("$k$")
    plt.title(
        "Probability mass function of a Poisson random variable; differing \
    $\lambda$ values")
    plt.show()


# poison_example()


def exponential_distributions():
    a = np.linspace(0, 4, 100)
    expo = stats.expon
    lambda_ = [0.5, 1]

    for l, c in zip(lambda_, COLOURS):
        plt.plot(a,
                 expo.pdf(a, scale=1. / l),
                 lw=3,
                 color=c,
                 label="$\lambda = %.1f$" % l)
        plt.fill_between(a, expo.pdf(a, scale=1. / l), color=c, alpha=.33)

    plt.legend()
    plt.ylabel("PDF at $z$")
    plt.xlabel("$z$")
    plt.ylim(0, 1.2)
    plt.title("Probability density function of an Exponential random variable;\
     differing $\lambda$")
    plt.show()


exponential_distributions()
