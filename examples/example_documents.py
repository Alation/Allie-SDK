"""
Example of creating, listing, updating and deleting one document.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You created a document hub. Set the DOCUMENT_HUB_ID within the "Set Global Variables" section below.
- The template for the document hub folder has a field called "Status" assigned.
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

DOCUMENT_HUB_ID = 5
DOCUMENT_TEMPLATE_NAME = "DS Document"

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


if len(templates) > 1:
    logging.error(f"More than one document template with the name {DOCUMENT_TEMPLATE_NAME} found.")
    logging.error("How to resolve: Make sure the template name is unique!")
    sys.exit(1)
else:
    my_template_id = templates[0].id

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


# get random folder
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

create_document_result = alation.document.create_documents(
    [
        allie.DocumentPostItem(
            title = "My KPI 1x1"
            , description = "This is the description for KPI 1"
            , template_id = my_template_id
            , folder_ids = [ random_folder_id ]
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

if create_document_result[0].status == "successful":
    created_document_id = create_document_result[0].result.created_terms[0].id
    print(f"Number of documents created: {create_document_result[0].result.created_term_count}")
    print(f"The following documents were created (IDs): {created_document_id}")

# ================================
# GET DOCUMENTS
# ================================

existing_documents = alation.document.get_documents(
    query_params = allie.DocumentParams(
        id = created_document_id
    )
)

if existing_documents:
    print(f"Retrieved document with id {created_document_id}.")

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


updated_doc_result = alation.document.update_documents(
    [
        allie.DocumentPutItem(
            id = created_document_id
            , description = "This is another description for KPI 1"
        )
    ]
)

if updated_doc_result[0].status == "successful":
    print(f"Number of documents updated: {updated_doc_result[0].result.updated_term_count}")
    print(f"The following documents were updated (IDs): {updated_doc_result[0].result.updated_terms[0].id}")

# ================================
# DELETE DOCUMENTS
# ================================


delete_document_result = alation.document.delete_documents(
    existing_documents
    # [
    #     allie.Document(
    #         id = 174
    #     )
    # ]
 )

if delete_document_result.status == "successful":
    print(f"Number of documents deleted: {delete_document_result.result.deleted_document_count}")
    print(f"The following documents were deleted (IDs): {delete_document_result.result.deleted_document_ids}")
