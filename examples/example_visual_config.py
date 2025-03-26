"""
Example of creating, listing, updating and deleting one visual config.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- ...

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================



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
        collection_type_id = 2
        , title='Data Product'
        , layout_otype='glossary_term'
        , component_list_in_config=[
            allie.VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                  page_defined_type='catalog_document.document_children', component_type='PAGE_DEFINED',
                                  panel='SIDEBAR')
            , allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=4, page_defined_type=None,
                                    component_type='BUILT_IN', panel='MAIN')
            , allie.VisualGroupedComponent(label='Data Product Info', open_by_default=True, panel='MAIN', is_group=True,
                                     components=[
                                         allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10011,
                                                               page_defined_type=None, component_type='USER_DEFINED',
                                                               panel='MAIN')
                                         , allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10012,
                                                                 page_defined_type=None, component_type='USER_DEFINED',
                                                                 panel='MAIN')
                                         , allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10013,
                                                                 page_defined_type=None, component_type='USER_DEFINED',
                                                                 panel='MAIN')
                                         , allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10014,
                                                                 page_defined_type=None, component_type='USER_DEFINED',
                                                                 panel='MAIN')
                                         , allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10015,
                                                                 page_defined_type=None, component_type='USER_DEFINED',
                                                                 panel='MAIN')
                                     ]
                                     )
            , allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10017, page_defined_type=None,
                                    component_type='USER_DEFINED', panel='MAIN')
            , allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10016, page_defined_type=None,
                                    component_type='USER_DEFINED', panel='MAIN')
            , allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10018, page_defined_type=None,
                                    component_type='USER_DEFINED', panel='MAIN')
            , allie.VisualGroupedComponent(label='Owners', open_by_default=True, panel='SIDEBAR', is_group=True, components=[
                allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10019, page_defined_type=None,
                                      component_type='USER_DEFINED', panel='SIDEBAR')
                , allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10020, page_defined_type=None,
                                        component_type='USER_DEFINED', panel='SIDEBAR')
                , allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=8, page_defined_type=None,
                                        component_type='BUILT_IN', panel='SIDEBAR')
            ]
                                     )
            , allie.VisualConfigComponent(rendered_otype='CUSTOM_FIELD', rendered_oid=10021, page_defined_type=None,
                                    component_type='USER_DEFINED', panel='SIDEBAR')
            , allie.VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                    page_defined_type='catalog.membership_to_domains', component_type='PAGE_DEFINED',
                                    panel='SIDEBAR')
            , allie.VisualConfigComponent(rendered_otype=None, rendered_oid=None, page_defined_type='catalog.tags',
                                    component_type='PAGE_DEFINED', panel='SIDEBAR')
            , allie.VisualGroupedComponent(label='Referenced By', open_by_default=True, panel='SIDEBAR', is_group=True,
                                     components=[
                                         allie.VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                                               page_defined_type='catalog.mentioned_on',
                                                               component_type='PAGE_DEFINED', panel='SIDEBAR')
                                         , allie.VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                                                 page_defined_type='catalog.article_backreferences',
                                                                 component_type='PAGE_DEFINED', panel='SIDEBAR')
                                         , allie.VisualConfigComponent(rendered_otype=None, rendered_oid=None,
                                                                 page_defined_type='catalog.objectset_backreferences',
                                                                 component_type='PAGE_DEFINED', panel='SIDEBAR')
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
        logging.info(f"Successful execution Visual Config '{create_response.title}' with id: {create_response.id}")
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
# GET A VISUAL CONFIG
# ================================

existing_visual_configs = alation.visual_config.get_a_visual_config(
    visual_config_id = 37
)

if existing_visual_configs is None:
    logging.warning("No visual config was found.")
elif isinstance(existing_visual_configs, allie.VisualConfig):
    logging.info(f"Found visual config: {existing_visual_configs.title} ")
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)