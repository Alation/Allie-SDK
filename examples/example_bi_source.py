"""
Example of creating, listing, updating and deleting one bi source.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- ... OPEN ...

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
# GET BI SERVERS
# ================================

existing_bi_servers = alation.bi_source.get_bi_servers()


if existing_bi_servers is None:
    logging.warning("No BI Server was found.")
elif isinstance(existing_bi_servers, list):
    logging.info(f"Found {len(existing_bi_servers)} BI Servers:")
    for d in existing_bi_servers:
        logging.info(f"{d.title}")
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)

# ================================
# GET ONE BI SERVER
# ================================

existing_bi_servers = alation.bi_source.get_bi_servers(
    query_params = allie.BIServerParams(
        oids=[1]
    )
)

if existing_bi_servers is None:
    logging.warning("No BI Server was found.")
elif isinstance(existing_bi_servers, list):
    logging.info(f"Found {len(existing_bi_servers)} BI Servers:")
    for d in existing_bi_servers:
        logging.info(f"{d.title}")
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)