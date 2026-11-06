"""Examples for every public method in the Alation AI Data Products API.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Enable individual examples in ``[alation_ai_data_product_examples]`` using
  the switches in config.ini.sample, which are all disabled initially.
- Replace the data product, BI datasource, dashboard, and optional LookML folder
  IDs below with existing objects in Alation.
- The data product has sample queries and downstream BI assets for metric extraction.
- Your Alation credentials have access to the AI API data product endpoints.
- Set DATA_PRODUCT_CREATION_TASK_ID to an existing asynchronous data product
  creation task ID to run the creation result polling example.
- Relationship generation uses the BI datasource preview, or DATA_PRODUCT_SPEC_YAML
  when the preview example is disabled.
- BI metric and revision result examples use IDs returned by the corresponding
  start examples, or BI_METRICS_TASK_ID and DATA_PRODUCT_REVISION_RESULT_ID
  when those start examples are disabled.

The revision example starts a "Suggest Fixes" workflow for the configured data
product. Revision and metric result getters fetch the current state once; call
them again with the same IDs if the workflow is still running. Creation result
polling waits for final YAML and raises TimeoutError after the configured timeout.
"""

import configparser
import logging
import sys
from dataclasses import asdict
from yaml import safe_dump
import allie_sdk as allie

# ================================
# Set Global Variables
# ================================

PUBLISHED_DATA_PRODUCT_ID = "customer-orders-redshift-provisioned"
BI_DATASOURCE_ID = 1 # "ACME Bank Reporting"
BI_DASHBOARD_ID = 50 # "Advisor AUM Dashboard"
LOOKML_MODEL_FOLDER_IDS: list[int] = []  # Optional additional BI assets to analyze.
DATA_PRODUCT_CREATION_TASK_ID: str | None = None
DATA_PRODUCT_SPEC: str | None = None
BI_METRICS_TASK_ID: str | None = None
DATA_PRODUCT_REVISION_RESULT_ID: str | None = None
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

example_switches = config["alation_ai_data_product_examples"]


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

if example_switches.getboolean("RESOLVE_UPSTREAM_TABLES_FROM_BI_OBJECT"):
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

if example_switches.getboolean("CREATE_OR_PREVIEW_DATA_PRODUCT_FROM_BI_DATASOURCE"):
    bi_datasource_preview = alation.alation_ai_data_product.create_data_product_from_bi_source(
        datasource_id=BI_DATASOURCE_ID,
        create_product=False,
    )
    DATA_PRODUCT_SPEC = bi_datasource_preview.result
    logging.info(f"BI datasource preview:\n{bi_datasource_preview.result}")

# ================================
# GENERATE RELATIONSHIPS FROM THE YAML SPEC
# ================================

if example_switches.getboolean("GENERATE_RELATIONSHIPS"):
    if not DATA_PRODUCT_SPEC:
        error_message = "Enable CREATE_OR_PREVIEW_DATA_PRODUCT_FROM_BI_DATASOURCE"
        logging.error(error_message)
        raise ValueError(error_message)
    data_product_spec_dict = asdict(DATA_PRODUCT_SPEC)
    data_product_spec_yaml = safe_dump(data_product_spec_dict)
    generated_relationships = alation.alation_ai_data_product.generate_relationships(
        allie.AlationAIGenerateRelationshipsRequest(
            data_product_spec_yaml=data_product_spec_yaml,
        )
    )
    logging.info(f"Generated {len(generated_relationships.result.relationships)} relationship(s)")

# ================================
# VALIDATE SQL AGAINST A DATA PRODUCT
# ================================

if example_switches.getboolean("VALIDATE_SQL"):
    validated_sql = alation.alation_ai_data_product.validate_sql(
        PUBLISHED_DATA_PRODUCT_ID,
        SQL_STATEMENTS,
    )
    logging.info(f"Validated {len(validated_sql.result)} SQL statement(s)")

# ================================
# EXTRACT METRICS FROM SQL STATEMENTS
# ================================

if example_switches.getboolean("EXTRACT_METRICS_FROM_SQL_STATEMENTS"):
    metrics_task = alation.alation_ai_data_product.extract_metrics_from_sql_statements(
        PUBLISHED_DATA_PRODUCT_ID,
        SQL_STATEMENTS,
    )
    logging.info(f"Started metric extraction task {metrics_task.result.task_id}")

    metrics_result = alation.alation_ai_data_product.get_data_product_metrics_extraction_result(metrics_task.result.task_id)
    if isinstance(metrics_result, allie.AlationAIAsyncTask):
        logging.info(f"Metric extraction task {metrics_result.id} is {metrics_result.status}")
    else:
        logging.info(f"Extracted metrics for {len(metrics_result)} SQL statement(s)")

