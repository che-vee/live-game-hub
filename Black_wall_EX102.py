import math
import numpy as np
from sqlalchemy.dialects.postgresql import psycopg2
import psycopg2.extensions

def black_wall_protocol_EX102(connection, input, mutation, dates, column_names, table_name, schema, type_accpeted):
    def ice_wall(input, type_accepted):
        dev_mode = 1
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
            return input, dates
    #Nan cleaning ------------------
    if mutation == "Modular clearance" and len(input) > 0:
        assert (type(input) == list or type(input) == np.ndarray)
        if type(input) != list and type(input) == np.ndarray:
            input = [element for element in input.flat]

        post_cleaning_output = ice_wall(input, type_accpeted)
        return post_cleaning_output
    #Database anomaly clearing
    if mutation == "Anomaly handler":
        cur = connection.cursor()
        clear_to_process = 0
        if table_name != None and column_names != None and schema != None:
            clear_to_process += 1

        if clear_to_process == 1:
            try:
                # Set the database isolation level
                level_selected = 1
                # Isolation protocols
                protocols = [psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
                             psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ,
                             psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE]

                isolation_level = protocols[level_selected]
                connection.set_isolation_level(isolation_level)

                for column in column_names:
                    cur.execute(f"SELECT {column} FROM {schema}.{table_name};")
            except:
                # Rollback in the event of failure
                connection.rollback()


    # Data
    #If there is machine learning then add pre-processing protocols here
    #ML preprocessing ------------------
    if mutation == "ML preprocessing" and len(input) > 0:
        assert (type(input) == list or type(input) == np.ndarray)
        if type(input) != np.ndarray:
            input = np.array(input)

        nan_cleared = ice_wall(input,type_accpeted)

        return nan_cleared