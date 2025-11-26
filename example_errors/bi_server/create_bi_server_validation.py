"""
Example of the post request failing because of missing URI in payload

Prerequisites:

- You adjusted the "config.ini" file with your settings.

"""

import allie_sdk as allie
import logging
import sys
import configparser
import datetime

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
# CREATE BI SERVER
# ================================

created_bi_servers = alation.bi_source.create_bi_servers(
    [
        allie.BIServerItem(
            uri = "", # <= missing URI should cause error
            title = "BI Server Test",
            description = "BI Server Test",
            name_configuration = allie.BIServerNameConfiguration(
                bi_report = "BI Report"
                , bi_datasource = "BI Data Source"
                , bi_folder = "BI Folder"
                , bi_connection = "BI Connection"
            )
        )
    ]
)


print()

"""
Expected response:

JobDetailsBIServerPost(status='failed', msg=None, result={'detail': 'Unable to create BI servers', 'errors': ['Problem creating/updating virtual bi configuration parameters'], 'code': '400002'})
"""