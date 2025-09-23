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

from allie_sdk import JobDetailsRdbmsResult

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

if steward_field is None:
    logging.error("No Steward custom field found")
    sys.exit(1)
else:
    steward_field_id = steward_field[0].id


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
                    field_id = steward_field_id
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

created_schema_id = None
if post_schema_response is None:
    logging.error("Tried to submit request ... but somehow heard nothing back!")
    sys.exit(1)
else:
    if isinstance(post_schema_response, list):
        for r in post_schema_response:
            if r.status == "successful":
                created_schema_id = r.result[0].mapping[0].id
                logging.info(r.result[0].response)
                logging.info(f"The following schemas were created (IDs): {created_schema_id}")
            else:
                logging.error(f"Finished with status {r.status}: {r.result}")
    else:
        logging.error("Unexpected result ... I don't know how to handle this ...")
        sys.exit(1)


# ================================
# UPDATE SCHEMA METADATA WITH PATCH
# ================================

if created_schema_id:
    patch_schema_response = alation.rdbms.patch_schemas(
        ds_id = DATA_SOURCE_ID
        , schemas = [
            allie.SchemaPatchItem(
                id = created_schema_id
                , title = "Orders - Updated"
                , description = "This is the updated orders schema ..."
            )
        ]
    )

    """
    Example response content:
    [JobDetailsRdbms(status='successful', msg='Job finished in 0.301728 seconds at 2024-09-24 14:42:11.070983+00:00', result=[JobDetailsRdbmsResult(response='Updated 1 schema objects.', mapping=[JobDetailsRdbmsResultMapping(id=218, key='193.ORDERS')], errors=[])])]
    """

    if patch_schema_response is None:
        logging.error("Tried to submit patch request ... but somehow heard nothing back!")
        sys.exit(1)
    else:
        if isinstance(patch_schema_response, list):
            for r in patch_schema_response:
                if r.status == "successful":
                    logging.info(r.result[0].response)
                else:
                    logging.error(f"Finished with status {r.status}: {r.result}")
        else:
            logging.error("Unexpected patch result ... I don't know how to handle this ...")
            sys.exit(1)
else:
    logging.warning("Skipping schema patch example because no schema ID was captured from the create step.")


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

if post_table_response is None:
    logging.error("Tried to submit request ... but somehow heard nothing back!")
    sys.exit(1)
else:
    if isinstance(post_table_response, list):
        for r in post_table_response:
            if r.status == "successful":
                created_table_id = r.result[0].mapping[0].id
                logging.info(r.result[0].response)
                logging.info(f"The following tables were created (IDs): {created_table_id}")
            else:
                logging.error(f"Finished with status {r.status}: {r.result}")
    else:
        logging.error("Unexpected result ... I don't know how to handle this ...")
        sys.exit(1)

# ================================
# UPDATE TABLE WITH PATCH
# ================================

patch_table_response = alation.rdbms.patch_tables(
    ds_id = DATA_SOURCE_ID,
    tables = [
        allie.TablePatchItem(
            id = created_table_id,
            title = "Refunds - Updated",
            description = "Updated description for the refunds table ...",
            table_comment = "Updated comment"
        )
    ]
)

if patch_table_response is None:
    logging.error("Tried to submit table patch request ... but somehow heard nothing back!")
    sys.exit(1)
else:
    if isinstance(patch_table_response, list):
        for r in patch_table_response:
            if r.status == "successful":
                logging.info(r.result[0].response)
            else:
                logging.error(f"Finished with status {r.status}: {r.result}")
    else:
        logging.error("Unexpected result ... I don't know how to handle this ...")
        sys.exit(1)

# ================================
# CREATE COLUMN WITH TECHNICAL AND LOGICAL METADATA
# ================================

#
# post_column_response = alation.rdbms.post_columns(
#     ds_id = DATA_SOURCE_ID
#     , columns = [
#         allie.ColumnItem(
#             key = f"{DATA_SOURCE_ID}.ORDERS.refunds.id"
#             , column_type = "INTEGER"
#             , title = "ID"
#             , description = "This is the id column of the refunds table ..."
#             , index = allie.ColumnIndex(
#                 isPrimaryKey = True
#                 , isForeignKey = False
#                 , referencedColumnId = None
#                 , isOtherIndex = False
#             )
#         )
#     ]
# )
#
# """
# Example response content:
# [JobDetailsRdbms(status='successful', msg='Job finished in 0.586626 seconds at 2024-09-24 14:32:38.439446+00:00', result=[JobDetailsRdbmsResult(response='Upserted 1 attribute objects.', mapping=[JobDetailsRdbmsResultMapping(id=848418, key='193.ORDERS.refunds.id')], errors=[])])]
# """
#
# if post_column_response is None:
#     logging.error("Tried to submit request ... but somehow heard nothing back!")
#     sys.exit(1)
# else:
#     if isinstance(post_column_response, list):
#         for r in post_column_response:
#             if r.status == "successful":
#                 created_column_id = r.result[0].mapping[0].id
#                 logging.info(r.result[0].response)
#                 logging.info(f"The following columns were created (IDs): {created_column_id}")
#             else:
#                 logging.error(f"Finished with status {r.status}: {r.result}")
#     else:
#         logging.error("Unexpected result ... I don't know how to handle this ...")
#         sys.exit(1)
#
# # ================================
# # UPDATE COLUMN WITH PATCH
# # ================================
#
# patch_column_response = alation.rdbms.patch_columns(
#     ds_id = DATA_SOURCE_ID,
#     columns = [
#         allie.ColumnPatchItem(
#             id = created_column_id
#             , title = "ID"
#             , description = "Updated description for the id column ..."
#             , index=allie.ColumnIndex(
#                 isPrimaryKey=True
#                 , isForeignKey=False
#                 , referencedColumnId=None
#                 , isOtherIndex=False
#             )
#         )
#     ]
# )
#
# if patch_column_response is None:
#     logging.error("Tried to submit patch request ... but somehow heard nothing back!")
#     sys.exit(1)
# else:
#     if isinstance(patch_column_response, list):
#         for r in patch_column_response:
#             if r.status == "successful":
#                 logging.info(r.result[0].response)
#             else:
#                 logging.error(f"Finished with status {r.status}: {r.result}")
#     else:
#         logging.error("Unexpected result ... I don't know how to handle this ...")
#         sys.exit(1)
#
