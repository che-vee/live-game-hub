#pip install snowflake-connector-python 
#pip install snowflake
#pip install pymongo

# import snowflake.snowpark as snowpark
import warnings, sys, os
import pandas as pd
import numpy as np
import random
from decimal import Decimal
from datetime import datetime, timedelta
import json
# import snowflake.connector
# from snowflake.snowpark.functions import col
import pymongo
import csv
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
import django
from game_hub.mongo_models import Session, Game, GameType

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

# POSTGRESS
session_table_name = "gamingplatform.game_hub_session"
game_table_name = "gamingplatform.game_hub_game"
gametype_table_name = "gamingplatform.game_hub_gametype"

def print_postgres_tables(p_conn):
    p_cursor = p_conn.cursor()
    schema_name = 'gamingplatform'

    p_cursor.execute(f"""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = '{schema_name}'
        AND table_type = 'BASE TABLE'
        AND table_name LIKE 'game_hub_%';
    """)
    tables = p_cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print()
        print(f"- Columns for table: {table_name}")

        p_cursor.execute(f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = '{schema_name}'
            AND table_name = '{table_name}';""")
        columns = p_cursor.fetchall()

        for column in columns:
            print(column[0])

        p_cursor.execute(f"""
                SELECT COUNT(*)
                FROM {schema_name}.{table_name};
            """)

        count = p_cursor.fetchone()[0]
        print(f"- Row Count: {count}")
    
    p_cursor.close()

def get_table_sample(cur, table_name):
    select_query = f"SELECT * FROM {table_name} LIMIT 2"
    cur.execute(select_query)
    amount = cur.fetchall()
    print(amount)

    select_query = f"SELECT COUNT(*) FROM {table_name}"
    cur.execute(select_query)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()

def create_session(cur):
    table_name = session_table_name
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    print(table_name)
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            ID SERIAL PRIMARY KEY,
            StreamerID INT,
            GameID INT,
            Duration INTERVAL,
            Score INT,
            Status VARCHAR(20),
            GameMode VARCHAR(20),
            Platform VARCHAR(20),
            SessionEvents TEXT,
            SessionMetadata TEXT,
            StartTime TIMESTAMP,
            EndTime TIMESTAMP
        )
    """
    cur.execute(create_table_query)

    n = random.randint(50, 200)
    insert_query = f"""
        INSERT INTO {table_name} (
            StreamerID, GameID, Duration, Score, Status,
            GameMode, Platform, SessionEvents, SessionMetadata,
            StartTime, EndTime
        ) VALUES %s
    """
    data = []
    for _ in range(n):
        streamer_id = random.randint(1, 100)
        game_id = random.randint(1, 30)
        duration = timedelta(minutes=random.randint(1, 120))
        score = random.randint(1000, 100000)
        status = random.choice(['Active', 'Inactive', 'Deprecated', 'Canceled'])
        game_mode = random.choice(['Single Player', 'Multiplayer', 'DeathMatch', 'TeamByTeam', 'Adventure'])
        platform = random.choice(['PC', 'Console', 'Mobile', 'Switch'])
        session_events = 'Some events...'
        session_metadata = 'Some metadata...'
        start_time = datetime.now() - timedelta(minutes=random.randint(1, 360000))
        end_time = start_time + duration

        data.append((
            streamer_id, game_id, duration, score, status,
            game_mode, platform, session_events, session_metadata,
            start_time, end_time
        ))

    execute_values(cur, insert_query, data)
    get_table_sample(cur, table_name)

def create_game(cur):
    table_name = game_table_name
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    print(table_name)
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            description TEXT,
            gametype_id INT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    """
    cur.execute(create_table_query)

    n = random.randint(30, 40)
    insert_query = f"""
        INSERT INTO {table_name} (
            name, description, gametype_id, 
            created_at, updated_at
        ) VALUES %s
    """
    data = []
    for _ in range(n):
        name = "Game_" + str(random.randint(1, 1000))
        description = "Description of " + name
        gametype_id = random.randint(1, 5) 
        created_at = datetime.now()
        updated_at = datetime.now()

        data.append((
            name, description, gametype_id, 
            created_at, updated_at
        ))

    execute_values(cur, insert_query, data)
    get_table_sample(cur, table_name)

def create_gametype(cur):
    table_name = gametype_table_name
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    print(table_name)
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            genre VARCHAR(255),
            price NUMERIC(18,2),
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    """
    cur.execute(create_table_query)

    n = random.randint(5, 10)
    insert_query = f"""
        INSERT INTO {table_name} (
            genre, price,
            created_at, updated_at
        ) VALUES %s
    """
    data = []
    for _ in range(n):
        genre = random.choice(['Action', 'Adventure', 'Puzzle', 'Strategy'])
        price = Decimal(random.uniform(0.99, 59.99)).quantize(Decimal('0.01'))
        created_at = datetime.now()
        updated_at = datetime.now()

        data.append((
            genre, price,
            created_at, updated_at
        ))

    execute_values(cur, insert_query, data)
    get_table_sample(cur, table_name)

def create_all_tables(conn):
    cur = conn.cursor()
    
    create_session(cur)
    create_game(cur)
    create_gametype(cur)

    conn.commit()
    cur.close()

def postgres_task():
    p_conn = psycopg2.connect(database="postgres",
                            user="vaschetomy",
                            password="SecurePassword",
                            host="database-1.c32ikym4q9dx.ap-southeast-1.rds.amazonaws.com",
                            port="5432")

    # create_all_tables(p_conn) # recreate tables
    # print_postgres_tables(p_conn) # check tables

    mongo_task(p_conn)

# MONGO

def set_docs(p_conn):
    p_cur = p_conn.cursor()

    p_cur.execute(f"""
        SELECT s.*, g.name, g.description, gt.genre, gt.price
        FROM {session_table_name} s
        JOIN {game_table_name} g ON s.GameID = g.id
        JOIN {gametype_table_name} gt ON g.gametype_id = gt.id
    """)
    rows = p_cur.fetchall()

    # check the structure
    # column_names = [desc[0] for desc in p_cur.description] 

    Session.objects.delete()
    
    session_docs = []
    for row in rows:
        gametype = GameType(genre=row[14], price=row[15])
        game = Game(name=row[12], description=row[13], gametype=gametype)

        session_doc = Session(
            streamer_id=row[1],
            game=game,
            duration=int(row[3].total_seconds()),
            score=row[4],
            status=row[5],
            game_mode=row[6],
            platform=row[7],
            session_events=row[8],
            session_metadata=row[9],
            start_time=row[10],
            end_time=row[11]
        )
        session_docs.append(session_doc)

    if session_docs:
        Session.objects.insert(session_docs, load_bulk=False)

    p_cur.close()
    p_conn.close()
    
def get_docs():
    for session in Session.objects:
        print(session)

def mongo_task(p_conn):
    # set_docs(p_conn)  # recreate documents
    get_docs()



# SNOWFLAKE
def snowflake_task():
    snow_con = snowflake.connector.connect(user='student',password='HSUnivSFTests970',
    account='GKB48589',warehouse='COMPUTE_XS',database='SF_SAMPLE',ocsp_fail_open=False)
    snow_cursor = snow_con.cursor()

    schema = 'GAMINGPLATFORM'
    sf_stage = '@~'
    snow_curs.execute(f"USE SCHEMA SF_SAMPLE.{schema}")

    snow_cursor.execute(f"SHOW TABLES IN SCHEMA SF_SAMPLE.{schema}")

    rows = snow_cursor.fetchall()
    table_names = [row[1] for row in rows]
    print(f"List of tables in schema '{schema}':")
    for table in table_names:
        print(table)

    snow_curs.execute("""
    CREATE TABLE IF NOT EXISTS SF_SAMPLE.GAMINGPLATFORM.SESSION (
    PlayerID INT,
    GameID INT,
    StartTime DATETIME,
    EndTime DATETIME
    );
    """)

    copy_into_cmd = f"""
    COPY INTO SF_SAMPLE.GAMINGPLATFORM.SESSION
    FROM {sf_stage}/{csv_file_name}.gz
    FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);
    """

    snow_curs.execute(copy_into_cmd).fetchall()

    snow_curs.execute('select * from "SF_SAMPLE"."GAMINGPLATFORM"."SESSION"')
    f_curs = snow_curs.fetchall()
    features = {}
    for r in f_curs:
        print(r)

    snow_cursor.close()
    snow_con.close()


def main():
    postgres_task()
    #  snowflake_task()


main()
