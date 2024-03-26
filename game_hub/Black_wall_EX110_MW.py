from django.utils.deprecation import MiddlewareMixin
from django.apps import apps
from sqlalchemy.dialects.postgresql import psycopg2
import psycopg2.extensions
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy.testing.exclusions import closed
from Black_wall_protocols import black_wall_protocols

def test_startup_operation():
    # Define the models you want to gather metadata for
    models = ['Payment', 'Game', 'GameType', 'GamePurchase', 'Session']

    # Iterate over the models and gather metadata
    for model_name in models:
        model_meta = get_model_meta_info(model_name)
        # Print the gathered metadata (for demonstration purposes)
        print(f"Metadata for {model_name}: {model_meta}")


def get_model_meta_info(model_name, app_label):
    model = apps.get_model(app_label, model_name)
    fields = model._meta.get_fields()

    # Extraction of schema and table name
    db_table = model._meta.db_table
    schema_name, _, table_name = db_table.partition('.')
    schema_name = schema_name if schema_name else 'default'

    # Initialize lists for column names and type constraints
    column_names = []
    type_constraints = []

    for field in fields:
        # Skip relation fields to focus on direct columns
        if field.is_relation and (field.many_to_many or field.one_to_many or field.one_to_one):
            continue

        # Add the column name (use db_column if available, otherwise field name)
        column_names.append(field.db_column or field.name)

        # Add the data type of the column
        type_constraints.append(field.get_internal_type())

    return schema_name, table_name, column_names, type_constraints

class BlackWallEX110(MiddlewareMixin):
    startup_operation_executed = False
    def __init__(self, get_response):
        super().__init__(get_response)
        # Execute the startup operation only once per Django startup
        if not BlackWallEX110.startup_operation_executed:
            self.run_startup_operation()
            BlackWallEX110.startup_operation_executed = True

    def run_startup_operation(self):
        # The layout of every table currently
        try:
            # get info on individual tables
            schema_01, table_name_01, columns_01, type_constraints_01 = get_model_meta_info("Payment","game_hub")
            payment_schema = schema_01
            payment_columns = columns_01
            payment_table_name = table_name_01
            payment_type_constraints = type_constraints_01

            schema_02, table_name_02, columns_02, type_constraints_02 = get_model_meta_info("Game","game_hub")
            game_schema = schema_02
            game_columns = columns_02
            games_table_name = table_name_02
            game_type_constraints = type_constraints_02

            schema_03, table_name_03, columns_03, type_constraints_03 = get_model_meta_info("GameType","game_hub")
            game_type_schema = schema_03
            game_type_columns = columns_03
            game_type_table_name = table_name_03
            game_type_type_constraints = type_constraints_03

            schema_04, table_name_04, columns_04, type_constraints_04 = get_model_meta_info("GamePurchase","game_hub")
            game_purchase_schema = schema_04
            game_purchases_columns = columns_04
            game_purchases_table_name = table_name_04
            game_purchases_type_constraints = type_constraints_04

            schema_05, table_name_05, columns_05, type_constraints_05 = get_model_meta_info("Session","game_hub")
            session_schema = schema_05
            session_columns = columns_05
            session_table_name = table_name_05
            session_type_constraints = type_constraints_05

            if True:
                black_wall_AH_threads = [
                                      # Sessions
                                      black_wall_protocols(connection=0,input=0,mutation="Anomaly handler",dates=0, column_names=session_columns,
                                                           table_name=session_table_name,schema=session_schema,type_accpeted=session_type_constraints),
                                      # Game purchases
                                      black_wall_protocols(connection=0, input=0, mutation="Anomaly handler", dates=0, column_names=game_purchases_columns,
                                                           table_name=game_purchases_table_name, schema=game_purchase_schema, type_accpeted=game_purchases_type_constraints),
                                      # Games available
                                      black_wall_protocols(connection=0, input=0, mutation="Anomaly handler", dates=0,
                                                           column_names=game_columns, table_name=games_table_name,
                                                           schema=game_schema, type_accpeted=game_type_constraints),
                                      # game types available
                                      black_wall_protocols(connection=0, input=0, mutation="Anomaly handler", dates=0,
                                                           column_names=game_type_columns, table_name=game_type_table_name,
                                                           schema=game_type_schema, type_accpeted=game_type_type_constraints),
                                      # Payment
                                      black_wall_protocols(connection=0, input=0,mutation="Anomaly handler",dates=0,column_names=payment_columns,
                                                           table_name=payment_table_name,schema=payment_schema,type_accpeted=payment_type_constraints)
                                      ]

                for threads in black_wall_AH_threads:
                    threads.start()
                for initialized_threads in black_wall_AH_threads:
                    initialized_threads.join()

        except:
            # Add rollback at this point
            pass
    def __call__(self, request):
        # After the startup operation, the middleware does nothing on requests.
        return self.get_response(request)

testing_section = 0
if testing_section == 1:
    test_startup_operation()