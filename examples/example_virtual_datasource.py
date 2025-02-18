"""
Example of creating and deleting objects within virtual data source.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You created a virtual datasource.
- Adjust the DATA_SOURCE_ID in the "Set Global Variables" section below.
- Note: The delete action performed at the end will delete all objects within this virtual datasource.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

# Note: this is for uploading the technical metadata
# You have to create the Alation virtual data source beforehand
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
# CREATE VIRTUAL DATA SOURCE OBJECTS WITHIN EXISTING DATA SOURCE
# ================================

# Add/Update Objects
ds_schema = "test"

# create the schema first and then submit the payload, otherwise the parser throws an error
s1 = allie.VirtualDataSourceSchema()
s1.key = f'{DATA_SOURCE_ID}.{ds_schema}'
s1.description = "New Schema for API testing"

t1 = allie.VirtualDataSourceTable()
t1.key = f'{DATA_SOURCE_ID}.{ds_schema}.Orders'
t1.table_type = "TABLE"
t1.table_comment = "This is a sample table created with Allie SDK for Virtual Dat Sources"
t1.title = "ORDERS"
t1.description = "Orders Table python description"
t1.data_location = "//hive_table_location_orders"
t1.definition_sql = "create table select from order_header"

v1 = allie.VirtualDataSourceView()
v1.key = f'{DATA_SOURCE_ID}.{ds_schema}.Orders_View'
v1.table_type = "VIEW"
v1.table_comment = "This is a sample table created with Allie SDK for Virtual Dat Sources"
v1.title = "ORDERS VIEW"
v1.description = "Orders View python description"
v1.view_sql = "select * from orders"

c1 = allie.VirtualDataSourceColumn()
c1.key = f'{t1.key}.Order_number'
c1.column_type = "int"
c1.nullable = False
c1.position = 1
c1.column_comment = "This is a sample column created with Allie SDK for Virtual Data Sources"
c1.description = "Order Number for sales orders"
c1.title = "Order Number"

i1 = allie.VirtualDataSourceIndex()
i1.key = f'{t1.key}.index'
i1.index_type = "PRIMARY"
i1.column_names = [c1.key.split('.')[3]]
i1.data_structure = "BTREE"

vds_objects = [s1, t1, v1, c1, i1]

params = allie.VirtualDataSourceParams()
params.set_title_descs = "true"
params.remove_not_seen = "false"

vds_response = alation.virtual_datasource.post_metadata(
    ds_id=DATA_SOURCE_ID
    , vds_objects=vds_objects
    , query_params=params
)

if vds_response is None:
    logging.error(f"Unable to create objects within virtual datasource.")
    sys.exit(1)
elif isinstance(vds_response, list):
    for r in vds_response:
        if r.status == "successful":
            logging.info("Status for creating virtual objects: successful")
            logging.info(f"> Received {r.result.number_received} objects")
            logging.info(f"> Updated {r.result.updated_objects} objects")
        else:
            logging.error(f"Job ended with status {r.status}: {r.result}")
            sys.exit(1)
else:
    logging.error(f"Received unexpected response ... I don't know what to do ...")
    sys.exit(1)

# ================================
# DELETE VIRTUAL OBJECTS
# ================================


params = allie.VirtualDataSourceParams()
params.set_title_descs = "false"
params.remove_not_seen = "true"

vds_response = alation.virtual_datasource.post_metadata(
    ds_id=DATA_SOURCE_ID
    , vds_objects=[]
    , query_params=params
)

if vds_response is None:
    logging.error(f"Unable to delete objects within virtual datasource.")
    sys.exit(1)
elif isinstance(vds_response, list):
    for r in vds_response:
        if r.status == "successful":
            logging.info("Status for creating virtual objects: successful")
            logging.info(f"> Received {r.result.number_received} objects")
            logging.info(f"> Updated {r.result.updated_objects} objects")
        else:
            logging.error(f"Job ended with status {r.status}: {r.result}")
            sys.exit(1)
else:
    logging.error(f"Received unexpected response ... I don't know what to do ...")
    sys.exit(1)