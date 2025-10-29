"""Example of creating a query and downloading its SQL text.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- The datasource ID used below already exists in Alation.
"""

import configparser
import logging
import sys

import allie_sdk as allie
from allie_sdk.models import QueryParams

# ================================
# Set Global Variables
# ================================

DATASOURCE_ID = 1
QUERY_TITLE = "Top 10 Users"
QUERY_DESCRIPTION = "Counts the number of users and lists the top 10 users."
QUERY_SQL = "SELECT count(*) FROM users;\nSELECT TOP 10 * FROM users;"
QUERY_TAGS = ["demo"]
QUERY_DOMAIN_IDS = [1]
AUTHOR_EMAIL = "user@example.com"

# ================================
# Define Logging Config
# ================================

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(message)s",
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
    refresh_token=ALATION_API_REFRESH_TOKEN,
)

# ================================
# CREATE QUERY
# ================================

query_request = allie.QueryItem(
    datasource_id=DATASOURCE_ID,
    content=QUERY_SQL,
    title=QUERY_TITLE,
    description=QUERY_DESCRIPTION,
    tag_names=QUERY_TAGS,
    domain_ids=QUERY_DOMAIN_IDS,
    author=allie.QueryAuthor(email=AUTHOR_EMAIL),
    published=True,
)

created_query = alation.query.create_query(query_request)

logging.info("Created query %s (id=%s)", created_query.result.title, created_query.result.id)

# ================================
# GET QUERIES
# ================================

queries = alation.query.get_queries(
    query_params = QueryParams(
        datasource_id=DATASOURCE_ID
    )
)

logging.info(f"I found {len(queries)} queries")

# ================================
# GET SPECIFIC QUERY BY ID
# ================================

query = alation.query.get_query(
    query_id = created_query.result.id
)

logging.info("Query %s (id=%s)", query.title, query.id)

# ================================
# GET QUERY SQL
# ================================

query = alation.query.get_query_sql(
    query_id = created_query.result.id
)

logging.info("Downloaded SQL for query id=%s", created_query.result.id)
logging.debug("SQL contents:\n%s", query)
