"""
Example of creating, listing, updating and deleting one document.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You created a glossary. Set the GLOSSARY_ID within the "Set Global Variables" section below.
- The template for the glossary term has a field called "Status" assigned. Set the TEMPLATE_NAME within the "Set Global Variables" section below.
- The "Status" field can be set to values: "Under Review", "Approved".
- The document template must have a unique template name.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

GLOSSARY_ID = 1
TEMPLATE_NAME = "DS Test 4"

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
            title = TEMPLATE_NAME
        )
    )

if templates:
    if len(templates) > 1:
        logging.error(f"More than one document template with the name {TEMPLATE_NAME} found.")
        logging.error("How to resolve: Make sure the template name is unique!")
        sys.exit(1)
    else:
        my_template_id = templates[0].id
else:
    logging.error("No template by the name of '{DOCUMENT_TEMPLATE_NAME}' was found.")
    sys.exit(1)

status_field_details = alation.custom_field.get_custom_fields(
    query_params = allie.CustomFieldParams(
        name_singular = 'Status'
    )
)

if not status_field_details:
    logging.error("No Status field was found.")
    sys.exit(1)
else:
    status_field_id = status_field_details[0].id


# ================================
# CREATE GLOSSARY TERMS
# ================================

create_glossary_term_result = alation.glossary_term.post_glossary_terms(
    [
        allie.GlossaryTermItem(
            title = "My Term 1"
            , description = "This is the description for Term 1"
            , template_id = my_template_id
            , glossary_ids = [ 1 ]
            , custom_fields = [
                allie.CustomFieldValueItem(
                    field_id=status_field_id
                    , value=allie.CustomFieldStringValueItem(
                        value='Approved'
                    )
                )
            ]
        )
    ]
)

if create_glossary_term_result[0].status == "successful":
    created_glossary_term_id = create_glossary_term_result[0].result.created_terms[0].id
    print(f"Number of glossary terms created: {create_glossary_term_result[0].result.created_term_count}")
    print(f"The following glossary terms were created (IDs): {created_glossary_term_id}")

# ================================
# GET GLOSSARY TERMS
# ================================

existing_terms = alation.glossary_term.get_glossary_terms(
    query_params = allie.GlossaryTermParams(
        # search = "'My Term 1'"
        id = created_glossary_term_id
    )
)


if existing_terms:
    print(f"Retrieved document with id {created_glossary_term_id}.")


# ================================
# UPDATE GLOSSARY TERMS
# ================================


updated_term_result = alation.glossary_term.put_glossary_terms(
    [
        allie.GlossaryTermItem(
            id = created_glossary_term_id
            , description = "This is yet another description for Term 1"
        )
    ]
)

if updated_term_result[0].status == "successful":
    print(f"Number of documents updated: {updated_term_result[0].result.updated_term_count}")
    print(f"The following documents were updated (IDs): {updated_term_result[0].result.updated_terms[0].id}")

# ================================
# DELETE GLOSSARY TERMS
# ================================

deleted_term_result = alation.glossary_term.delete_glossary_terms(
    existing_terms
 )

if deleted_term_result.status == "successful":
    print(f"Number of documents deleted: {deleted_term_result.result.deleted_term_count}")
    print(f"The following documents were deleted (IDs): {deleted_term_result.result.deleted_term_ids}")
