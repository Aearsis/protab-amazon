#!/usr/bin/env python3

"""
Math based on this article:
    http://www.turingfinance.com/random-walks-down-wall-street-stochastic-processes-in-python/

TODO: Implement the following.

Before starting the game, set the inception variable to roughly an hour before
the game starts. The generated charts will start at that time.
"""

import math

import datetime
import numpy
import random
import scipy.linalg
import numpy.random as nrand
import matplotlib.pyplot as plt
import matplotlib.dates as dates

class ModelParameters:
    def __init__(self, s0, time):
        # This is the amount of minutes
        self.all_time = time
        # Number of values per minute
        self.all_delta = 1/60
        # This is the volatility of the stochastic processes
        self.all_sigma = 0.2
        # This is the correlation between the wiener processes of the Heston model
        self.cir_rho = 0.1
        # This is the rate of mean reversion for volatility in the Heston model
        self.heston_a = 0.9
        # This is the long run average volatility for the Heston model
        self.heston_mu = 0.05
        # This is the starting volatility value for the Heston model
        self.heston_vol0 = 0.1
        # This is the starting asset value
        self.all_s0 = 10


def convert_to_prices(param, log_returns):
    """
    This method converts a sequence of log returns into normal returns (exponentiation) and then computes a price
    sequence given a starting price, param.s0.
    :param param: the model parameters object
    :param log_returns: the log returns to exponentiated
    :return:
    """
    returns = numpy.exp(log_returns)
    # A sequence of prices starting with param.s0
    price_sequence = [param.s0]
    for i in range(1, len(returns)):
        # Add the price at t-1 * return at t
        price_sequence.append(price_sequence[i - 1] * returns[i - 1])
    return numpy.array(price_sequence)

def cox_ingersoll_ross_heston(param):
    """
    This method returns the rate levels of a mean-reverting cox ingersoll ross process. It is used to model interest
    rates as well as stochastic volatility in the Heston model. Because the returns between the underlying and the
    stochastic volatility should be correlated we pass a correlated Brownian motion process into the method from which
    the interest rate levels are constructed. The other correlated process is used in the Heston model
    :param param: the model parameters objects
    :return: the interest rate levels for the CIR process
    """
    # We don't multiply by sigma here because we do that in heston
    sqrt_delta_sigma = math.sqrt(param.all_delta) * param.all_sigma
    brownian_motion_volatility = nrand.normal(loc=0, scale=sqrt_delta_sigma, size=param.all_time)
    a, mu, zero = param.heston_a, param.heston_mu, param.heston_vol0
    volatilities = [zero]
    for i in range(1, param.all_time):
        drift = a * (mu - volatilities[i-1]) * param.all_delta
        randomness = math.sqrt(abs(volatilities[i - 1])) * brownian_motion_volatility[i - 1]
        volatilities.append(volatilities[i - 1] + drift + randomness)
    return numpy.array(brownian_motion_volatility), numpy.array(volatilities)


def heston_levels(param):
    """
    The Heston model is the geometric brownian motion model with stochastic volatility. This stochastic volatility is
    given by the cox ingersoll ross process. Step one on this method is to construct two correlated GBM processes. One
    is used for the underlying asset prices and the other is used for the stochastic volatility levels
    :param param: model parameters object
    :return: the prices for an underlying following a Heston process
    """
    assert isinstance(param, ModelParameters)
    # Get two correlated brownian motion sequences for the volatility parameter and the underlying asset
    # brownian_motion_market, brownian_motion_vol = get_correlated_paths_simple(param)
    brownian, cir_process = cox_ingersoll_ross_heston(param)
    brownian, brownian_motion_market = heston_construct_correlated_path(param, brownian)

    heston_market_price_levels = [param.all_s0]
    for i in range(1, param.all_time):
        #drift = param.gbm_mu * heston_market_price_levels[i - 1] * param.all_delta
        drift = 0
        vol = cir_process[i - 1] * heston_market_price_levels[i - 1] * brownian_motion_market[i - 1]
        heston_market_price_levels.append(heston_market_price_levels[i - 1] + drift + vol)
    return numpy.array(heston_market_price_levels)


