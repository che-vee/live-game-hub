import math
import numpy as np
from sqlalchemy.dialects.postgresql import psycopg2
import psycopg2.extensions
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy.testing.exclusions import closed

def black_wall_protocols(connection, input, mutation, dates, column_names, table_name, schema, type_accpeted):
    def execute_query(connection_params, query):
        assert(type(query) == str)
        conn = None
        try:
            conn = psycopg2.connect(**connection_params).cursor()
            conn.execute(query)
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            if conn is not closed:
                conn.close()

    def ice_wall(input, type_accepted):
        assert(type(input) == list or type(input) == np.ndarray)
        accpeted_types = [bool, str, int, float]
        assert(type_accepted in accpeted_types)
        # Filter
        filtered_list = [item for item in input if isinstance(item, type_accepted) and not (isinstance(item, float) and math.isnan(item))]
        # Failsafe
        failsafe = []
        for x in filtered_list:
            if type(x) == type_accepted:
                failsafe.append(x)

        filtered_list = np.array(failsafe)
        return filtered_list

    assert(type(mutation) == str)
    assert(type(table_name) == str)
    assert(type(schema) == str)

    compatible_mutations = ["Modular clearance", "S-Sync", "Anomaly handler",
                            "ML preprocessing", "DB-sync"]
    if mutation not in compatible_mutations:
        return "Mutation protocol does not exist"

    #synchronizer if compatible ------------------
    if mutation == "Sync" and len(input) > 0 and dates > 0:
        assert(type(input) == list or type(input) == np.ndarray)
        dormant_status = 1
        if type(input) != np.ndarray:
            input = np.array(input)

        if dormant_status == 1:
            return 0, 0
        # Add synchronizing script here

        if dormant_status == 0:
            synced_dates = []
            synced_data = []
            return synced_data, synced_dates
    # DB-sync ---------------
    elif mutation == "DB-sync" and table_name != None and column_names != None and schema != None:
        dormant_state_DB_sync = 0
        if dormant_state_DB_sync == 1:
            return 0
        # Restructure to make it sort alphabetically
        connection = connection.cursor()
        sort_direction = "ASC"
        column_scanner = f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = '{schema}'
        AND table_name = '{table_name}'
        AND data_type LIKE '%char%'
        AND column_name NOT LIKE '%ID%'
        ORDER BY ordinal_position """

        connection.execute(column_scanner)
        result = connection.fetchone()
        first_str_column = result[0] if result else None
        if first_str_column != None:
            fetch_query = f"SELECT * FROM {schema}.{table_name} ORDER BY LOWER({first_str_column}) {sort_direction};"
            connection.execute(fetch_query)

    #Nan cleaning ------------------
    elif mutation == "Modular clearance" and len(input) > 0:
        assert (type(input) == list or type(input) == np.ndarray)
        if type(input) != list and type(input) == np.ndarray:
            input = [element for element in input.flat]

        post_cleaning_output = ice_wall(input, type_accpeted)
        return post_cleaning_output

    #Database anomaly clearing
    elif mutation == "Anomaly handler":
        cur = connection.cursor()
        clear_to_process = 0
        if table_name != None and column_names != None and schema != None:
            clear_to_process += 1

        if clear_to_process == 1:
            try:
                # Winner details: Batch processing was applied
                # Winning number: 2
                # Set the database isolation level
                level_selected = 1
                # Isolation protocols
                protocols = [psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
                             psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ,
                             psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE]

                isolation_level = protocols[level_selected]
                connection.set_isolation_level(isolation_level)

                columns = ', '.join(column_names)
                query = f"SELECT {columns} FROM {schema}.{table_name};"
                cur.execute(query)
            except:
                # Rollback in the event of failure
                connection.rollback()
            finally:
                if connection is not closed:
                    connection.close()
    # Data
    #If there is machine learning then add pre-processing protocols here
    #ML preprocessing ------------------
    elif mutation == "ML preprocessing" and len(input) > 0:
        assert (type(input) == list or type(input) == np.ndarray)
        if type(input) != np.ndarray:
            input = np.array(input)

        nan_cleared = ice_wall(input,type_accpeted)

        return nan_cleared

