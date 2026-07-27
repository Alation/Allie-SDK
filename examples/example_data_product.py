"""
Example of working with the Data Products API.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- The marketplace and product IDs used below already exist in Alation when you run the read-only sections.
- If you enable the create or publish sections, your user must have the required marketplace and data product permissions.
"""

import configparser
import logging
import sys

import allie_sdk as allie


# ================================
# Set Global Variables
# ================================

DATA_PRODUCT_ID = "finance:last_quarter_sales"
DATA_PRODUCT_VERSION = "1.0.0"
MARKETPLACE_ID = "finance:public"

CREATE_OR_UPDATE_PRODUCT = False
PUBLISH_PRODUCT_TO_MARKETPLACE = False


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

ALATION_USER_ID = config.get(section="api", option="ALATION_USER_ID", fallback=None)
ALATION_BASE_URL = config.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section="api", option="ALATION_API_REFRESH_TOKEN", fallback=None)
ALATION_OAUTH_CLIENT_ID = config.get(section="api", option="ALATION_OAUTH_CLIENT_ID", fallback=None)
ALATION_OAUTH_CLIENT_SECRET = config.get(
    section="api",
    option="ALATION_OAUTH_CLIENT_SECRET",
    fallback=None,
)


# ================================
# Create Session With Your Alation Instance
# ================================

if ALATION_OAUTH_CLIENT_ID and ALATION_OAUTH_CLIENT_SECRET:
    logging.info("Using OAuth client_credentials authentication")
    alation = allie.Alation(
        host=ALATION_BASE_URL,
        client_id=ALATION_OAUTH_CLIENT_ID,
        client_secret=ALATION_OAUTH_CLIENT_SECRET,
    )
else:
    logging.info("Using refresh token authentication")
    alation = allie.Alation(
        host=ALATION_BASE_URL,
        user_id=ALATION_USER_ID,
        refresh_token=ALATION_API_REFRESH_TOKEN,
    )


# ================================
# Build a Typed Data Product Spec
# ================================

data_product_spec = allie.DataProductSpec(
    product=allie.DataProductSpecDefinition(
        productId=DATA_PRODUCT_ID,
        version=DATA_PRODUCT_VERSION,
        contactEmail="data-products@example.com",
        contactName="Finance Data Products Team",
        en=allie.DataProductLanguage(
            name="Last Quarter Sales",
            shortDescription="Regional sales for the last completed quarter",
            description=(
                "This data product contains last-quarter sales measures by region and product line. "
                "Use it for quarterly performance reviews and marketplace demos."
            ),
        ),
        deliverySystems={
            "snowflake": allie.DataProductDeliverySystem(
                type="sql",
                uri="snowflake://acme.analytics/FINANCE/SALES",
                accessRequestInstruction=allie.DataProductAccessRequestInstruction(
                    type="manual",
                    instruction="Request the FINANCE_ANALYST role from the data platform team.",
                    request="https://example.com/access-request",
                ),
            )
        },
        recordSets={
            "quarterly_sales": allie.DataProductRecordSet(
                name="quarterly_sales",
                displayName="Quarterly Sales",
                description="Each row represents total sales for a region and product family.",
                schema=[
                    allie.DataProductRecordSetField(
                        name="quarter",
                        type="date",
                        description="Quarter start date.",
                    ),
                    allie.DataProductRecordSetField(
                        name="region",
                        type="string",
                        description="Commercial region.",
                    ),
                    allie.DataProductRecordSetField(
                        name="booked_revenue",
                        type="number",
                        description="Revenue booked for the quarter.",
                    ),
                ],
                sample=allie.DataProductRecordSetSample(
                    type="mock",
                    data="quarter,region,booked_revenue\n2024-01-01,NA,1250000",
                ),
                dataAccess=[
                    allie.DataProductDataAccess(
                        type="SQL",
                        documentationUrl="https://example.com/docs/quarterly-sales",
                        qualifiedName=allie.DataProductQualifiedName(
                            database="FINANCE",
                            schema="SALES",
                            table="QUARTERLY_SALES",
                        ),
                    )
                ],
            )
        },
        metadata=allie.DataProductMetadata(
            metrics={
                "totalRevenue": allie.DataProductMetric(
                    displayName="Total Revenue",
                    description="Total booked revenue in the record set.",
                    expression="SUM(booked_revenue)",
                    type="numeric",
                    columns=["booked_revenue"],
                )
            }
        ),
    )
)


# ================================
# LIST DATA PRODUCTS
# ================================

data_products = alation.data_product.get_data_products(
    allie.DataProductParams(
        limit=25,
        group_by_product=True,
    )
)
logging.info("Fetched %s data product row(s).", len(data_products))


# ================================
# FETCH A SINGLE DATA PRODUCT
# ================================

data_product = alation.data_product.get_data_product(DATA_PRODUCT_ID)
logging.info(
    "Fetched data product %s version %s with status %s.",
    data_product.product_id,
    data_product.version_id,
    data_product.status,
)


# ================================
# OPTIONALLY CREATE OR UPDATE THE PRODUCT
# ================================

if CREATE_OR_UPDATE_PRODUCT:
    created_product = alation.data_product.create_data_product(data_product_spec)
    logging.info(
        "Created or replaced data product %s version %s.",
        created_product.product_id,
        created_product.version_id,
    )

    checked_product = alation.data_product.check_data_product(
        allie.DataProductCheck(
            product_spec=data_product_spec,
            standards=[
                allie.DataProductCheckStandard(
                    type="static",
                    check="Ensure the product has a contact email.",
                    key="product.contactEmail",
                )
            ],
        )
    )
    logging.info("Standards check returned %s result(s).", len(checked_product))


# ================================
# FETCH MARKETPLACE DETAILS
# ================================

marketplace = alation.data_product.get_data_marketplace(MARKETPLACE_ID)
logging.info(
    "Fetched marketplace %s with %s published product(s).",
    marketplace.external_marketplace_id,
    marketplace.products_total,
)


# ================================
# SEARCH PRODUCTS INSIDE A MARKETPLACE
# ================================

search_results = alation.data_product.search_data_products_in_marketplace(
    MARKETPLACE_ID,
    allie.DataProductSearchQuery(
        user_query="Which data products contain recent sales information?",
    ),
)
logging.info("Marketplace search returned %s product(s).", len(search_results))


# ================================
# OPTIONALLY PUBLISH THE PRODUCT
# ================================

if PUBLISH_PRODUCT_TO_MARKETPLACE:
    published_product = alation.data_product.publish_data_product(
        MARKETPLACE_ID,
        DATA_PRODUCT_ID,
        allie.DataProductPublishParams(version=DATA_PRODUCT_VERSION),
    )
    logging.info(
        "Published product %s version %s to marketplace %s.",
        published_product.product_id,
        published_product.version_id,
        MARKETPLACE_ID,
    )


# ================================
# VIEW EFFECTIVE PERMISSIONS
# ================================

permissions = alation.data_product.get_user_permissions()
logging.info("Authenticated user has %s data product permission assignment(s).", len(permissions))
