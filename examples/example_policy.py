"""
Example of creating, listing, updating and deleting one policy.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Adjust the variables in the "Set Global Variables" section below.
- Note: The policy template must have a unique name.
- A policy group must already exist.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

POLICY_TEMPLATE_NAME = "GDPR"
POLICY_TITLE = "PII Policy"
POLICY_DESCRIPTION = "Policy outlining PII in our organization"
POLICY_GROUP_ID = 1

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

templates = alation.custom_template.get_custom_templates(
        allie.CustomTemplateParams(
            title = POLICY_TEMPLATE_NAME
        )
    )

if templates is None:
    logging.error("No template by the name of '{POLICY_TEMPLATE_NAME}' was found.")
    sys.exit(1)
elif isinstance(templates, list):
    if len(templates) > 1:
        logging.error(f"More than one custom template with the name {POLICY_TEMPLATE_NAME} found.")
        logging.error("How to resolve: Make sure the template name is unique!")
        sys.exit(1)
    else:
        my_template_id = templates[0].id
else:
    logging.error("Unexpected result ... I don't know what to do ...")
    sys.exit(1)

# ================================
# Create Policy
# ================================


# Create a Policy
policy_item = allie.BusinessPolicyPostItem(
    title = POLICY_TITLE,
    description = POLICY_DESCRIPTION,
    template_id = my_template_id,
    policy_group_ids = [ POLICY_GROUP_ID ]
)

create_policy_result = alation.business_policy.create_business_policies(
    [
        policy_item
    ]
)

if create_policy_result is None:
    logging.error("Tried to create policy but received no response ...")
    sys.exit(1)
elif isinstance(create_policy_result, list):
    for r in create_policy_result:
        if r.status == "successful":
            logging.info(f"Policy created successfully.")
        else:
            logging.error(f"Policy creation job status: {r.status}. Details: {r.result}")
            sys.exit(1)
else:
    logging.error("Received unexpected response ... I don't know what to do ...")
    sys.exit(1)

# ================================
# Get Policy
# ================================

get_policy_result = alation.business_policy.get_business_policies(
    query_params = allie.BusinessPolicyParams(
        search = POLICY_TITLE
    )
)


if get_policy_result is None:
    logging.error("Tried to get policy but received no response ...")
    sys.exit(1)
elif isinstance(get_policy_result, list):
    if len(get_policy_result) > 1:
        logging.error(f"More than one policy with the name {POLICY_TITLE} found.")
        sys.exit(1)
    elif len(get_policy_result) == 1:
        existing_policy = get_policy_result[0]
        logging.info(f"Policy found. The ID is: {existing_policy.id}")
    else:
        logging.error("Unexpected result ... I don't know what to do ...")
        sys.exit(1)
else:
    logging.error("Received unexpected response ... I don't know what to do ...")
    sys.exit(1)


# ================================
# Update Policy
# ================================


# Update a Policy
policy_item = allie.BusinessPolicyPutItem(
    id = existing_policy.id
    , description = f"{POLICY_DESCRIPTION} - updated!"
)

update_policy_result = alation.business_policy.update_business_policies(
    [
        policy_item
    ]
)

if update_policy_result is None:
    logging.error("Tried to update policy but received no response ...")
    sys.exit(1)
elif isinstance(update_policy_result, list):
    for r in update_policy_result:
        if r.status == "successful":
            logging.info(f"Policy updated successfully.")
        else:
            logging.error(f"Policy update job status: {r.status}. Details: {r.result}")
            sys.exit(1)
else:
    logging.error("Received unexpected response ... I don't know what to do ...")
    sys.exit(1)


# ================================
# Delete Policy
# ================================



delete_policy_result = alation.business_policy.delete_business_policies(
    [
        existing_policy
    ]
)

if delete_policy_result is None:
    logging.error("Tried to delete policy but received no response ...")
    sys.exit(1)
elif isinstance(delete_policy_result, allie.JobDetails):
    if delete_policy_result.status == "successful":
        logging.info(f"Policy deleted successfully.")
    else:
        logging.error(f"Policy deletion job status: {delete_policy_result.status}. Details: {delete_policy_result.result}")
        sys.exit(1)
else:
    logging.error("Received unexpected response ... I don't know what to do ...")
    sys.exit(1)