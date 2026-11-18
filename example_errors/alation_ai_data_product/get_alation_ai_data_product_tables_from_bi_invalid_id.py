"""Example of fetching BI upstream tables with an invalid object identifier.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- The BI object type below exists in your Alation environment.
"""

import configparser
import logging
import sys

import allie_sdk as allie


# ================================
# Set Global Variables
# ================================

BI_OBJECT_TYPE = "dashboard"
INVALID_BI_OBJECT_ID = -1

# ================================
# Define Logging Config
# ================================

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ================================
# Source Global Config
# ================================

config = configparser.ConfigParser()
config.read("./../config.ini")

ALATION_USER_ID = config.get(section="api", option="ALATION_USER_ID")
ALATION_BASE_URL = config.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section="api", option="ALATION_API_REFRESH_TOKEN")

# ================================
# Create Session With Your Alation Instance
# ================================

alation = allie.Alation(
    host=ALATION_BASE_URL,
    user_id=ALATION_USER_ID,
    refresh_token=ALATION_API_REFRESH_TOKEN,
)

# ================================
# FETCH TABLES FROM BI
# ================================

tables = alation.alation_ai_data_product.get_upstream_tables_from_bi_object(
    allie.AlationAIGetUpstreamTablesFromBiObjectParams(
        type=BI_OBJECT_TYPE,
        id=INVALID_BI_OBJECT_ID,
    )
)

logging.info("Returned tables: %s", tables)

"""
Expected behaviour: Fail

requests.exceptions.HTTPError: 422 Client Error or 404 Client Error depending on how your
Alation environment validates unknown BI objects.
"""
