import os
from datetime import datetime
from os import DirEntry
from pprint import pprint as pp

path = '../'


def scaner(p, external_storage, ignored):
    stor = external_storage
    with os.scandir(p) as items:
        for item in items:
            if item.is_dir() and not item.name.startswith('.') and item.name not in ignored:
                try:
                    scaner(item.path, stor, ignored)
                except PermissionError as e:
                    print(f'Permission denied: {item.path}')
                    continue
            if item.is_file():
                stor.append(get_file_stat(item))
            else:
                continue


def convert_timestamp(ts):
    return datetime.fromtimestamp(int(ts)).strftime('%d-%m-%Y %H:%M')


def convert_bytes(b):
    for power in [(1e9, 'Gb'), (1e6, 'Mb'), (1e3, 'Kb')]:
        if (b / power[0]) < 1:
            continue
        else:
            return f'{b / power[0]:.2f} {power[1]}'


def get_file_stat(file: DirEntry):
    statinfo = os.stat(file)
    d = {
        "path": os.path.normcase(file.path),
        "name": file.name,
        "permissions": statinfo.st_mode,
        "index": statinfo.st_ino,
        "hard_links": statinfo.st_nlink,
        "owner_userid": statinfo.st_uid,
        "owner_groupid": statinfo.st_gid,
        "size": convert_bytes(statinfo.st_size),
        "size_in_bytes": statinfo.st_size,
        "last_access_time": convert_timestamp(statinfo.st_atime),
        "last_modification_time": convert_timestamp(statinfo.st_mtime),
        "creation_time": convert_timestamp(statinfo.st_ctime),
        "last_access_time_ts": statinfo.st_atime,
        "last_modification_time_ts": statinfo.st_mtime,
        "creation_time_ts": statinfo.st_ctime

    }
    return d


if __name__ == '__main__':
    import os
    import json
    from pprint import pprint as pp
    ignored = ['AppData', 'venvs', 'Projects', 'Google Drive']
    # p = os.getcwd()
    # p = os.environ.get('HOME')
    p = "D:\\"
    save_as = p.replace('\\', '_').replace(':', '')
    storage = []
    res = scaner(p, storage, ignored)
    # pp(storage)
    print(len(storage))
    with open(f"scan_{save_as}.json", 'w') as f:
        json.dump(storage, f, indent=2)

    size = [x.get('size_in_bytes') for x in storage]
    largest = [convert_bytes(x) for x in sorted(size, reverse=True)[:10]]
    pp(largest)
