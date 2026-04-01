"""
Example of intentionally failing when tagging an object with an invalid object type.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
"""

import configparser
import logging
import sys

import allie_sdk as allie

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

config = configparser.ConfigParser()
config.read("config.ini")

ALATION_USER_ID = config.get(section="api", option="ALATION_USER_ID")
ALATION_BASE_URL = config.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section="api", option="ALATION_API_REFRESH_TOKEN")

alation = allie.Alation(
    host=ALATION_BASE_URL,
    user_id=ALATION_USER_ID,
    refresh_token=ALATION_API_REFRESH_TOKEN
)

try:
    alation.tag.add_tag_to_object(
        tag_name="SDK Demo Tag",
        object=allie.TagObjectItem(
            oid=1,
            otype="not_a_valid_otype"
        )
    )
except Exception as exc:
    logging.exception("The Tags API call failed as expected: %s", exc)
