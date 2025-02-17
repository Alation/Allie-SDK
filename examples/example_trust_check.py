"""
Example of working with trust checks.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- We define for which catalog object we want to set the trust check for:
    - Specify the DATA_SOURCE_ID in the "Set Global Variables" section below.
    - Specify the TABLE_ID in the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

# adjust to your requirements
DATA_SOURCE_ID = 1
TABLE_ID = 1

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


# ================================
# CREATE TRUST CHECK
# ================================

post_trust_check_response = alation.trust_checks.post_trust_check(
    trust_check = allie.TrustCheckFlagItem(
        flag_type = "WARNING"
        , flag_reason = "Something went wrong."
        , subject = allie.TrustCheckFlagSubject(
            otype = "table"
            , id = TABLE_ID
        )
    )
)

if post_trust_check_response is None:
    logging.error("Tried to post trust check but somehow received no response ...")
    sys.exit(1)
elif isinstance(post_trust_check_response, allie.JobDetails):
    if post_trust_check_response.status == "successful":
        trust_check_flag_id = post_trust_check_response.result.id
        print(f"Posted info to trust check flag with id: {trust_check_flag_id}")
    else:
        logging.error(f"The job ended with following status: {post_trust_check_response.status}.")
        logging.error(f"More details: {post_trust_check_response.result}")
        sys.exit(1)
else:
    logging.error("Unexpected result ... I don't know what to do ...")
    sys.exit(1)

# ================================
# GET TRUST CHECK
# ================================

get_trust_check_response = alation.trust_checks.get_trust_checks(
    query_params = allie.TrustCheckFlagParams(
        otype = "table"
        , oid = TABLE_ID
    )
)

if get_trust_check_response is None:
    logging.error("Tried to get trust check but somehow received no response ...")
    sys.exit(1)
else:
    logging.info("Trust checks successfully fetched.")

# ================================
# UPDATE TRUST CHECK
# ================================

# NOTE: You can't update flag_reason for ENDORSEMENT flag types as they don't have a reason.

update_trust_check_response = alation.trust_checks.put_trust_check(
    trust_check = allie.TrustCheckFlag(
        id = trust_check_flag_id
        , flag_type = "WARNING"
        , flag_reason = "ETL process failed yesterday: Data is out-of-date!"
    )
)

if update_trust_check_response is None:
    logging.error("Tried to update trust check but somehow received no response ...")
    sys.exit(1)
elif isinstance(update_trust_check_response, allie.JobDetails):
    if update_trust_check_response.status == "successful":
        trust_check_flag_id = update_trust_check_response.result.id
        print(f"Updated trust check flag with id: {trust_check_flag_id}")
    else:
        logging.error(f"The job ended with following status: {update_trust_check_response.status}.")
        logging.error(f"More details: {update_trust_check_response.result}")
        sys.exit(1)
else:
    logging.error("Unexpected result ... I don't know what to do ...")
    sys.exit(1)

# ================================
# DELETE TRUST CHECK
# ================================

delete_trust_check_response = alation.trust_checks.delete_trust_check(
    allie.TrustCheckFlag(
        id = trust_check_flag_id
    )
)

if delete_trust_check_response is None:
    logging.error("Tried to delete trust check but somehow received no response ...")
    sys.exit(1)
elif isinstance(delete_trust_check_response, allie.JobDetails):
    if delete_trust_check_response.status == "successful":
        print(f"Deleted trust check flag.")
    else:
        logging.error(f"The job ended with following status: {delete_trust_check_response.status}.")
        logging.error(f"More details: {delete_trust_check_response.result}")
        sys.exit(1)
else:
    logging.error("Unexpected result ... I don't know what to do ...")
    sys.exit(1)