# ================================
# EXTRACT METRICS FROM A DATA PRODUCT'S SAMPLE QUERIES
# ================================

if example_switches.getboolean("EXTRACT_METRICS_FROM_SAMPLE_QUERIES"):
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

if example_switches.getboolean("EXTRACT_METRICS_FROM_DOWNSTREAM_BI_ASSETS"):
    bi_metrics_task = alation.alation_ai_data_product.extract_data_product_metrics_from_bi(
        data_product_id=PUBLISHED_DATA_PRODUCT_ID,
        query_params=allie.AlationAIExtractMetricsFromBIParams(
            dashboard_ids=[BI_DASHBOARD_ID],
            lookml_model_folder_ids=LOOKML_MODEL_FOLDER_IDS,
        ),
    )
    BI_METRICS_TASK_ID = bi_metrics_task.result.task_id
    logging.info(f"Started BI metric extraction task {bi_metrics_task.result.task_id}")

# ================================
# FETCH METRICS WITH SOURCE METADATA
# ================================

if example_switches.getboolean("FETCH_METRICS_WITH_SOURCE_METADATA"):
    if not BI_METRICS_TASK_ID:
        error_message = "Enable EXTRACT_METRICS_FROM_DOWNSTREAM_BI_ASSETS or set BI_METRICS_TASK_ID to fetch metrics with source metadata."
        logging.error(error_message)
        raise ValueError(error_message)
    bi_metrics_result = alation.alation_ai_data_product.get_data_product_metrics_extraction_result_with_source(
        task_id=BI_METRICS_TASK_ID,
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

if example_switches.getboolean("START_DATA_PRODUCT_REVISION_WORKFLOW"):
    revision_workflow = alation.alation_ai_data_product.initiate_revise_data_product_workflow(
        data_product_id=PUBLISHED_DATA_PRODUCT_ID,
        revise_request=allie.AlationAIReviseDataProductRequest(
            message="Improve metric descriptions and relationships to address SQL evaluation failures, then evaluate the revised data product.",
        ),
    )
    DATA_PRODUCT_REVISION_RESULT_ID = revision_workflow.result.result_id
    logging.info(f"Started revision result {revision_workflow.result.result_id} in chat {revision_workflow.result.chat_id}")

# ================================
# LIST DATA PRODUCT REVISION JOBS
# ================================

if example_switches.getboolean("LIST_DATA_PRODUCT_REVISION_JOBS"):
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

if example_switches.getboolean("FETCH_DATA_PRODUCT_REVISION_RESULT"):
    if not DATA_PRODUCT_REVISION_RESULT_ID:
        error_message = "Enable START_DATA_PRODUCT_REVISION_WORKFLOW or set DATA_PRODUCT_REVISION_RESULT_ID to fetch a revision result."
        logging.error(error_message)
        raise ValueError(error_message)
    revision_result = alation.alation_ai_data_product.get_data_product_revision_result(
        result_id=DATA_PRODUCT_REVISION_RESULT_ID,
    )
    logging.info(f"Revision result {revision_result.result_id} is {revision_result.status}")
    logging.info(f"Revision summary: {revision_result.summary}")
    if revision_result.final_data_product_yaml:
        logging.info(f"Revised data product YAML:\n{revision_result.final_data_product_yaml}")

# ================================
# POLL AN EXISTING DATA PRODUCT CREATION TASK FOR FINAL YAML
# ================================

# Creation task IDs are separate from metric extraction task IDs.
if example_switches.getboolean("POLL_DATA_PRODUCT_CREATION_RESULT"):
    if not DATA_PRODUCT_CREATION_TASK_ID:
        error_message = "Set DATA_PRODUCT_CREATION_TASK_ID to run the creation result polling example."
        logging.error(error_message)
        raise ValueError(error_message)
    created_data_product_yaml = alation.alation_ai_data_product.get_data_product_creation_result(
        task_id=DATA_PRODUCT_CREATION_TASK_ID,
        poll_interval_seconds=3,
        timeout_seconds=300,
    )
    logging.info(f"Completed data product creation YAML:\n{created_data_product_yaml}")
