"""
Example of working with the Data Products API.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Adjust the data product spec in the "Build a Typed Data Product Spec" section.
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

DATA_PRODUCT_ID = "last-quarter-sales-3"
DATA_PRODUCT_VERSION = "1.0.0"
MARKETPLACE_ID = "marketplace_id_example"

CREATE_DATA_PRODUCT = False
PUBLISH_PRODUCT_TO_MARKETPLACE = True


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
        en=allie.DataProductDescription(
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
                uri="snowflake://alation-alationproserv.snowflakecomputing.com:443/?warehouse=PS_COMPUTE_WH&db=SUPERSTORE",
                accessRequestInstruction=allie.DataProductAccessRequestInstruction(
                    type="manual",
                    instruction="Request the FINANCE_ANALYST role from the data platform team.",
                    request="https://example.com/access-request",
                ),
            )
        },
        recordSets={
            "quarterly_sales": allie.DataProductRecordSet(
                name="SUPERSTORE_REPORTING",
                displayName="Quarterly Sales",
                description="Each row represents total sales for a region and product family.",
                schema=[
                    allie.DataProductRecordSetField(
                        name="ORDER_DATE",
                        type="date",
                        description="Order Date",
                    ),
                    allie.DataProductRecordSetField(
                        name="COUNTRY",
                        type="string",
                        description="Commercial country",
                    ),
                    allie.DataProductRecordSetField(
                        name="SALES",
                        type="number",
                        description="Money generated",
                    ),
                ],
                sample=allie.DataProductRecordSetSample(
                    type="mock",
                    data="ORDER_DATE,COUNTRY,SALES\n2024-01-01,USA,1250000",
                ),
                dataAccess=[
                    allie.DataProductDataAccess(
                        type="SQL",
                        documentationUrl="snowflake://alation-alationproserv.snowflakecomputing.com:443/?warehouse=PS_COMPUTE_WH&db=SUPERSTORE",
                        qualifiedName=allie.DataProductQualifiedName(
                            database="SUPERSTORE",
                            schema="Public",
                            table="SUPERSTORE_REPORTING",
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
                    expression="SUM(SALES)",
                    type="numeric",
                    columns=["SALES"],
                )
            }
        ),
    )
)

# ================================
# CREATE DATA PRODUCT
# ================================

if CREATE_DATA_PRODUCT:

    created_data_product = alation.data_product.create_data_product(
        data_product_spec = data_product_spec
    )

# ================================
# CHECK DATA PRODUCT
# ================================

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
# FETCH A SINGLE DATA PRODUCT
# ================================

data_product = alation.data_product.get_data_product(
    data_product_id = DATA_PRODUCT_ID
)
logging.info(
    "Fetched data product %s version %s with status %s.",
    data_product.product_id,
    data_product.version_id,
    data_product.status,
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
# UPDATE DATA PRODUCT
# ================================

updated_data_product = alation.data_product.update_data_product(
    data_product_spec = data_product_spec
)




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
