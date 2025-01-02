"""
Example of the post request failing because of invalid data source id

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Set the variables in the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser
import datetime

# ================================
# Set Global Variables
# ================================

# MAKE IT FAIL: Use invalid data source id
DATA_SOURCE_ID = 0

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
# CREATE VIRTUAL DATA SOURCE OBJECTS WITHIN EXISTING DATA SOURCE
# ================================

"""
MAKE IT FAIL

- use invalid data source id
"""

# Note this is for uploading the technical metadata
# You have to create the Alation virtual data source beforehand
fs_id = DATA_SOURCE_ID

# Add/Update Objects

vfs1 = allie.VirtualFileSystemItem(
    path="/"
    , name="var"
    , is_directory=True
)
vfs2 = allie.VirtualFileSystemItem(
    path="/var"
    , name="log"
    , is_directory=True
)
vfs3 = allie.VirtualFileSystemItem(
    path="/var"
    , name="File 2"
    , is_directory=False
)
vfs4 = allie.VirtualFileSystemItem(
    path="/var/log"
    , name="boot.log"
    , is_directory=False
    , size_in_bytes=98800
    , ts_last_modified="2024-06-20T18:26:54.663432Z"
    , ts_last_accessed="2024-06-20T18:26:54.663432Z"
    , owner="root"
    , group="root"
    , permission_bits=755
)

vfs_response = alation.virtual_filesystem.post_metadata(fs_id=fs_id, vfs_objects=[vfs1, vfs2, vfs3, vfs4])

print()

"""
expected response:

[JobDetails(status='failed', msg=None, result={'error': 'Cannot find FileSystem id: 0'})]

expected logging message:

2025-01-02 11:26:02,332 - ERROR - ERROR MESSAGE: Error submitting the POST Request to: //api/v1/bulk_metadata/file_upload/0/
ERROR: {'error': 'Cannot find FileSystem id: 0'}

"""