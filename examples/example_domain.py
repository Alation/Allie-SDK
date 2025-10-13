"""
Example of listing domains and assigning object to a given domain.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- You created at least one domain via the UI.
- Set the variables in the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================

# specify the domain name - should be a unique name
DOMAIN_NAME = "HR"
# ids of objects to be assigned to domain id mentioned above
DOMAIN_ASSIGNMENT_OBJECT_IDS = [1,2,3]
# object type of the objects that should be assigned to the domain mentioned above
DOMAIN_ASSIGNMENT_OBJECT_TYPE = "table"

# Optional filters used when viewing domain membership rules.
DOMAIN_RULES_EXCLUDE = False
DOMAIN_RULES_RECURSIVE = None  # Set to True/False to filter by recursive rules

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
# CREATE DOMAIN
# ================================

# Currently not supported by Allie-SDK

# ================================
# FETCH DOMAINS
# ================================

domain_id:int

domains = alation.domain.get_domains()

if domains is None:
    logging.error("No domains found!")
    sys.exit(1)
elif isinstance(domains, list):
    logging.info("Successfully fetched domains")
    for d in domains:
        if d.title == DOMAIN_NAME:
            domain_id = d.id
else:
    logging.error("Unexpected result ... I don't know what to do")
    sys.exit(1)

# ================================
# ASSIGN OBJECTS TO DOMAINS
# ================================

if domain_id:
    result = alation.domain.assign_objects_to_domain(
        allie.DomainMembership(
            id = domain_id
            , oid = DOMAIN_ASSIGNMENT_OBJECT_IDS
            , otype = DOMAIN_ASSIGNMENT_OBJECT_TYPE
        )
    )

    if result is None:
        logging.error("Unable to assign objects to domain")
        sys.exit(1)
    elif isinstance(result, list):
        for r in result:
            if r.status == "successful":
                logging.info("Successfully assigned objects to domain.")
            else:
                logging.error("Unable to assign objects to domain")
    else:
        logging.info("Unexpected result ... I don't know what to do")
        sys.exit(1)

    # ================================
    # VIEW DOMAIN MEMBERSHIP RULES
    # ================================

    rules_request = allie.DomainMembershipRuleRequest(
        domain_ids=[domain_id],
        exclude=DOMAIN_RULES_EXCLUDE,
        recursive=DOMAIN_RULES_RECURSIVE,
    )

    rules = alation.domain.get_domain_membership_rules(rules_request)

    if not rules:
        logging.info("No membership rules matched the supplied filters.")
    else:
        logging.info("Membership rules found:")
        for rule in rules:
            logging.info(
                "Domain %s applies to otype '%s' (oid=%s), exclude=%s, recursive=%s",
                rule.domain_id,
                rule.otype,
                rule.oid,
                rule.exclude,
                rule.recursive,
            )
