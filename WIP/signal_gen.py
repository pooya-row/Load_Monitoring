import numpy as np


def produce_signal(time_range: float,
                   time_steps: float,
                   signal_mean: float = 1.,
                   rnd_seed: int = 0,
                   to_csv=False):
    """Generates a random signal for the period of `time_range`, discretized by `time-step`.

    Arguments
    ---------
    time_range: float
        total period of time sampling is performed
    time_steps: float
        length of time increments used for sampling
    signal_mean: float
        mean value of the signal (default = 1.0)
    rnd_seed: int
        random seed (default = 0)
    to_csv: bool
        whether to write the signal into `signal.csv` file

    Returns
    -------
    time, signal: ndarray, ndarray
        "time" (discretized time) and "signal" (corresponding signal values) lists or arrays

    Example
    -------
    Below an example is shown:

    >>> from WIP import signal_gen
    >>> t, s = signal_gen.produce_signal(0.1, .01, 1., 42)
    t = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    s = array([1.49671415, 0.8617357 , 1.64768854, 2.52302986, 0.76584663,
               0.76586304, 2.57921282, 1.76743473, 0.53052561, 1.54256004,
               0.53658231])

    Generates a serialized signal

    """

    np.random.seed(rnd_seed)

    time = list(np.arange(0, (time_range + time_steps), time_steps))
    signal = signal_mean + np.random.randn(len(time))

    if to_csv:
        np.savetxt('signal.csv', np.column_stack((time, signal)), delimiter=',', fmt='%.8f')


    # time = range(1, 17)
    # signal = [2, -14, 10, 0, 13, -9, 11, -8, 8, -9, 15, -4, 10, 0, 13, 0]

    # time = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6,
    #         0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.]
    # signal = [1, 2.4, 2.1, 2.9, 2.3, 2.45, 2.2, 2.1, 1.9, 3.0, 2.9, 3, 1.6, 1.7,
    #           0.0, 0.9, 0.1, 0.5, 0.7, 0.8, 1.1]

    # time = np.array([0.848920863, 1.294964029, 2.014388489, 3.223021583, 4.172661871, 4.73381295, 6.0,
    #                  7.366906475, 8.158273381])
    # signal = np.array([-2.034990792, 0.837937385, -2.863720074, 4.926335175, -1.05893186, 2.826887661,
    #                    -3.839779006, 3.839779006, -2.145488029])
    # signal = [-2., 1., -3., 5., -1., 3., -4., 4., -2.]
    return time, signal

# signal = [0.6 * sin(t) + 0.2 * cos(10 * t) + 0.2 * sin(20 * t) for t in time]


# np.random.seed(0)
# time = [2.0 * i / 10 for i in range(100 + 1)]
# signal = 1 + np.random.randn(len(time))
