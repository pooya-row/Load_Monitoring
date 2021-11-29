from numba import jit
import numpy as np
import math


@jit
def hypot(x, y):
    x = abs(x)
    y = abs(y)
    t = min(x, y)
    x = max(x, y)
    t = t / x
    return x * math.sqrt(1 + t * t)


@jit()
def ex1(x, y):
    out = []
    for i in range(x.shape[0]):
        out.append(math.sqrt(x[i] ** 2 + y[i] ** 2))
    return out


in1 = np.arange(10e6, dtype=np.float64)
in2 = 2 * in1 + 1
# out = np.empty_like(in1)

print('in1:', in1)
print('in2:', in2)

out1 = ex1(in1, in2)

# print('out:', out1)

# np.testing.assert_almost_equal(out1, np.hypot(in1, in2))
