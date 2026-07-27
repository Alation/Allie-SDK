"""
Example of reading a Critical Data Manager (CDM / CDE) job failing because the requested
job ID does not exist.

`get_cde_job` calls `GET /cde-service/integration/job/{id}/`. If the ID is not found, the
CDE service returns a non-success status code and the SDK raises a `requests.HTTPError`.

See: https://developer.alation.com/dev/reference/cde-api-overview

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Set the variables in the "Set Global Variables" section below.

"""

import pathlib

import allie_sdk as allie
import logging
import sys
import configparser
import requests

# ================================
# Set Global Variables
# ================================

# MAKE IT FAIL: Use a CDE job ID that does not exist.
INVALID_JOB_ID = 999999999

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

# Resolve config.ini relative to this file (example_errors/config.ini) so the script
# runs correctly from any working directory. Using read_file raises if it is missing
# rather than silently producing an empty config.
config_path = pathlib.Path(__file__).parent.parent / "config.ini"
config = configparser.ConfigParser()
with open(config_path, "r") as f:
    config.read_file(f)

ALATION_USER_ID = config.get(section="api", option="ALATION_USER_ID")
ALATION_BASE_URL = config.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section="api", option="ALATION_API_REFRESH_TOKEN")

# ================================
# Create session with your Alation instance
# ================================

alation = allie.Alation(
    host=ALATION_BASE_URL
    , user_id=ALATION_USER_ID
    , refresh_token=ALATION_API_REFRESH_TOKEN
)

# ================================
# Attempt to read a CDE job that does not exist
# ================================

try:
    job = alation.cdm_job.get_cde_job(INVALID_JOB_ID)
    print(f"CDE job found: id={job.id} status={job.status}")
except requests.exceptions.HTTPError as error:
    print("Failed to read the CDE job!")
    print(f"HTTP status code: {error.response.status_code}")
    print("What to do next: Provide the ID of an existing CDE job.")

"""
expected response:

Failed to read the CDE job!
HTTP status code: 404
What to do next: Provide the ID of an existing CDE job.

expected log message:

... - ERROR - ERROR MESSAGE: Error submitting the CDE GET Request to: /cde-service/integration/job/999999999/ ...
"""
