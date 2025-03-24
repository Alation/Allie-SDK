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
    visual_config_id = 1
)

if existing_visual_configs is None:
    logging.warning("No visual config was found.")
elif isinstance(existing_visual_configs, allie.VisualConfig):
    logging.info(f"Found visual config: {existing_visual_configs.title} ")
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)