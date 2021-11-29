import matplotlib.pyplot as plt
import numpy as np

# dir = 'G:\\WORK ORDERS\\2021\\21028 - PAL - Beech 200 - Loads Monitoring Program\\ENGINEERING\\00_Raw_Data\\Clean - RLM\\'
dir = '/Initial Data\\'
file_name = 'Monday September 13, 2021 12-17 PM'
# file_path = dir + 'Tuesday September 14, 2021 12-39 PM.dat'

with open(dir + file_name + '.dat', 'r') as file:
    data = np.loadtxt(file.name, dtype='float64', encoding="utf-8")

time = np.arange(0, len(data) * .004, .004) / 60

# start = int(700 / .004)
# end = int(18280 / .004)
start = 0
end = len(data) - 1

fig, ax = plt.subplots(2, 1, figsize=(13, 8.5), sharex=True)
fig.suptitle(file_name, fontsize=18)

ax[0].plot(time[start:end], data[start:end, 5], linewidth=.5, color='xkcd:dark slate blue')
# ax.set_xlabel('Time (sec)', fontsize=11)
ax[0].set_ylabel(r'$N_Z$, Vertical Acceleration @ CG $(×g)$', fontsize=11)
# ax[0].set_title(file_name, fontsize=18)
ax[0].grid(True)

ax[1].plot(time[start:end], data[start:end, 1], linewidth=.5, color='xkcd:dark slate blue')
# ax[1].plot(time[start:end], data[start:end, 3]/data[start:end, 5]*180/3.1416, linewidth=.5, color='xkcd:dark slate blue')
# ax[2].plot(time[start:end], data[start:end, 1], linewidth=.5, color='xkcd:dark slate blue')
ax[1].set_xlabel('Time (min)', fontsize=11)
ax[1].set_ylabel(r'$\dot{\theta}_y$, Pitching Rate @ CG $(\dfrac{deg}{s})$', fontsize=11)
ax[1].grid(True)
# ax[2].grid(True)

# ax.set_ylim(-14, 16)
ax[1].set_xticks(np.arange(0, 325, 25))

print(np.argmax(data[start:end, 2]))
print(np.max(data[start:end, 2]))
print(np.argmin(data[start:end, 2]))
print(np.min(data[start:end, 2]))

plt.show()
