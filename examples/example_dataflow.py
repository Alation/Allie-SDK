"""
Example of creating and manipulating lineage via /dataflow endpoint.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You have ingested catalog metadata

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================


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
# CREATE/UPDATE DATAFLOW OBJECTS WITH LINEAGE PATHS
# ================================

# Add/Update Objects

dflow1 = allie.Dataflow(
    title="Purchase transaction Transformation"
    , description="<p>Data flow from Trips table to Employees.csv in S3</p>"
    , content="Select * into trip_secure_view from test_view_citibike;"
    , group_name="Snowflake-1"
    , external_id="api/df101")

dflow2 = allie.Dataflow(
    title="ample data flow Cat session"
    , description="<p>Sample description From Radek</p>>"
    , content="select c.id, c.amount from customers c inner join purchases p on c.id = p.cid;"
    , group_name="Snowflake-12"
    , external_id="api/df102")

paths=[
        [
            [allie.DataflowPathObject(otype='table', key='95.CITIBIKE.PUBLIC.TRIP_SECURE_VIEW')],
            [allie.DataflowPathObject(otype='dataflow', key='api/df102')],
            [allie.DataflowPathObject(otype='table', key='95.CITIBIKE.PUBLIC.TEST_VIEW_CITIBKE')]
        ],
        [
            [allie.DataflowPathObject(otype='table', key='95.CITIBIKE.PUBLIC.TRIPS')],
            [allie.DataflowPathObject(otype='dataflow', key='api/df101')],
            [allie.DataflowPathObject(otype='file', key='6.radek-alation-ps/Employees/Employees.csv')]
        ]
    ]

df_payload = allie.DataflowPayload()
df_payload.dataflow_objects = [dflow1, dflow2]
df_payload.paths = paths

result = alation.dataflow.create_or_replace_dataflows(df_payload)

# result contains status and list of added/updated objects
print(result)

modified_dataflows = []
if result[0].status == 'successful':
    modified_dataflows.append(result[0].result[0].mapping)
    print(f"Number of dataflows added/updated: {result[0].result[0].response}")
    for map in result[0].result[0].mapping:
        print(f"The following dataaflow was modified: {map}" )
    # print(f"The following dataaflows were updated (IDs): {map for map in result[0].result[0].mapping]}")


# find the api/df102 mapping
sample_dataflow = next((d for d in result[0].result[0].mapping if d.external_id == "api/df102"), None)


# ================================
# UPDATE/PATCH DATAFLOW OBJECTS (WITHOUT LINEAGE PATHS)
# ================================

# PATCH Objects

# Update test (dataflow ID is required)
dflowpatch = allie.DataflowPatchItem(
    title="Sample data flow changed"
    , description="<p>Sample description</p>>"
    , content="select c.id, c.amount from customers;"
    , group_name="Snowflake-12"
    , id=sample_dataflow.id)

result = alation.dataflow.update_dataflows([dflowpatch])

print(result)

# ================================
# DELETE DATAFLOW OBJECTS
# ================================

result = alation.dataflow.delete_dataflows(
    ["api/df101", "api/df102"]
    , allie.DataflowParams(keyField="external_id"))

print(result)
