import math
import numpy as np
from sqlalchemy.dialects.postgresql import psycopg2
import psycopg2.extensions

def black_wall_protocol_EX102(connection, input, mutation, dates, column_names, table_name, schema, type_accpeted):
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
        dev_mode = 0
        if dev_mode == 1:
            print("---")
            print(f"Type accepted: {type_accepted}")
            print(f"Input data type: {type(input)}")
            print(f"Initial input: {input}")

        # Filter
        filtered_list = [item for item in input if isinstance(item, type_accepted) and not (isinstance(item, float) and math.isnan(item))]
        # Failsafe
        failsafe = []
        for x in filtered_list:
            if type(x) == type_accepted:
                failsafe.append(x)

        if dev_mode == 1:
            print(f"Post-filtering: {filtered_list}")
            print(f"Failsafe: {failsafe}")
            print("---")

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
        dormant_state_DB_sync = 1
        if dormant_state_DB_sync == 1:
            return 0
        # Overwrite  missing integers with zero, strings with empty string
        connection = connection.cursor()
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
            fetch_query = f"SELECT * FROM {schema}.{table_name} ORDER BY {first_str_column} ASC;"
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
                # Winning number: 2
                experimentation_method = 0
                # Set the database isolation level
                level_selected = 1
                # Isolation protocols
                protocols = [psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
                             psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ,
                             psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE]

                isolation_level = protocols[level_selected]
                connection.set_isolation_level(isolation_level)
                if experimentation_method == 0:
                    for column in column_names:
                        cur.execute(f"SELECT {column} FROM {schema}.{table_name};")
                elif experimentation_method == 1:
                    columns = ', '.join(column_names)
                    query = f"SELECT {columns} FROM {schema}.{table_name};"
                    cur.execute(query)
                elif experimentation_method == 2:
                    queries = [f"SELECT {column} FROM {schema}.{table_name};" for column in
                               column_names]  # List of queries

                    # Use ThreadPoolExecutor to execute queries in parallel
                    with ThreadPoolExecutor(max_workers=len(queries)) as executor:
                        future_to_query = {executor.submit(execute_query, connection, query): query for query in
                                           queries}

                        for future in as_completed(future_to_query):
                            query = future_to_query[future]
                            try:
                                data = future.result()

                            except Exception as exc:
                                print(f'{query} generated an exception: {exc}')

            except:
                # Rollback in the event of failure
                connection.rollback()
    # Data
    #If there is machine learning then add pre-processing protocols here
    #ML preprocessing ------------------
    elif mutation == "ML preprocessing" and len(input) > 0:
        assert (type(input) == list or type(input) == np.ndarray)
        if type(input) != np.ndarray:
            input = np.array(input)

        nan_cleared = ice_wall(input,type_accpeted)

        return nan_cleared
