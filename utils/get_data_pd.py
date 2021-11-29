import pandas as pd
import numpy as np
from datetime import datetime

col = ['date', 'time', 'Ax', 'Ay', 'Az', 'Rx', 'Ry', 'Rz', 'something',
       'channel']


def get_data(file_path: str) -> np.ndarray:
    """Reads data using pandas.

    Parameters
    ----------
    file_path : str
        The path of the ``dat`` file.

    Returns
    -------
    array
        The read data.

    """
    with open(file_path, 'r') as f:
        df = pd.read_csv(f, sep=r'\s+', header=None, engine='python',
                         names=col)

    df['date_time'] = [x + ' ' + y for x, y in zip(df['date'], df['time'])]
    arr = np.column_stack([df['date_time'], df['Az'], df['Rx']])
    del df

    t0 = datetime.strptime(arr[0, 0][:-1], '%d/%m/%Y %H:%M:%S.%f')

    arr[:, 0] = [(datetime.strptime(
        x[:-1], '%d/%m/%Y %H:%M:%S.%f') - t0).total_seconds()
                 for x in arr[:, 0]]

    # gc.collect()
    return arr
