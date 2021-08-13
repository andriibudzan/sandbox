import os
import pandas as pd
from typing import Iterable, Dict, List
from settings import *


def split_to_tables(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    df = (
        df[cols]
        .drop_duplicates()
        .reset_index()
        .drop('index', axis=1)
        .rename(mapper={x: x.lower() for x in cols}, axis=1)
    )
    return df


def add_attrs_to_table(df: pd.DataFrame, name: str) -> pd.DataFrame:
    # df[f'{name}_id'] = ((name[:3] if len(name) >= 3 else name) +
    #                     pd.Series(df.index).astype("str"))
    df[f'{name}_id'] = df.index
    df.__setattr__('name', name)
    return df


def map_and_drop_cols(mapped: pd.DataFrame,
                      mapper: pd.DataFrame,
                      tables_config: Dict) -> pd.DataFrame:

    on = tables_config.get(mapper.name)
    try:
        return mapped.merge(mapper, how='left', on=on).drop(on, axis=1)
    except KeyError:
        return mapped.merge(mapper, how='left').drop(on, axis=1)


def map_tables(table_to_map: str,
               map_with: Iterable,
               tables: Dict,
               tables_config: Dict) -> pd.DataFrame:

    df = tables.get(table_to_map)
    mappers = [tables.get(x) for x in map_with]
    orig_name = df.name
    for mapper in mappers:
        df = map_and_drop_cols(df, mapper, tables_config)
    df.__setattr__('name', orig_name)
    return df


def get_headers(sample: str) -> List:
    df = pd.read_csv(sample, sep=';', nrows=0) \
        .rename(columns=str.lower) \
        .rename(mapper=MAPPER_COLUMNS, axis=1)
    return list(df)


def makedirs(path: Iterable):
    os.makedirs(os.path.join(path), exist_ok=True)


def reader(sample: str, names: List, chunksize: int) -> pd.DataFrame:
    df = pd.read_csv(
        sample,
        sep=';',
        chunksize=chunksize,
        on_bad_lines='skip',
        dtype=MAPPER_DTYPES,
        header=0,
        names=names,
        parse_dates=['d_reg'])
    return df


if __name__ == '__main__':
    from datetime import datetime
    workdir = 'D:/Projects/sandbox/etl_pandas'
    sample = 'tz_opendata_z01012021_po01072021.csv'
    headers = get_headers(sample)
    tables = {}
    mapped_tables = {}
    chunksize = 100000
    readed = reader(sample, names=headers, chunksize=chunksize)
    processed = 0

    while True:
        try:
            df = next(readed)
            for table, cols in CONFIG_TABLES.items():
                tables[table] = add_attrs_to_table(split_to_tables(df, cols), table)

            for tb, tb_mapping in MAPPER_TABLES.items():
                mapped_tables[tb] = map_tables(tb, tb_mapping, tables, CONFIG_TABLES)

            tables.update(mapped_tables)
            for tname, tb in tables.items():
                path = f'{workdir}/mapped/{tname}'
                fname = f'{tname}_{datetime.now().strftime("%m%d_%S_%f")}.csv'
                os.makedirs(path, exist_ok=True)
                dump_name = f'{path}/{fname}'
                print(f'{tname} is DataFrame: {isinstance(tb, pd.DataFrame)}')
                print(f'path is: {path}')
                print(f'fname is: {fname}')
                print(f'dump_name is: {dump_name}')
                tb.to_csv(dump_name, index=False)
            processed += chunksize
            print(f'PROCESSED: {processed}')
        except StopIteration:
            print(f'END!')
            break
        except ValueError as e:
            print(f'---\nERROR!!!\n\t{e}---')
            continue
