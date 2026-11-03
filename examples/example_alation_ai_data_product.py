"""Examples for every public method in the Alation AI Data Products API.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Replace the data product, BI datasource, dashboard, and optional LookML folder
  IDs below with existing objects in Alation.
- The data product has sample queries and downstream BI assets for metric extraction.
- Your Alation credentials have access to the AI API data product endpoints.
- Optionally set DATA_PRODUCT_CREATION_TASK_ID to an existing asynchronous data
  product creation task ID to run the creation result polling example.

The revision example starts a "Suggest Fixes" workflow for the configured data
product. Revision and metric result getters fetch the current state once; call
them again with the same IDs if the workflow is still running. Creation result
polling waits for final YAML and raises TimeoutError after the configured timeout.
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
BI_DASHBOARD_ID = 99
LOOKML_MODEL_FOLDER_IDS: list[int] = []  # Optional additional BI assets to analyze.
DATA_PRODUCT_CREATION_TASK_ID: str | None = None
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
ALATION_OAUTH_CLIENT_ID = config.get(section="api", option="ALATION_OAUTH_CLIENT_ID", fallback=None)
ALATION_OAUTH_CLIENT_SECRET = config.get(section="api", option="ALATION_OAUTH_CLIENT_SECRET", fallback=None)

# ================================
# Create Session With Your Alation Instance
# ================================

logging.info("Using OAuth client_credentials authentication")
# JWT is created when the Alation object is instantiated, so we can just create the object with the client credentials and it will generate the token automatically
alation = allie.Alation(
    host=ALATION_BASE_URL,
    client_id=ALATION_OAUTH_CLIENT_ID,
    client_secret=ALATION_OAUTH_CLIENT_SECRET,
)

# ================================
# RESOLVE UPSTREAM TABLES FROM A BI OBJECT
# ================================

upstream_tables = alation.alation_ai_data_product.get_upstream_tables_from_bi_object(
    query_params=allie.AlationAIGetUpstreamTablesFromBiObjectParams(
        type="dashboard",
        id=BI_DASHBOARD_ID,
    )
)
for datasource_tables in upstream_tables.datasources:
    logging.info(f"Datasource {datasource_tables.datasource_id} has {len(datasource_tables.tables)} upstream table(s)")
    for table in datasource_tables.tables:
        logging.info(f"Upstream table {table.table_id} uses column IDs {table.column_ids}")

# ================================
# CREATE OR PREVIEW A DATA PRODUCT FROM A BI DATASOURCE
# ================================

bi_datasource_preview = alation.alation_ai_data_product.create_data_product_from_bi_source(
    datasource_id=BI_DATASOURCE_ID,
    create_product=False,
)
logging.info("BI datasource preview:\n%s", bi_datasource_preview.result)

# ================================
# POLL AN EXISTING DATA PRODUCT CREATION TASK FOR FINAL YAML
# ================================

# Creation task IDs are separate from metric extraction task IDs.
if DATA_PRODUCT_CREATION_TASK_ID:
    created_data_product_yaml = alation.alation_ai_data_product.get_data_product_creation_result(
        task_id=DATA_PRODUCT_CREATION_TASK_ID,
        poll_interval_seconds=3,
        timeout_seconds=300,
    )
    logging.info(f"Completed data product creation YAML:\n{created_data_product_yaml}")
else:
    logging.info("Set DATA_PRODUCT_CREATION_TASK_ID to run the creation result polling example")

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

# ================================
# EXTRACT METRICS FROM A DATA PRODUCT'S SAMPLE QUERIES
# ================================

sample_query_metrics_task = alation.alation_ai_data_product.extract_data_product_metrics_from_sample_queries(
    data_product_id=PUBLISHED_DATA_PRODUCT_ID,
)
logging.info(f"Started sample query metric extraction task {sample_query_metrics_task.result.task_id}")

sample_query_metrics_result = alation.alation_ai_data_product.get_data_product_metrics_extraction_result(
    task_id=sample_query_metrics_task.result.task_id,
)
if isinstance(sample_query_metrics_result, allie.AlationAIAsyncTask):
    logging.info(f"Sample query metric extraction task {sample_query_metrics_result.id} is {sample_query_metrics_result.status}")
else:
    logging.info(f"Extracted metrics for {len(sample_query_metrics_result)} sample query statement(s)")

# ================================
# EXTRACT METRICS FROM DOWNSTREAM BI ASSETS
# ================================

bi_metrics_task = alation.alation_ai_data_product.extract_data_product_metrics_from_bi(
    data_product_id=PUBLISHED_DATA_PRODUCT_ID,
    query_params=allie.AlationAIExtractMetricsFromBIParams(
        dashboard_ids=[BI_DASHBOARD_ID],
        lookml_model_folder_ids=LOOKML_MODEL_FOLDER_IDS,
    ),
)
logging.info(f"Started BI metric extraction task {bi_metrics_task.result.task_id}")

# ================================
# FETCH METRICS WITH SOURCE METADATA
# ================================

bi_metrics_result = alation.alation_ai_data_product.get_data_product_metrics_extraction_result_with_source(
    task_id=bi_metrics_task.result.task_id,
)
if isinstance(bi_metrics_result, allie.AlationAIAsyncTask):
    logging.info(f"BI metric extraction task {bi_metrics_result.id} is {bi_metrics_result.status}")
else:
    logging.info(f"Received {len(bi_metrics_result)} BI metric extraction result(s)")
    for metric_result in bi_metrics_result:
        for metric in metric_result.metrics or []:
            logging.info(f"Metric {metric.displayName}: {metric.expression}")
            for source in metric.sources or []:
                logging.info(f"Source {source.source_type}: {source.source_name}; catalog URL: {source.catalog_url}")

# ================================
# START A DATA PRODUCT REVISION WORKFLOW
# ================================

revision_workflow = alation.alation_ai_data_product.initiate_revise_data_product_workflow(
    data_product_id=PUBLISHED_DATA_PRODUCT_ID,
    revise_request=allie.AlationAIReviseDataProductRequest(
        message="Improve metric descriptions and relationships to address SQL evaluation failures, then evaluate the revised data product.",
    ),
)
logging.info(f"Started revision result {revision_workflow.result.result_id} in chat {revision_workflow.result.chat_id}")

# ================================
# LIST DATA PRODUCT REVISION JOBS
# ================================

revision_jobs = alation.alation_ai_data_product.get_data_product_revision_jobs(
    query_params=allie.AlationAIReviseDataProductJobsParams(
        data_product_id=PUBLISHED_DATA_PRODUCT_ID,
        status=["RUNNING", "COMPLETED"],
        limit=20,
        offset=0,
    )
)
logging.info(f"Retrieved {len(revision_jobs.data)} of {revision_jobs.total} matching revision job(s)")
for revision_job in revision_jobs.data:
    logging.info(f"Revision result {revision_job.result_id} for data product {revision_job.data_product_id} is {revision_job.status}")

# ================================
# FETCH A DATA PRODUCT REVISION RESULT
# ================================

revision_result = alation.alation_ai_data_product.get_data_product_revision_result(
    result_id=revision_workflow.result.result_id,
)
logging.info(f"Revision result {revision_result.result_id} is {revision_result.status}")
logging.info(f"Revision summary: {revision_result.summary}")
if revision_result.final_data_product_yaml:
    logging.info(f"Revised data product YAML:\n{revision_result.final_data_product_yaml}")
