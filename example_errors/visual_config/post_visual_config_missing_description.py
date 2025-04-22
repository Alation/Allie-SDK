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
config.read("./../config.ini")

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
            # We purposely omit the description
            # allie.VisualConfigComponent(
            #     rendered_otype='CUSTOM_FIELD'
            #     , rendered_oid=4
            #     , page_defined_type=None
            #     , component_type='BUILT_IN'
            #     , panel='MAIN'
            # )
            allie.VisualGroupedComponent(
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

"""
Expected error:
{'detail': 'No default custom fields(4,8) in the request', 'code': '400000'}
"""

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

