import os

from timeit import default_timer as timer
from dask import dataframe as ddf
from dask.distributed import Client

if __name__ == '__main__':
    client = Client(n_workers=4)
    print(client.cluster.dashboard_link)
    filename = 'tz_opendata_z01012021_po01072021.csv'
    path = os.environ.get('DATADIR')
    file = os.path.join(path, filename)
    dtype = {
        'CAPACITY': 'float64',
        'OWN_WEIGHT': 'object',
        'TOTAL_WEIGHT': 'object'
    }
    reading_times = []
    for i in range(5):
        start = timer()
        print('reading')
        df = (
              ddf
              .read_csv(file, engine='python', sep=';', dtype=dtype)
              .compute()
              )
        end = timer()
        reading_times.append(end - start)

    print(f'average dask reading time: {sum(reading_times) / len(reading_times):.2f} seconds.')
