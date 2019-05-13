import os

import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt

import pymc3 as pm

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


def texting(graph_init=False):
    path = os.path.join('/Users/nasr/code/jaynes/resources/hackers',
                        'txtdata.csv')
    count_data = np.loadtxt(path)
    n_count_data = len(count_data)

    if graph_init:
        plt.bar(np.arange(n_count_data), count_data, color="#348ABD")
        plt.xlabel("Time (days)")
        plt.ylabel("count of text-msgs received")
        plt.title("Did the user's texting habits change over time?")
        plt.xlim(0, n_count_data)
        plt.show()

    with pm.Model() as model:
        alpha = 1 / count_data.mean()
        lambda_1 = pm.Exponential("lambda_1", alpha)
        lambda_2 = pm.Exponential("lambda_2", alpha)

        tau = pm.DiscreteUniform("tau", lower=0, upper=n_count_data - 1)

    with model:
        idx = np.arange(n_count_data)  # Index
        lambda_ = pm.math.switch(tau > idx, lambda_1, lambda_2)
        observation = pm.Poisson("obs", lambda_, observed=count_data)
        step = pm.Metropolis()
        trace = pm.sample(10000, tune=5000, step=step)
    ax = plt.subplot(311)
    ax.set_autoscaley_on(False)

    lambda_1_samples = trace['lambda_1']
    lambda_2_samples = trace['lambda_2']
    tau_samples = trace['tau']

    plt.hist(lambda_1_samples,
             histtype='stepfilled',
             bins=30,
             alpha=0.85,
             label="posterior of $\lambda_1$",
             color="#A60628",
             normed=True)
    plt.legend(loc="upper left")
    plt.title(r"""Posterior distributions of the variables
        $\lambda_1,\;\lambda_2,\;\tau$""")
    plt.xlim([15, 30])
    plt.xlabel("$\lambda_1$ value")

    ax = plt.subplot(312)
    ax.set_autoscaley_on(False)
    plt.hist(lambda_2_samples,
             histtype='stepfilled',
             bins=30,
             alpha=0.85,
             label="posterior of $\lambda_2$",
             color="#7A68A6",
             normed=True)
    plt.legend(loc="upper left")
    plt.xlim([15, 30])
    plt.xlabel("$\lambda_2$ value")

    plt.subplot(313)
    w = 1.0 / tau_samples.shape[0] * np.ones_like(tau_samples)
    plt.hist(tau_samples,
             bins=n_count_data,
             alpha=1,
             label=r"posterior of $\tau$",
             color="#467821",
             weights=w,
             rwidth=2.)
    plt.xticks(np.arange(n_count_data))

    plt.legend(loc="upper left")
    plt.ylim([0, .75])
    plt.xlim([35, len(count_data) - 20])
    plt.xlabel(r"$\tau$ (in days)")
    plt.ylabel("probability")


texting()
