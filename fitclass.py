import numpy as np
from scipy import optimize


class Parameter:

    def __init__(self, value):
        self.value = value

    def set(self, value):
        self.value = value

    def __call__(self):
        return self.value


def fit(function, parameters, y, x=None):
    def f(params):
        i = 0
        for p in parameters:
            p.set(params[i])
            i += 1
        return y - function(x)

    if x is None:
        x = np.arange(y.shape[0])
    p = [param() for param in parameters]
    return optimize.leastsq(f, p)