def heston_construct_correlated_path(param, brownian_motion_one):
    """
    This method is a simplified version of the Cholesky decomposition method for just two assets. It does not make use
    of matrix algebra and is therefore quite easy to implement.
    :param param: model parameters object
    :return: a correlated brownian motion path
    """
    # We do not multiply by sigma here, we do that in the Heston model
    sqrt_delta = math.sqrt(param.all_delta)
    # Construct a path correlated to the first path
    brownian_motion_two = []
    for i in range(param.all_time - 1):
        term_one = param.cir_rho * brownian_motion_one[i]
        term_two = math.sqrt(1 - math.pow(param.cir_rho, 2.0)) * random.normalvariate(0, sqrt_delta)
        brownian_motion_two.append(term_one + term_two)
    return numpy.array(brownian_motion_one), numpy.array(brownian_motion_two)


def get_correlated_geometric_brownian_motions(param, correlation_matrix, n):
    """
    This method can construct a basket of correlated asset paths using the Cholesky decomposition method
    :param param: model parameters object
    :param correlation_matrix: nxn correlation matrix
    :param n: the number of assets i.e. the number of paths to return
    :return: n correlated log return geometric brownian motion processes
    """
    assert isinstance(param, ModelParameters)
    decomposition = scipy.linalg.cholesky(correlation_matrix, lower=False)
    uncorrelated_paths = []
    sqrt_delta_sigma = math.sqrt(param.all_delta) * param.all_sigma
    # Construct uncorrelated paths to convert into correlated paths
    for i in range(param.all_time):
        uncorrelated_random_numbers = []
        for j in range(n):
            uncorrelated_random_numbers.append(random.normalvariate(0, sqrt_delta_sigma))
        uncorrelated_paths.append(numpy.array(uncorrelated_random_numbers))
    uncorrelated_matrix = numpy.matrix(uncorrelated_paths)
    correlated_matrix = uncorrelated_matrix * decomposition
    assert isinstance(correlated_matrix, numpy.matrix)
    # The rest of this method just extracts paths from the matrix
    extracted_paths = []
    for i in range(1, n + 1):
        extracted_paths.append([])
    for j in range(0, len(correlated_matrix)*n - n, n):
        for i in range(n):
            extracted_paths[i].append(correlated_matrix.item(j + i))
    return extracted_paths

# The time data will be generated for - an hour before game, an hour after
inception = datetime.datetime.today().replace(hour=13)
destruction = datetime.datetime.today().replace(hour=19)
eternity_sec = int((destruction - inception).total_seconds())

# The time in which data will be normalized
game_start = datetime.datetime.today().replace(hour=14, minute=30)
game_end = datetime.datetime.today().replace(hour=17, minute=30)
game_length = game_end - game_start

now = datetime.datetime.today().replace(hour=17, minute=30)

game_sec = int(game_length.total_seconds())
window_sec = game_sec // 3

second = datetime.timedelta(seconds=1)

def gen_stock(i):
    # Generate random levels using Heston model
    random.seed(420 + i)
    nrand.seed(420 + i)
    params = ModelParameters(1, eternity_sec)
    levels = heston_levels(params)

    # Normalize all stock to the same yield over gametime
    start_off = int((game_start - inception).total_seconds())
    coef = game_sec * 10 / numpy.sum(levels[start_off:start_off + game_sec])
    return levels * coef

stock = [gen_stock(i) for i in range(5)]

plt.style.use(['bmh'])
fig, ax = plt.subplots(1)
fig.suptitle("Vývoj cen", fontsize=16)
ax.set_xlabel('Čas')
ax.set_xlim(now - window_sec * second, now)
ax.set_ylabel('Cena')
ax.set_ylim(0, 25)

x_axis = dates.drange(inception, inception + len(stock[0]) * second, second)

for i in range(len(stock)):
    plt.plot_date(x_axis, stock[i], "-", linewidth=0.3)

plt.show()

