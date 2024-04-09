# %%
import numpy as np
import pandas as pd
import scipy.stats as sps
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.optimize import minimize


# %%
def intensity(baseline, alpha, beta, timesteps, t):
    if len(timesteps) == 1:
        return baseline
    ti = timesteps[timesteps < t]
    result = baseline
    for i in range(len(ti)):
        result += mu(alpha, beta, t - ti[i])
    return result


def mu(alpha, beta, t):
    return np.sum(alpha * np.exp(-beta * t))


def take_timestep(baseline, alpha, beta, timesteps):
    lmbda = intensity(baseline, alpha, beta, timesteps[:-1], timesteps[-1])
    t = np.random.exponential(1 / lmbda)
    updated_timesteps = np.append(timesteps, t)
    return updated_timesteps


def log_likelihood(params, timesteps):
    n = len(params) // 2
    baseline = params[0]
    alpha = params[1 : n + 1]
    beta = params[n + 1 :]
    lmbda_t = np.zeros(len(timesteps))
    for i in range(len(timesteps)):
        lmbda_t[i] = intensity(baseline, alpha, beta, timesteps, timesteps[i])
    integral = np.sum(lmbda_t[1:] * np.diff(timesteps))
    return np.sum(np.log(lmbda_t)) - integral


def fit(initial_params, timesteps):
    res = minimize(log_likelihood, initial_params, args=timesteps, method="Nelder-Mead")
    return res.x


# %%
sp500 = (
    yf.download("^GSPC", start="2021-01-01", end="2023-08-31")["Close"]
    .pct_change()
    .dropna()
)
sp500 = sp500.reset_index()

rolling_vol = sp500["Close"].rolling(window=20).std().dropna().values
events = []
events_val = []
for i in range(1, len(rolling_vol)):
    if rolling_vol[i] > 0.015:
        events.append(i)
        events_val.append(rolling_vol[i])

# plt.plot(rolling_vol)
# plt.scatter(events, events_val, color="red")
# plt.show()

# %%
T = len(rolling_vol)
t = np.linspace(0, T, 1000)
initial_params = np.array([0.1, 0.001, 0.1])
params = fit(initial_params, np.array(events))
baseline = params[0]
alpha = params[1]
beta = params[2]
intensity_values = [
    intensity(baseline, alpha, beta, np.array(events), time) for time in t
]
plt.plot(t, intensity_values)
plt.show()
# %%
