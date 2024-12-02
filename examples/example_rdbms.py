"""
Example of working with RDBMS objects.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You created a virtual or non-virtual data source configuration in your Alation Catalog that we can use for testing.
- Specify the DATA_SOURCE_ID in the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

# adjust to your requirements
DATA_SOURCE_ID = 1

# ================================
# Define Logging Config
# ================================

logging.basicConfig(
  level=logging.INFO
  , stream = sys.stdout
  , format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================================
# Source Global Config
# ================================

config = configparser.ConfigParser()
config.read("config.ini")

ALATION_USER_ID = config.get(section = "api", option = "ALATION_USER_ID")
ALATION_BASE_URL = config.get(section = "api", option = "ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section = "api", option = "ALATION_API_REFRESH_TOKEN")

# ================================
# Create session with your Alation instance
# ================================

alation = allie.Alation(
    host = ALATION_BASE_URL
    , user_id = ALATION_USER_ID
    , refresh_token = ALATION_API_REFRESH_TOKEN
)

# ================================
# LOOKUP ANY REQUIRED DATA
# ================================

steward_field =  alation.custom_field.get_custom_fields(
    allie.CustomFieldParams(
        name_singular = "Steward"
    )
)

if steward_field:
    steward_field_id = steward_field[0].id
else:
    logging.error("No Steward custom field found")
    sys.exit(1)

# ================================
# CREATE SCHEMA WITH TECHNICAL AND LOGICAL METADATA
# ================================

post_schema_response = alation.rdbms.post_schemas(
    ds_id = DATA_SOURCE_ID
    , schemas = [
        allie.SchemaItem( # <= USE THE DEDICATED DATA CLASS HERE
            key = f"{DATA_SOURCE_ID}.ORDERS"
            , title = "Orders"
            , description = "This is the orders schema ..."
            , custom_fields = [
                allie.CustomFieldValueItem(
                    field_id = 8
                    , value = [
                        allie.CustomFieldDictValueItem(
                            otype = "user"
                            , oid = 1
                        )
                    ]
                )
            ]
        )
    ]
)

"""
Example response content:
[JobDetailsRdbms(status='successful', msg='Job finished in 0.445766 seconds at 2024-09-24 14:28:19.300729+00:00', result=[JobDetailsRdbmsResult(response='Upserted 1 schema objects.', mapping=[JobDetailsRdbmsResultMapping(id=218, key='193.ORDERS')], errors=[])])]
"""

if post_schema_response[0].status == "successful":
    created_schema_id = post_schema_response[0].result[0].mapping[0].id
    print(post_schema_response[0].result[0].response)
    print(f"The following documents were created (IDs): {created_schema_id}")

# ================================
# CREATE TABLE WITH TECHNICAL AND LOGICAL METADATA
# ================================


post_table_response = alation.rdbms.post_tables(
    ds_id = DATA_SOURCE_ID
    , tables = [
        allie.TableItem(
            key = f"{DATA_SOURCE_ID}.ORDERS.refunds"
            , title = "Refunds"
            , description = "This is the refunds table ..."
        )
    ]
)

"""
Example response content:
[JobDetailsRdbms(status='successful', msg='Job finished in 0.313928 seconds at 2024-09-24 14:30:52.634298+00:00', result=[JobDetailsRdbmsResult(response='Upserted 1 table objects.', mapping=[JobDetailsRdbmsResultMapping(id=115164, key='193.ORDERS.refunds')], errors=[])])]
"""

if post_table_response[0].status == "successful":
    created_table_id = post_table_response[0].result[0].mapping[0].id
    print(post_table_response[0].result[0].response)
    print(f"The following documents were created (IDs): {created_table_id}")

# ================================
# CREATE COLUMN WITH TECHNICAL AND LOGICAL METADATA
# ================================


post_column_response = alation.rdbms.post_columns(
    ds_id = DATA_SOURCE_ID
    , columns = [
        allie.ColumnItem(
            key = f"{DATA_SOURCE_ID}.ORDERS.refunds.id"
            , column_type = "INTEGER"
            , title = "ID"
            , description = "This is the id column of the refunds table ..."
        )
    ]
)

"""
Example response content:
[JobDetailsRdbms(status='successful', msg='Job finished in 0.586626 seconds at 2024-09-24 14:32:38.439446+00:00', result=[JobDetailsRdbmsResult(response='Upserted 1 attribute objects.', mapping=[JobDetailsRdbmsResultMapping(id=848418, key='193.ORDERS.refunds.id')], errors=[])])]
"""

if post_column_response[0].status == "successful":
    created_column_id = post_column_response[0].result[0].mapping[0].id
    print(post_column_response[0].result[0].response)
    print(f"The following documents were created (IDs): {created_column_id}")

