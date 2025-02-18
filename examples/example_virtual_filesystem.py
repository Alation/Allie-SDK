"""
Example of creating and deleting objects within virtual file system.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You created a virtual file system data source in Alation.
- Adjust the FILE_SYSTEM_ID in the "Set Global Variables" section below.
- Note: The delete action performed at the end will delete all objects within this virtual datasource.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

# Note: this is for uploading the technical metadata
# You have to create the Alation virtual data source beforehand
FILE_SYSTEM_ID = 3

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
# CREATE VIRTUAL FILE SYSTEM OBJECTS
# ================================

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

vfs_response = alation.virtual_filesystem.post_metadata(fs_id=FILE_SYSTEM_ID, vfs_objects=[vfs1, vfs2, vfs3, vfs4])

if vfs_response is None:
    logging.error(f"Unable to create objects within virtual datasource.")
    sys.exit(1)
elif isinstance(vfs_response, list):
    for r in vfs_response:
        if r.status == "successful":
            logging.info("Status for creating virtual objects: successful")
        else:
            logging.error(f"Job ended with status {r.status}: {r.result}")
            sys.exit(1)
else:
    logging.error(f"Received unexpected response ... I don't know what to do ...")
    sys.exit(1)


# ================================
# DELETE VIRTUAL OBJECTS
# ================================


# Remove all objects not mentioned
vfs1 = allie.VirtualFileSystemItem(path="/", name="var", is_directory=True)
# All other file objects that are not part of the vfs_objects list will be deleted
vfs_response = alation.virtual_filesystem.post_metadata(fs_id=FILE_SYSTEM_ID, vfs_objects=[vfs1])

# Remove All Objects
vfs_response = alation.virtual_filesystem.post_metadata(fs_id=FILE_SYSTEM_ID, vfs_objects=[])

if vfs_response is None:
    logging.error(f"Unable to delete objects within virtual datasource.")
    sys.exit(1)
elif isinstance(vfs_response, list):
    for r in vfs_response:
        if r.status == "successful":
            logging.info("Status for creating virtual objects: successful")
        else:
            logging.error(f"Job ended with status {r.status}: {r.result}")
            sys.exit(1)
else:
    logging.error(f"Received unexpected response ... I don't know what to do ...")
    sys.exit(1)
