"""
Example of listing tags, getting tagged objects, tagging an object, updating a tag, and untagging the object.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You have an existing catalog object that can be tagged. Set OBJECT_OTYPE and OBJECT_OID below.
- If you want to test updating an existing tag, make sure the tag already exists in Alation.
"""

import configparser
import logging
import sys
from idlelib.rpc import objecttable

import allie_sdk as allie

# ================================
# Set Global Variables
# ================================

TAG_NAME = "SDK Demo Tag"
UPDATED_TAG_NAME = "SDK Demo Tag Updated"
OBJECT_OTYPE = "glossary_term"
OBJECT_OID = 1

# ================================
# Define Logging Config
# ================================

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ================================
# Source Global Config
# ================================

config = configparser.ConfigParser()
config.read("config.ini")

ALATION_USER_ID = config.get(section="api", option="ALATION_USER_ID")
ALATION_BASE_URL = config.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section="api", option="ALATION_API_REFRESH_TOKEN")

# ================================
# Create session with your Alation instance
# ================================

alation = allie.Alation(
    host=ALATION_BASE_URL,
    user_id=ALATION_USER_ID,
    refresh_token=ALATION_API_REFRESH_TOKEN
)

# ================================
# GET TAGS
# ================================

tags = alation.tag.get_tags(
    # query_params=allie.TagParams(
    #     oid=OBJECT_OID,
    #     otype=OBJECT_OTYPE
    # )
)

logging.info("Retrieved %s existing tag(s)", len(tags))

# ================================
# ADD TAG TO OBJECT
# ================================

tag = alation.tag.add_tag_to_object(
    tag_name=TAG_NAME,
    object=allie.TagObjectItem(
        oid=OBJECT_OID,
        otype=OBJECT_OTYPE
    )
)

logging.info("Tag '%s' now exists with id %s.", tag.name, tag.id)

# ================================
# GET TAGGED OBJECTS
# ================================

objects = alation.tag.get_objects_tagged_with_specific_tag(
    tag_name=TAG_NAME,
    query_params=allie.TaggedObjectParams(order_by="-ts_tagged")
)

logging.info("Retrieved %s tagged object(s) for '%s'.", len(objects), TAG_NAME)

# ================================
# UPDATE TAG
# ================================

updated_tag = alation.tag.update_tag(
    tag_id=tag.id,
    tag=allie.TagItem(
        name=UPDATED_TAG_NAME,
        description="Updated through the Allie SDK example."
    )
)

logging.info("Updated tag %s to '%s'.", updated_tag.id, updated_tag.name)

# ================================
# REMOVE TAG FROM OBJECT
# ================================

delete_result = alation.tag.remove_tag_from_object(
    tag_name=UPDATED_TAG_NAME,
    otype=OBJECT_OTYPE,
    oid=OBJECT_OID
)

if delete_result.status != "successful":
    logging.error("Failed to remove tag from object: %s", delete_result.result)
    sys.exit(1)

logging.info("Removed tag '%s' from %s/%s.", UPDATED_TAG_NAME, OBJECT_OTYPE, OBJECT_OID)
