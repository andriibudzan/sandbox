import os

import pandas as pd
from timeit import default_timer as timer


if __name__=='__main__':
    filename = 'tz_opendata_z01012021_po01072021.csv'
    path = os.environ.get('DATADIR')
    file = os.path.join(path, filename)


    reading_times = []
    for i in range(5):
        start = timer()
        print('reading')
        df = pd.read_csv(file, engine='python', sep=';')
        end = timer()
        reading_times.append(end - start)

    print(f'average Pandas reading time: {sum(reading_times) / len(reading_times):.2f} seconds.')
