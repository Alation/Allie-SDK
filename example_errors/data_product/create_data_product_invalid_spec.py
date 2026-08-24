"""
Example of a data product create request failing because the typed payload is invalid.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
"""

import configparser
import logging
import sys

import allie_sdk as allie


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
config.read("./../config.ini")

ALATION_USER_ID = config.get(section="api", option="ALATION_USER_ID")
ALATION_BASE_URL = config.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section="api", option="ALATION_API_REFRESH_TOKEN")


# ================================
# Create Session With Your Alation Instance
# ================================

alation = allie.Alation(
    host=ALATION_BASE_URL,
    user_id=ALATION_USER_ID,
    refresh_token=ALATION_API_REFRESH_TOKEN,
)


# ================================
# CREATE DATA PRODUCT: MAKE IT FAIL DURING DATA CLASS VALIDATION
# ================================

invalid_data_product_spec = allie.DataProductSpec(
    product=allie.DataProductSpecDefinition(
        productId=None,  # Required field on purpose.
        version="1.0.0",
        contactEmail="data-products@example.com",
        contactName="Finance Team",
        en=allie.DataProductDescription(
            name="Broken Product Example",
        ),
    )
)

alation.data_product.enrich_data_product_spec(invalid_data_product_spec)

"""
Expected behaviour: Fail before the API request is sent.

Expected error:

allie_sdk.core.custom_exceptions.InvalidPostBody:
Missing required fields for Data Product spec payload bodies: ['productId']
"""
