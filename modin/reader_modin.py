import os

import modin.pandas as pd
from timeit import default_timer as timer
from dask.distributed import Client

if __name__ == '__main__':
    from pprint import pprint as pp
    pp(os.environ.__dict__)
    client = Client(n_workers=4)
    print(client.cluster.dashboard_link)
    path = os.environ.get('DATADIR')
    filename = 'tz_opendata_z01012021_po01072021.csv'
    print(path, filename)
    file = os.path.join(path, filename)
    reading_times = []
    for i in range(5):
        start = timer()
        print('reading')
        df = pd.read_csv(file, engine='python', sep=';')
        end = timer()
        reading_times.append(end - start)

    print(f'average modin reading time: {sum(reading_times) / len(reading_times):.2f} seconds.')
