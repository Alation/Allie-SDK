"""Example of uploading a data dictionary file via the Allie SDK."""

import configparser
import logging
import sys
from pathlib import Path
from time import sleep

import allie_sdk as allie


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")

ALATION_USER_ID = CONFIG.get(section="api", option="ALATION_USER_ID")
ALATION_BASE_URL = CONFIG.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = CONFIG.get(section="api", option="ALATION_API_REFRESH_TOKEN")

# Update these variables for your environment
TARGET_OBJECT_TYPE = "data"  # see SUPPORTED_OBJECT_TYPES for the full list
TARGET_OBJECT_ID = 1
DATA_DICTIONARY_PATH = Path("./sample_data_dictionary.csv")

if not DATA_DICTIONARY_PATH.exists():
    logging.error("Create a sample data dictionary file before running this example.")
    sys.exit(1)

alation = allie.Alation(
    host=ALATION_BASE_URL,
    user_id=ALATION_USER_ID,
    refresh_token=ALATION_API_REFRESH_TOKEN,
)

payload = allie.UploadDataDictionaryRequestPayload(
    overwrite_values=True,
    allow_reset=False,
    file=DATA_DICTIONARY_PATH,
)

task = alation.data_dictionary.upload_data_dictionary(
    TARGET_OBJECT_TYPE,
    TARGET_OBJECT_ID,
    payload,
)

logging.info("Data dictionary upload task created with id: %s", task.task.id)

# Poll the task endpoint for a short time just to illustrate usage
task_details = alation.data_dictionary.get_data_dictionary_task_details(task.task.id)

while task_details.state != "COMPLETED":
    logging.info(
        "Task %s currently in state %s (batches completed: %s/%s)",
        task_details.id,
        task_details.state,
        task_details.progress.batches_completed if task_details.progress else 0,
        task_details.progress.total_batches if task_details.progress else 0,
    )
    sleep(2)
    task_details = alation.data_dictionary.get_data_dictionary_task_details(task.task.id)

logging.info("Task %s completed with status %s", task_details.id, task_details.status)

if task_details.status != "SUCCEEDED":
    errors = alation.data_dictionary.get_data_dictionary_task_errors(task_details.id)
    if errors:
        logging.info("First reported error: %s", errors[0].error_message)
