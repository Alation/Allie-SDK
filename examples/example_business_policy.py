"""
Example of creating, listing, updating and deleting one business policy.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- In the "Set Global Variables" section below define the custom template name and
  policy group id that should be associated with the business policy. Both must already exist.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

# For creating the business policy, please define the following:
BUSINESS_POLICY_TITLE = "Business Policy Example"
CUSTOM_TEMPLATE_NAME = "GDPR"
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
            title = CUSTOM_TEMPLATE_NAME
        )
    )

if templates:
    if len(templates) > 1:
        logging.error(f"More than one custom template with the name {CUSTOM_TEMPLATE_NAME} found.")
        logging.error("How to resolve: Make sure the template name is unique!")
        sys.exit(1)
    else:
        my_template_id = templates[0].id
else:
    logging.error(f"No custom template with name '{CUSTOM_TEMPLATE_NAME}' found!")
    sys.exit(1)

# ================================
# CREATE MULTIPLE POLICIES
# ================================

create_business_policy_result = alation.business_policy.create_business_policies(
    [
        allie.BusinessPolicyPostItem(
            title = BUSINESS_POLICY_TITLE
            , template_id = my_template_id
            , policy_group_ids = [POLICY_GROUP_ID]
            , fields = [
                allie.CustomFieldValueItem(
                    field_id = 8
                    , value = [
                        allie.CustomFieldDictValueItem(
                            otype = "user"
                            , oid = 1
                        )
                    ]
                )
            ]
        )
    ]
)


if create_business_policy_result:
    if create_business_policy_result[0].status == "successful":
        logging.info("Business policy created successfully.")
    elif create_business_policy_result[0].status == "failed":
        logging.error(f"Failed to create Business Policy. Reason:")
        logging.error(create_business_policy_result[0].result)
        sys.exit(1)


# ================================
# GET BUSINESS POLICIES
# ================================

business_policies = alation.business_policy.get_business_policies()

if business_policies:
    for p in business_policies:
        if p.title == BUSINESS_POLICY_TITLE:
            business_policy_id = p.id
else:
    logging.error(f"No business policy with name '{BUSINESS_POLICY_TITLE}' found.")
    sys.exit(1)

# ================================
# UPDATE MANY POLICIES
# ================================

update_result = alation.business_policy.update_business_policies(
    business_policies = [
        allie.BusinessPolicyPutItem(
            id = business_policy_id
            , title = BUSINESS_POLICY_TITLE
            , template_id = my_template_id
            , policy_group_ids = allie.BusinessPolicyGroupIds(
                add = [1]
            )
            , fields = [
                allie.CustomFieldValueItem(
                    field_id = 8
                    , value = [
                        allie.CustomFieldDictValueItem(
                            otype = "user"
                            , oid = 2
                        )
                    ]
                )
            ]
        )
    ]
)

if update_result[0].status == "successful":
    logging.info("Business policy updated successfully.")

# ================================
# DELETE POLICIES
# ================================

delete_business_policy_result = alation.business_policy.delete_business_policies(
    business_policies =
        [
            allie.BusinessPolicy(
                id = business_policy_id
            )
        ]
)

if delete_business_policy_result.result == "successful":
    logging.info("All done!")
