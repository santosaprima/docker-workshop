#!/usr/bin/env python
# coding: utf-8

import os
import json
import click
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from time import time

def get_file_iterator(file_path, chunksize, parse_dates_list=None, schema=None):
    if file_path.endswith('.csv') or file_path.endswith('.csv.gz'):
        return pd.read_csv(
            file_path, 
            iterator=True, 
            chunksize=chunksize, 
            parse_dates=parse_dates_list,
            dtype=schema,
            low_memory=False
        )
    elif file_path.endswith('.parquet'):
        parquet_file = pq.ParquetFile(file_path)
        def parquet_generator():
            for batch in parquet_file.iter_batches(batch_size=chunksize):
                yield batch.to_pandas()
        return parquet_generator()
    else:
        raise ValueError("Error: Unsupported file format. Supported formats are .csv, .csv.gz, and .parquet")

@click.command()
@click.option('--user', required=True)
@click.option('--password', required=True)
@click.option('--host', required=True)
@click.option('--port', required=True)
@click.option('--db', required=True)
@click.option('--table_name', required=True)
@click.option('--url', required=True)
@click.option('--chunksize', default=100000)
@click.option('--parse_dates', default=None, help='Comma separated date columns')
@click.option('--schema_path', default=None, help='Path to JSON file containing dtype schema') 
def ingest_data(user, password, host, port, db, table_name, url, chunksize, parse_dates, schema_path):
    dtype_schema = None
    if schema_path:
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                dtype_schema = json.load(f)
            print(f"Loaded schema from {schema_path}")
        else:
            print(f"Warning: Schema file {schema_path} not found. Using default inference.")

    parse_dates_list = parse_dates.split(',') if parse_dates else None

    file_name = 'output_data'
    if url.endswith('.csv.gz'): file_name += '.csv.gz'
    elif url.endswith('.csv'): file_name += '.csv'
    elif url.endswith('.parquet'): file_name += '.parquet'
    
    print(f"Downloading {url}...")
    os.system(f"wget {url} -O {file_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    try:
        df_iter = get_file_iterator(file_name, chunksize, parse_dates_list, dtype_schema)
        
        t_start = time()
        df = next(df_iter)
        
        df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine, if_exists='append')
        
        print(f"Inserted first chunk, took {time() - t_start:.3f}s")

        while True:
            try:
                t_start = time()
                df = next(df_iter)
                df.to_sql(name=table_name, con=engine, if_exists='append')
                print(f"Inserted chunk, took {time() - t_start:.3f}s")
            except StopIteration:
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == '__main__':
    ingest_data()
