"""
Example for reading Alation Critical Data Manager (CDM / CDE) jobs.

CDE jobs track asynchronous CDE operations (for example, bulk-creating Critical Data
Elements). They have their own status vocabulary
(`QUEUED`/`IN_PROGRESS`/`FINISHED`/`ERROR`/`CANCELED`), distinct from the core Alation
background-job API.

The SDK handles the CDE authentication transparently, so you can call the
`alation.cdm_job` methods directly.

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
# List recent bulk-creation jobs
# ================================

jobs = alation.cdm_job.get_cde_jobs(
    query_params=allie.CDEJobParams(type="API_BULK_CREATION", order_by="-ts_created")
)
logging.info(f"Found {len(jobs)} bulk-creation job(s).")

for job in jobs[:10]:
    logging.info(f"Job id={job.id} key={job.key} status={job.status}")

# ================================
# Get a single job by id
# ================================

if jobs:
    single_job = alation.cdm_job.get_cde_job(jobs[0].id)
    logging.info(f"Fetched job id={single_job.id}: status={single_job.status}")

# ================================
# Wait for a job to finish (by its uuid key)
# ================================

# Asynchronous writes (e.g. bulk-create, to be added in a later stage) return a job
# `key`. `wait_for_cde_job` blocks until that job reaches a terminal state.
#
# job_key = "<uuid returned by an async write>"
# terminal_job = alation.cdm_job.wait_for_cde_job(job_key)
# logging.info(f"Job {job_key} finished with status {terminal_job.status}")
