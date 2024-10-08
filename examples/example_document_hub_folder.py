"""
Example of creating, listing, updating and deleting one document hub folder.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You created a document hub. Set the DOCUMENT_HUB_ID within the "Set Global Variables" section below.
- The template for the document hub folder has a field called "Status" assigned.
- The "Status" field can be set to values: "Under Review", "Approved".

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

DOCUMENT_HUB_ID = 5

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
# CREATE DOCUMENT HUB FOLDERS
# ================================

create_folder_result = alation.document_hub_folder.create_document_hub_folders(
    [
        allie.DocumentHubFolderPostItem(
            title = 'Test Document Hub Folder'
            , description = 'Test Document Hub Folder'
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

if create_folder_result[0].status == "successful":
    created_folder_id = create_folder_result[0].result.created_folders[0].id
    logging.info(f"Number of folders created: {create_folder_result[0].result.created_folder_count}")
    logging.info(f"The following folders were created (IDs): {created_folder_id}")


# ================================
# GET DOCUMENT HUB FOLDERS
# ================================

existing_folders = alation.document_hub_folder.get_document_hub_folders(
    allie.DocumentHubFolderParams(
        id = created_folder_id
    )
)

if existing_folders:
    logging.info(f"Retrieved folder with id {created_folder_id}.")

# Misc other examples
# folders = alation.document_hub_folder.get_document_hub_folders(
#     allie.DocumentHubFolderParams(
#         document_hub_id = DOCUMENT_HUB_ID
#     )
# )
#
# filtered_dhf = alation.document_hub_folder.get_document_hub_folders(
#     allie.DocumentHubFolderParams(
#         values = 'title, description'
#     )
# )

# ================================
# UPDATE DOCUMENT HUB FOLDERS
# ================================

update_folder_result = alation.document_hub_folder.update_document_hub_folders(
    [
        allie.DocumentHubFolderPutItem(
            id = created_folder_id
            , title = 'Test Document Hub Folder'
            , description = 'Test Document Hub Folder'
            , document_hub_id = DOCUMENT_HUB_ID
            , custom_fields = [
                allie.CustomFieldValueItem(
                    field_id = status_field_id
                    , value = allie.CustomFieldStringValueItem(
                        value = 'Under Review'
                    )
                )
            ]
        )
    ]
)

if update_folder_result[0].status == "successful":
    logging.info(f"Number of folders updated: {update_folder_result[0].result.updated_folder_count}")
    logging.info(f"The following folders were updated (IDs): {update_folder_result[0].result.updated_folders[0].id}")

# ================================
# DELETE DOCUMENT HUB FOLDERS
# ================================

delete_folder_result = alation.document_hub_folder.delete_document_hub_folders(
    document_hub_folders = existing_folders
)

if delete_folder_result.status == "successful":
    logging.info(f"Number of folders deleted: {delete_folder_result.result.deleted_folder_count}")
    logging.info(f"The following folders were deleted (IDs): {delete_folder_result.result.deleted_folder_ids}")
