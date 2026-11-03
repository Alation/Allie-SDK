"""Example of working with Alation AI Data Products.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- The published data product and BI datasource IDs below already exist in Alation.
- Your Alation credentials have access to the AI API data product endpoints.
"""

import configparser
import logging
import sys

import allie_sdk as allie

# ================================
# Set Global Variables
# ================================

PUBLISHED_DATA_PRODUCT_ID = "customer-orders-redshift-provisioned"
BI_DATASOURCE_ID = 1
SQL_STATEMENTS = [
    "SELECT COUNT(*) AS cnt_customers FROM customersx",
]

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


ALATION_BASE_URL = config.get(section="api", option="ALATION_BASE_URL")
ALATION_OAUTH_CLIENT_ID = config.get(section = "api", option = "ALATION_OAUTH_CLIENT_ID", fallback=None)
ALATION_OAUTH_CLIENT_SECRET = config.get(section = "api", option = "ALATION_OAUTH_CLIENT_SECRET", fallback=None)

# ================================
# Create Session With Your Alation Instance
# ================================

logging.info("Using OAuth client_credentials authentication")
# JWT is created when the Alation object is instantiated, so we can just create the object with the client credentials and it will generate the token automatically
alation = allie.Alation(
    host = ALATION_BASE_URL
    , client_id = ALATION_OAUTH_CLIENT_ID
    , client_secret = ALATION_OAUTH_CLIENT_SECRET,
)

# ================================
# CREATE OR PREVIEW A DATA PRODUCT FROM A BI DATASOURCE
# ================================

bi_datasource_preview = alation.alation_ai_data_product.create_data_product_from_bi_source(
    datasource_id=BI_DATASOURCE_ID,
    create_product=False,
)
logging.info("BI datasource preview:\n%s", bi_datasource_preview.result)

# ================================
# GENERATE RELATIONSHIPS FROM THE YAML SPEC
# ================================

generated_relationships = alation.alation_ai_data_product.generate_relationships(
    allie.AlationAIGenerateRelationshipsRequest(
        data_product_spec_yaml=bi_datasource_preview.result,
    )
)
logging.info("Generated %s relationship(s)", len(generated_relationships.result.relationships))

# ================================
# VALIDATE SQL AGAINST A DATA PRODUCT
# ================================

validated_sql = alation.alation_ai_data_product.validate_sql(
    PUBLISHED_DATA_PRODUCT_ID,
    SQL_STATEMENTS,
)
logging.info(f"Validated {len(validated_sql.result)} SQL statement(s)")

# ================================
# EXTRACT METRICS FROM SQL STATEMENTS
# ================================

metrics_task = alation.alation_ai_data_product.extract_metrics_from_sql_statements(
    PUBLISHED_DATA_PRODUCT_ID,
    SQL_STATEMENTS,
)
logging.info("Started metric extraction task %s", metrics_task.result.task_id)

metrics_result = alation.alation_ai_data_product.get_data_product_metrics_extraction_result(metrics_task.result.task_id)
if isinstance(metrics_result, allie.AlationAIAsyncTask):
    logging.info("Metric extraction task %s is %s", metrics_result.id, metrics_result.status)
else:
    logging.info("Extracted metrics for %s SQL statement(s)", len(metrics_result))
