import string

import numpy as np
import psycopg2, random, timeit
from timeit import default_timer as timer
from datetime import timedelta, datetime
import threading
import random
import psycopg2
import psycopg2.extensions
import time
from Black_wall_EX102 import black_wall_protocol_EX102

def synthetic_test_data_generator_GEN3(data_type, count):
    results = []
    string_limit = 3

    if data_type == int:
        for _ in range(count):
            results.append(round(random.randint(1, 575000), 2))
    elif data_type == str and string_limit is not None:
        generated = set()
        while len(generated) < count:
            potential_string = ''.join(random.choices(string.ascii_letters + string.digits, k=string_limit))
            if potential_string not in generated:
                generated.add(potential_string)
                results.append(potential_string)
            if len(generated) == 62 ** string_limit:  # Max unique combinations
                break
        results = list(generated)
    elif data_type == datetime:
        start_date = datetime(2020, 1, 1)
        for _ in range(count):
            results.append(start_date + timedelta(days=random.randint(1, 365)))
    elif data_type == float:
        for _ in range(count):
            results.append(round(random.uniform(10.0, 5000.0), 2))
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

    return results

def insertion_protocol(connection, schema_name, data, table_name, column_names):
    columns_sql = ', '.join(column_names)
    placeholders = ', '.join(['%s'] * len(column_names))
    insert_query = f"INSERT INTO {schema_name}.{table_name} ({columns_sql}) VALUES ({placeholders})"
    # Black wall applying anomaly handling
    black_wall_protocol_EX102(connection, input=None, mutation="Anomaly handler", dates=None, column_names=column_names, table_name=table_name,
                                                schema=schema_name,type_accpeted=None)
    with connection.cursor() as cur:
        cur.executemany(insert_query, data)
        connection.commit()

def generate_data_based_on_schema(schema_info, count):
    data = []
    for data_type in schema_info.values():
        column_data = synthetic_test_data_generator_GEN3(data_type, count)
        data.append(column_data)
    return list(map(list, zip(*data)))

def connect():
    conn = psycopg2.connect(database="postgres",
                            user="vaschetomy",
                            password="SecurePassword",
                            host="database-1.c32ikym4q9dx.ap-southeast-1.rds.amazonaws.com",
                            port="5432")
    return conn

# Behavior modifiers
dev_mode = 1
if dev_mode == 1:
    print("---")
    print("Dev mode active")
    print("---")
    print()
insertion_mode = 1
if insertion_mode == 1:
    print("---")
    print("Insertion mode active")
    print("---")
    print()
start_time = datetime.now()

connection = connect()
row_count = 2
schema = "gamingplatform"
table_name = "game_hub_streamer"
include_currency = True
column_names = ["username", "email", "balance", "balance_currency", "created_at", "updated_at"]
column_constraint_types = [str, str, float, str, datetime, datetime]
clerance_to_proceed = 0
if len(column_names) == len(column_constraint_types):
    clerance_to_proceed += 1
    if dev_mode == 1:
        print("Column names:")
        print(column_names)
        print("Column type constraints:")
        print(column_constraint_types)

data = []
if clerance_to_proceed == 1:
    schema_info = dict(zip(column_names, column_constraint_types))
    data = generate_data_based_on_schema(schema_info, row_count)
    if dev_mode == 1:
        print()
        print("Clearance granted")
elif clerance_to_proceed == 0:
    quit("Clearance denied. Length of column names and column type constraints not equal.")

if dev_mode == 1:
    if connection:
        print()
        print("Connection active")
        print(f"Connection type: {type(connection)}")
        print()
    else:
        print("Connection inactive")

if dev_mode == 1 and clerance_to_proceed == 1:
    print("Insertion data pre-insertion")
    for elements in data:
        print(elements)

if insertion_mode == 1 and clerance_to_proceed == 1:
    insertion_protocol(connection, schema, data, table_name, column_names)
    end_time = datetime.now() - start_time
    print(f"Processing time: {end_time}")
    print(f"Rows generated: {row_count}")
    print(f"Rows generated per second: {round(row_count / end_time.total_seconds(), 1)}")
    print(f"Rows generated per microsecond: {round(row_count / end_time.microseconds, 1)}")
elif insertion_mode == 1 and clerance_to_proceed == 0:
    print("Double check you have the same length in column names and column constraints")
    end_time = datetime.now() - start_time
    print(f"Processing time: {end_time}")
elif insertion_mode == 0:
    print("-----")
    print("Insertion protocols manually disabled")
    end_time = datetime.now() - start_time
    print(f"Processing time: {end_time}")
    print(f"Rows generated: {row_count}")
    print(f"Rows generated per second: {round(row_count/end_time.total_seconds(), 1)}")
    print(f"Rows generated per microsecond: {round(row_count/end_time.microseconds,1)}")
    print("-----")
