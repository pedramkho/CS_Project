from numpy import np


def poisson(lam=1.0):
    s = np.random.poisson(lam)
    return s


def exponential(mean=1.0):
    s = np.random.exponential(mean)
    return int(s)


def uniform():
    s = np.random.uniform()
    if s < 0.5:
        return 0
    elif 0.5 <= s < 0.7:
        return 1
    elif 0.7 <= s < 0.85:
        return 2
    elif 0.85 <= s < 0.95:
        return 3
    else:
        return 4
