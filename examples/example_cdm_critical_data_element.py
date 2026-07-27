"""
Example for reading Alation Critical Data Elements (CDM / CDE).

Critical Data Elements are served by the `cde-service`, which uses a dedicated
authentication flow. The SDK handles that transparently: the CDE token is minted from
your Alation access token on the first CDE call (and re-exchanged automatically when it
expires), so you can call the `alation.cdm_critical_data_element` methods directly.

See: https://developer.alation.com/dev/reference/cde-api-overview

Prerequisites:

- You adjusted the "config.ini" file with your settings.

"""

import pathlib

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Define Logging Config
# ================================

logging.basicConfig(
    level=logging.INFO
    , stream=sys.stdout
    , format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================================
# Source Global Config
# ================================
config_path = pathlib.Path(__file__).parent / "config.ini"
config = configparser.ConfigParser()
with open(config_path, 'r') as f:
    config.read_file(f)

ALATION_USER_ID = config.get(section="api", option="ALATION_USER_ID")
ALATION_BASE_URL = config.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section="api", option="ALATION_API_REFRESH_TOKEN")

# ================================
# Authenticate with Alation
# ================================

alation = allie.Alation(
    host=ALATION_BASE_URL
    , user_id=ALATION_USER_ID
    , refresh_token=ALATION_API_REFRESH_TOKEN
)

# ================================
# List all Critical Data Elements
# ================================

# The CDE token is minted lazily on this first call.
all_cdes = alation.cdm_critical_data_element.get_critical_data_elements()
logging.info(f"Found {len(all_cdes)} Critical Data Element(s).")

for cde in all_cdes[:10]:
    logging.info(f"CDE id={cde.id} name={cde.name!r} status={cde.status}")

# ================================
# Filter Critical Data Elements by status
# ================================

certified_cdes = alation.cdm_critical_data_element.get_critical_data_elements(
    query_params=allie.CriticalDataElementParams(status="CERTIFIED")
)
logging.info(f"Found {len(certified_cdes)} CERTIFIED Critical Data Element(s).")

# ================================
# Get a single Critical Data Element by id
# ================================

if all_cdes:
    first_id = all_cdes[0].id
    single_cde = alation.cdm_critical_data_element.get_critical_data_element(first_id)
    logging.info(f"Fetched CDE id={single_cde.id}: {single_cde.name!r}")

# ================================
# Create a single Critical Data Element (and clean it up)
# ================================

# NOTE: the following are WRITE operations that create real objects on your server.
new_cde = alation.cdm_critical_data_element.create_critical_data_element(
    allie.CriticalDataElementItem(
        name="SDK Example CDE",
        description="Created by the Allie-SDK example.",
        status="CANDIDATE",
    )
)
logging.info(f"Created CDE id={new_cde.id} name={new_cde.name!r}")

# Update it (synchronous; returns the updated element). Note: `status` is not an update
# field — use the status-transition endpoint for that.
updated_cde = alation.cdm_critical_data_element.update_critical_data_element(
    new_cde.id,
    allie.CriticalDataElementItem(description="Updated by the Allie-SDK example."),
)
logging.info(f"Updated CDE id={updated_cde.id} description={updated_cde.description!r}")

# Delete the element we just created so the example leaves no residue.
alation.cdm_critical_data_element.delete_critical_data_element(new_cde.id)
logging.info(f"Deleted CDE id={new_cde.id}")

# ================================
# Bulk-create Critical Data Elements (asynchronous → job)
# ================================

# Bulk-create runs asynchronously. By default the SDK blocks until the job finishes and
# returns the terminal CDEJob (pass wait_for_completion=False to get the job key instead).
job = alation.cdm_critical_data_element.create_critical_data_elements_bulk(
    [
        allie.CriticalDataElementItem(name="SDK Example CDE 1", status="CANDIDATE"),
        allie.CriticalDataElementItem(name="SDK Example CDE 2", status="CANDIDATE"),
    ]
)
logging.info(f"Bulk-create job {job.key} finished with status {job.status}")
logging.info(f"Job result: {job.result}")

# ================================
# Bulk-delete Critical Data Elements by id (synchronous)
# ================================

# Look up the elements we just created by name and delete them in one call.
example_cdes = alation.cdm_critical_data_element.get_critical_data_elements(
    query_params=allie.CriticalDataElementParams(search="SDK Example CDE")
)
ids_to_delete = [c.id for c in example_cdes if c.name.startswith("SDK Example CDE")]
if ids_to_delete:
    alation.cdm_critical_data_element.delete_critical_data_elements_bulk(ids_to_delete)
    logging.info(f"Bulk-deleted {len(ids_to_delete)} example CDE(s): {ids_to_delete}")
