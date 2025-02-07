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

# specify the document hub id
DOCUMENT_HUB_ID = 4

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
        name_singular = 'Description'
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

create_folder_response = alation.document_hub_folder.create_document_hub_folders(
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


if create_folder_response is None:
    logging.error("Tried to create doc hub folder but somehow got no feedback ...")
    sys.exit(1)
elif isinstance(create_folder_response, list):
    for r in create_folder_response:
        if r.status == "successful":
            created_folder_id = create_folder_response[0].result.created_folders[0].id
            logging.info(f"Number of folders created: {create_folder_response[0].result.created_folder_count}")
            logging.info(f"The following folders were created (IDs): {created_folder_id}")
        else:
            logging.info(f"Something went wrong while creating folder: {r.result}")
            sys.exit(1)
else:
    logging.error(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)


# ================================
# GET DOCUMENT HUB FOLDERS
# ================================

existing_folders = alation.document_hub_folder.get_document_hub_folders(
    allie.DocumentHubFolderParams(
        id = created_folder_id
    )
)

if existing_folders is None:
    logging.warning(f"No existing document hub folder was found with id {created_folder_id}.")
elif isinstance(existing_folders, list):
    logging.info(f"Retrieved folder(s):")
    for f in existing_folders:
        logging.info(f.title)
else:
    logging.error(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)

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

update_folder_response = alation.document_hub_folder.update_document_hub_folders(
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

if update_folder_response is None:
    logging.error("Tried to update doc hub folder but somehow got no feedback ...")
elif isinstance(update_folder_response, list):
    for f in update_folder_response:
        if f.status == "successful":
            logging.info(f"Number of folders updated: {update_folder_response[0].result.updated_folder_count}")
            logging.info(f"The following folders were updated (IDs): {update_folder_response[0].result.updated_folders[0].id}")
        else:
            logging.error(f"Something went wrong while updating folder: {f.result}")
            sys.exit(1)
else:
    logging.error(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)

# ================================
# DELETE DOCUMENT HUB FOLDERS
# ================================

delete_folder_response = alation.document_hub_folder.delete_document_hub_folders(
    document_hub_folders = existing_folders
)

if delete_folder_response is None:
    logging.error("Tried to delete doc hub folder but somehow got no feedback ...")
    sys.exit(1)
elif isinstance(delete_folder_response, allie.JobDetailsDocumentHubFolderDelete):
    if delete_folder_response.status == "successful":
        logging.info(f"Number of folders deleted: {delete_folder_response.result.deleted_folder_count}")
        logging.info(f"The following folders were deleted (IDs): {delete_folder_response.result.deleted_folder_ids}")
    else:
        logging.error("Something went wrong while deleting doc hub folder: {delete_folder_response.result}")
        sys.exit(1)
else:
    logging.error(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)
