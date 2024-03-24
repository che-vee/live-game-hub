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

def synthetic_test_data_generator_GEN3(data_type, count):
    if data_type == int:
        return [random.randint(10, 5000000) for _ in range(count)]
    elif data_type == str:
        return [''.join(random.choices(string.ascii_letters + string.digits, k=8)) for _ in range(count)]
    elif data_type == datetime:
        start_date = datetime(2020, 1, 1)
        return [start_date + timedelta(days=random.randint(1, 365)) for _ in range(count)]
    elif data_type == float:
        return [random.uniform(10.0, 5000.0) for _ in range(count)]
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

def insertion_protocol(connection, schema_name, data, table_name, column_names):
    columns_sql = ', '.join(column_names)
    placeholders = ', '.join(['%s'] * len(column_names))
    insert_query = f"INSERT INTO {schema_name}.{table_name} ({columns_sql}) VALUES ({placeholders})"
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
insertion_mode = 0
start_time = datetime.now()

connection = connect()
row_count = 5
schema = "gamingplatform"
table_name = "game_hub_streamer"
include_currency = True
column_names = ["username", "email", "balance", "balance_currency", "created_at", "updated_at"]
column_constraint_types = [str, str, float, str, datetime, datetime]
clerance_to_proceed = 0
if len(column_names) == len(column_constraint_types):
    clerance_to_proceed += 1

data = []
if clerance_to_proceed == 1:
    schema_info = dict(zip(column_names, column_constraint_types))
    data = generate_data_based_on_schema(schema_info, row_count)

if dev_mode == 1:
    print("Clearance granted")


if dev_mode == 1:
    if connection:
        print("Connection active")
        print(f"Type: {type(connection)}")
    else:
        print("Connection inactive")
        print(f"Type: {type(connection)}")

if dev_mode == 1 and clerance_to_proceed == 1:
    print("Insertion data pre-insertion")
    for elements in data:
        print(elements)

if insertion_mode == 1 and clerance_to_proceed == 1:
    insertion_protocol(connection, schema, data, table_name, column_names)
    end_time = datetime.now() - start_time
    if dev_mode == 1:
        print(f"Processing time: {end_time}")
        print(f"Rows generated: {row_count}")
elif insertion_mode == 1 and clerance_to_proceed == 0:
    print("Double check you have the same length in column names and column constraints")
    end_time = datetime.now() - start_time
    if dev_mode == 1:
        print(f"Processing time: {end_time}")
        print(f"Rows generated: {row_count}")
elif insertion_mode == 0:
    print("-----")
    print("Insertion manually disabled")
    end_time = datetime.now() - start_time
    if dev_mode == 1:
        print(f"Processing time: {end_time}")
        print(f"Rows generated: {row_count}")
    print("-----")
