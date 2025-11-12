"""
Example of listing native Alation data sources.
Example of creating, listing, updating and deleting OCF Alation data sources.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Set the variables in the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser
import datetime

# ================================
# Set Global Variables
# ================================

OCF_CONNECTOR_ID = 4

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
# Get a list of OCF data sources configured in Alation
# ================================

ocf_datasources = alation.datasource.get_ocf_datasources(
    allie.OCFDatasourceParams(
        include_hidden = False
    )
)

if ocf_datasources is None:
    logging.warning("No OCF datasources found.")
elif isinstance(ocf_datasources, list):
    logging.info("Successfully retrieved list of OCF datasources:")
    for od in ocf_datasources:
        logging.info(od.title)
else:
    logging.error("Unexpected result ... I don't know what to do ...")
    sys.exit(1)


# ================================
# Get a list of native data sources configured in Alation
# ================================

native_datasources = alation.datasource.get_native_datasources()

if native_datasources is None:
    logging.warning("No native datasources found.")
elif isinstance(native_datasources, list):
    logging.info("Successfully retrieved list of native datasources:")
    for nd in native_datasources:
        logging.info(nd.title)
else:
    logging.error("Unexpected result ... I don't know what to do ...")
    sys.exit(1)


# ================================
# Create an OCF data source in Alation
# ================================

datasource_post_payload = allie.OCFDatasourcePostItem(
    connector_id = OCF_CONNECTOR_ID
    , title="New Datasource"
    , description="Sample mysql datasource setup"
    , uri="mysql://192.212.11.23:6543/groceries"
    , db_username = "alation"
    , db_password = "pwd123"
    , private=False
)

datasource_post_response = alation.datasource.create_ocf_datasource(
    datasource = datasource_post_payload
)

if datasource_post_response:
    new_datasource_id = datasource_post_response.id
else:
    logging.error("Unable to create new datasource ...")
    sys.exit(1)

# ================================
# Get an OCF data source in Alation
# ================================

datasource_get_response = alation.datasource.get_ocf_datasource_by_id(
    datasource_id = new_datasource_id
)

if datasource_get_response:
    logging.info(f"Successfully retrieved datasource {datasource_get_response.title} ...")
# ================================
# Update an OCF data source in Alation
# ================================

datasource_update_payload = allie.OCFDatasourcePutItem(
    description="Updated description"
)

datasource_update_response = alation.datasource.update_ocf_datasource(
    datasource_id = new_datasource_id
    , datasource = datasource_update_payload
)

if datasource_update_response:
    updated_datasource_id = datasource_update_response.id
else:
    logging.error("Unable to update datasource ...")
    sys.exit(1)


# ================================
# Delete an OCF data source in Alation
# ================================

delete_datasource_response = alation.datasource.delete_ocf_datasource(
    datasource_id = new_datasource_id
)

logging.info(f"Attempt to delete OCF data source was: {delete_datasource_response.status}")
