"""Example of working with Alation AI Data Products.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- The table and column IDs below already exist in Alation.
- Your Alation credentials have access to the AI API data product endpoints.
"""

import configparser
import logging
import sys

import allie_sdk as allie


# ================================
# Set Global Variables
# ================================

TABLE_A_ID = 311
TABLE_B_ID = 312
ALATION_AI_DATA_PRODUCT_ID = "replace with created data product name"
EXISTING_DATA_PRODUCT_YAML = None
BI_DATASOURCE_ID = 5
SQL_STATEMENTS = [
    "SELECT SUM(revenue) AS total_revenue FROM sales.orders",
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
# GET TABLE AND COLUMN IDS
# ================================

table_a_columns = alation.rdbms.get_columns(
    allie.ColumnParams(
        table_id = TABLE_A_ID
    )
)

TABLE_A_COLUMN_IDS = [ c.id for c in table_a_columns ]

table_b_columns = alation.rdbms.get_columns(
    allie.ColumnParams(
        table_id = TABLE_B_ID
    )
)

TABLE_B_COLUMN_IDS = [ c.id for c in table_b_columns ]

# ================================
# CREATE DATA PRODUCT
# ================================

creation_request = allie.AlationAIDataProductCreationInfo(
    table_column_info_list=[
        allie.AlationAIDataProductTableColumnInfo(
            table_id=TABLE_A_ID,
            column_ids=TABLE_A_COLUMN_IDS,
        ),
        allie.AlationAIDataProductTableColumnInfo(
            table_id=TABLE_B_ID,
            column_ids=TABLE_B_COLUMN_IDS,
        )
    ],
    existing_data_product=EXISTING_DATA_PRODUCT_YAML,
)

creation_task = alation.alation_ai_data_product.create_data_product(
    alation_ai_data_product=creation_request,
    generate_missing_descriptions=True,
    generate_relationships=True
)
logging.info(f"Started data product creation task {creation_task.task_id}")

# ================================
# WAIT FOR FINAL DATA PRODUCT YAML
# ================================

data_product_result = alation.alation_ai_data_product.get_data_product_task(creation_task.task_id)
logging.info(f"Data product YAML:\n{data_product_result}")

# ================================
# VALIDATE SQL AGAINST A DATA PRODUCT
# ================================

validated_sql = alation.alation_ai_data_product.validate_data_product_sql(
    ALATION_AI_DATA_PRODUCT_ID,
    SQL_STATEMENTS,
)
logging.info(f"Validated {len(validated_sql)} SQL statement(s)")

# ================================
# EXTRACT METRICS FROM SQL
# ================================

metrics_task = alation.alation_ai_data_product.extract_data_product_metrics(
    ALATION_AI_DATA_PRODUCT_ID,
    SQL_STATEMENTS,
)
logging.info("Started metric extraction task %s", metrics_task.task_id)

metrics_result = alation.alation_ai_data_product.get_data_product_metrics(metrics_task.task_id)
if isinstance(metrics_result, allie.AlationAIAsyncTask):
    logging.info("Metric extraction task %s is %s", metrics_result.id, metrics_result.status)
else:
    logging.info("Extracted metrics for %s SQL statement(s)", len(metrics_result))

# ================================
# CREATE OR PREVIEW A DATA PRODUCT FROM A BI DATASOURCE
# ================================

bi_datasource_preview = alation.alation_ai_data_product.create_data_product_from_bi_datasource(
    datasource_id=BI_DATASOURCE_ID,
    create_product=False,
)
logging.info("BI datasource preview:\n%s", bi_datasource_preview)
