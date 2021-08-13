import os
from pprint import pprint as pp

filename = 'tz_opendata_z01012021_po01072021.csv'
path = os.environ.get('DATADIR')
file = os.path.join(path, filename)
files = {}
for file in os.listdir(path):
    files[file] = os.path.getsize(os.path.join(path, file)) / 1e6
    # d = {
    #   "name": file,
    #   "size": os.path.getsize(os.path.join(path, file))
    # }

pp(files)
