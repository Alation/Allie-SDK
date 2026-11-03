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
