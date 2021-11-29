import fatpack
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(10)
# Generate a dataseries for the example
y = np.random.normal(size=100) * 10.
t = np.arange(100) / 1000
print(len(y))
print(len(t))
rev, ix = fatpack.find_reversals(y)
# Extract reversals with all rainflow ranges lower than 15 removed
rev_rtf, ix_rtf = fatpack.find_reversals_racetrack_filtered(y, h=20.)

# Below a figure is created which shows reversals of the data series with and
# without the racetrack filter
l1 = plt.plot(t, y, label='signal')
l2 = plt.plot(t[ix], rev, label='reversals')
l3 = plt.plot(t[ix_rtf], rev_rtf, label='racetrack filtered reversals')

# xlim = plt.xlim(0, 100)
leg = plt.legend(loc='best')
xlab = plt.xlabel("Indices")
ylab = plt.ylabel("Signal")
plt.grid(True)

plt.show(block=True)
