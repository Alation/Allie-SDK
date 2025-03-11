"""
Example of creating, listing, updating and deleting one document.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You created a document hub. Set the DOCUMENT_HUB_ID within the "Set Global Variables" section below.
- You created a document hub folder. The script will randomly pick a document hub folder you created.
- The template for the document has a field called "Status" assigned.
- The "Status" field can be set to values: "Under Review", "Approved".
- The document template must have a unique template name (so it should not just be called "Document").

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

DOCUMENT_HUB_ID = 2
DOCUMENT_TEMPLATE_NAME = "DS Test 6"

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
            title = DOCUMENT_TEMPLATE_NAME
        )
    )

if templates is None:
    logging.error("No template by the name of '{DOCUMENT_TEMPLATE_NAME}' was found.")
    sys.exit(1)
elif isinstance(templates, list):
    if len(templates) > 1:
        logging.error(f"More than one document template with the name {DOCUMENT_TEMPLATE_NAME} found.")
        logging.error("How to resolve: Make sure the template name is unique!")
        sys.exit(1)
    else:
        my_template_id = templates[0].id
else:
    logging.error("Unexpected result ... I don't know what to do ...")
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


# get random document hub folder
folders = alation.document_hub_folder.get_document_hub_folders(
    allie.DocumentHubFolderParams(
        document_hub_id = DOCUMENT_HUB_ID
    )
)

if not folders:
    logging.error("ERROR: No document hub folder found.")
    logging.error(f"Solution: Via the Web UI please create a document hub folder within doc hub with id {DOCUMENT_HUB_ID}.")
    sys.exit(1)
else:
    random_folder_id = folders[0].id

# ================================
# CREATE DOCUMENTS
# ================================

create_document_response = alation.document.create_documents(
    [
        allie.DocumentPostItem(
            title = "My KPI 1x1"
            , description = "This is the description for KPI 1"
            , template_id = my_template_id
            , parent_folder_id = random_folder_id
            , nav_link_folder_ids = []
            , document_hub_id = DOCUMENT_HUB_ID
            , custom_fields = [
                allie.CustomFieldValueItem(
                    field_id = status_field_id
                    , value = allie.CustomFieldStringValueItem(
                        value = 'Approved'
                    )
                )
            ]
        )
    ]
)

if create_document_response is None:
    logging.error("Tried to create documents but received no response ...")
    sys.exit(1)
elif isinstance(create_document_response, list):
    for d in create_document_response:
        if d.status == "successful":
            created_document_id = d.result.created_terms[0].id
            logging.info(f"Number of documents created: {d.result.created_term_count}")
            logging.info(f"The following documents were created (IDs): {created_document_id}")
        else:
            logging.error(f"Tried to create documents but received {d.status}: {d.result}")
else:
    logging.error(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)

# ================================
# GET DOCUMENTS
# ================================

existing_documents = alation.document.get_documents(
    query_params = allie.DocumentParams(
        id = created_document_id
    )
)

if existing_documents is None:
    logging.warning("No document was found.")
elif isinstance(existing_documents, list):
    logging.info(f"Found {len(existing_documents)} documents:")
    for d in existing_documents:
        logging.info(f"{d.title}")
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)

# Misc other examples:
# docs = alation.document.get_documents()


# d = alation.document.get_documents(
#     allie.DocumentParams(
#         id = 1309
#     )
# )

# get only specific fields
# d = alation.document.get_documents(
#     allie.DocumentParams(
#         values = 'title,description'
#     )
# )
#


# ================================
# UPDATE DOCUMENTS
# ================================


updated_doc_response = alation.document.update_documents(
    [
        allie.DocumentPutItem(
            id = created_document_id
            , description = "This is another description for KPI 1"
        )
    ]
)

if updated_doc_response[0].status == "successful":
    print(f"Number of documents updated: {updated_doc_response[0].result.updated_term_count}")
    print(f"The following documents were updated (IDs): {updated_doc_response[0].result.updated_terms[0].id}")

# ================================
# DELETE DOCUMENTS
# ================================


delete_document_response = alation.document.delete_documents(
    existing_documents
    # [
    #     allie.Document(
    #         id = 174
    #     )
    # ]
 )

if delete_document_response.status == "successful":
    print(f"Number of documents deleted: {delete_document_response.result.deleted_document_count}")
    print(f"The following documents were deleted (IDs): {delete_document_response.result.deleted_document_ids}")
