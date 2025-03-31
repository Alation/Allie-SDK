"""
Example of creating, listing, updating and deleting one visual config.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Adjust the variable values in the below "Set Global Variables" section.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

# the id for the document hub that we assign the visual config to
DOCUMENT_HUB_ID = 2
# IDs of custom fields that you want to add to the visual config
FIRST_CUSTOM_FIELD_ID=10011
SECOND_CUSTOM_FIELD_ID=10012

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
# CREATE VISUAL CONFIG
# ================================

create_response = alation.visual_config.create_visual_config(
    visual_config = allie.VisualConfigItem(
        collection_type_id = DOCUMENT_HUB_ID
        , title='Data Product'
        , layout_otype='glossary_term'
        , component_list_in_config=[
            allie.VisualConfigComponent(
                rendered_otype='CUSTOM_FIELD'
                , rendered_oid=4
                , page_defined_type=None
                , component_type='BUILT_IN'
                , panel='MAIN'
            )
            , allie.VisualGroupedComponent(
                label='Data Product Info'
                , open_by_default=True
                , panel='MAIN'
                , is_group=True
                , components=[
                    allie.VisualConfigComponent(
                        rendered_otype='CUSTOM_FIELD'
                        , rendered_oid=FIRST_CUSTOM_FIELD_ID
                        , page_defined_type=None
                        , component_type='USER_DEFINED'
                        , panel='MAIN'
                    )
                    , allie.VisualConfigComponent(
                        rendered_otype='CUSTOM_FIELD'
                        , rendered_oid=SECOND_CUSTOM_FIELD_ID
                        , page_defined_type=None
                        , component_type='USER_DEFINED'
                        , panel='MAIN'
                    )
                ]
            )
            , allie.VisualGroupedComponent(
                label='Owners'
                , open_by_default=True
                , panel='SIDEBAR'
                , is_group=True
                , components=[
                    allie.VisualConfigComponent(
                        rendered_otype='CUSTOM_FIELD'
                        , rendered_oid=8
                        , page_defined_type=None
                        , component_type='BUILT_IN'
                        , panel='SIDEBAR'
                    )
                ]
            )
        ]
    )
)

if create_response is None:
    logging.error("Tried to create visual config but got no response ...")
    sys.exit(1)
elif isinstance(create_response, allie.JobDetails):
    if create_response.status == "successful":
        my_visual_config = create_response.result
        logging.info(f"Successfully created Visual Config '{my_visual_config.title}' with id: {my_visual_config.id}")
    else:
        logging.error(f"Failed execution. Additional info: {create_response.result}")
        sys.exit(1)
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)

# ================================
# GET VISUAL CONFIGS
# ================================

existing_visual_configs = alation.visual_config.get_visual_configs()

if existing_visual_configs is None:
    logging.warning("No visual config was found.")
elif isinstance(existing_visual_configs, list):
    logging.info(f"Found {len(existing_visual_configs)} visual configs:")
    for d in existing_visual_configs:
        logging.info(f"{d.title}")
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)

# ================================
# GET VISUAL CONFIGS BY OBJECT TYPE
# ================================

existing_visual_configs = alation.visual_config.get_visual_configs(
    otype = "glossary_term"
)

if existing_visual_configs is None:
    logging.warning("No visual config was found.")
elif isinstance(existing_visual_configs, list):
    logging.info(f"Found {len(existing_visual_configs)} visual configs:")
    for d in existing_visual_configs:
        logging.info(f"{d.title}")
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)

# ================================
# GET A VISUAL CONFIG
# ================================

existing_visual_configs = alation.visual_config.get_a_visual_config(
    visual_config_id = my_visual_config.id
)

if existing_visual_configs is None:
    logging.warning("No visual config was found.")
elif isinstance(existing_visual_configs, allie.VisualConfig):
    logging.info(f"Found visual config: {existing_visual_configs.title} ")
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)


# ================================
# UPDATE A VISUAL CONFIG
# ================================

update_response = alation.visual_config.update_visual_config(
    visual_config = allie.VisualConfigItem(
        collection_type_id = DOCUMENT_HUB_ID # Note: Currently collection type id is not supported for updates
        , title='Data Product UPDATED'
        , layout_otype='glossary_term'
        , component_list_in_config=[
            allie.VisualConfigComponent(
                rendered_otype='CUSTOM_FIELD'
                , rendered_oid=4
                , page_defined_type=None
                , component_type='BUILT_IN'
                , panel='MAIN'
            )
            , allie.VisualGroupedComponent(
                label='Data Product Info'
                , open_by_default=True
                , panel='MAIN'
                , is_group=True
                , components=[
                    allie.VisualConfigComponent(
                        rendered_otype='CUSTOM_FIELD'
                        , rendered_oid=FIRST_CUSTOM_FIELD_ID
                        , page_defined_type=None
                        , component_type='USER_DEFINED'
                        , panel='MAIN'
                    )
                    , allie.VisualConfigComponent(
                        rendered_otype='CUSTOM_FIELD'
                        , rendered_oid=SECOND_CUSTOM_FIELD_ID
                        , page_defined_type=None
                        , component_type='USER_DEFINED'
                        , panel='MAIN'
                    )
                ]
            )
            , allie.VisualGroupedComponent(
                label='Owners'
                , open_by_default=True
                , panel='SIDEBAR'
                , is_group=True
                , components=[
                    allie.VisualConfigComponent(
                        rendered_otype='CUSTOM_FIELD'
                        , rendered_oid=8
                        , page_defined_type=None
                        , component_type='BUILT_IN'
                        , panel='SIDEBAR'
                    )
                ]
            )
        ]
    )
    , visual_config_id = my_visual_config.id
)

if update_response is None:
    logging.error("Tried to update visual config but got no response ...")
    sys.exit(1)
elif isinstance(update_response, allie.JobDetails):
    if update_response.status == "successful":
        logging.info(f"Successfully updated Visual Config '{my_visual_config.title}' with id: {my_visual_config.id}")
    else:
        logging.error(f"Failed execution. Additional info: {update_response.result}")
        sys.exit(1)
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)


# ================================
# DELETE A VISUAL CONFIG
# ================================

# Note: Currently visual configs cannot be deleted for documents and document folders.

delete_response = alation.visual_config.delete_visual_config(
    visual_config_id = my_visual_config.id
)

if delete_response is None:
    logging.error("Tried to delete visual config but got no response ...")
    sys.exit(1)
elif isinstance(update_response, allie.JobDetails):
    if update_response.status == "successful":
        logging.info(f"Successfully deleted Visual Config")
    else:
        logging.error(f"Failed execution. Additional info: {update_response.result}")
        sys.exit(1)
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)