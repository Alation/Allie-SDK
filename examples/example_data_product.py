"""Examples for every public method in the Data Products API.

Configure ``config.ini`` before running this file from the examples directory:

- ``[api]``: ALATION_BASE_URL and either refresh-token or OAuth credentials.
- ``[data_product]``: product/version/marketplace IDs, JSON spec definitions,
  update values, report values, search text, pagination, and permission subject.
- ``[data_product_examples]``: switches selecting the examples to run.

All switches in config.ini.sample are disabled initially. Enable create switches
for new objects, or supply existing IDs for individual get/update examples.
Publishing and bulk updating require a ready product version. Permission
examples require an existing test user or group with the configured subject ID.
Cleanup runs last: unpublish, delete permission, delete version, delete product,
and delete marketplace. Enable cleanup switches only for disposable objects.
"""

import configparser
import json
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

config = configparser.ConfigParser(interpolation=None)
config.read("config.ini")

ALATION_USER_ID = config.get(section="api", option="ALATION_USER_ID", fallback=None)
ALATION_BASE_URL = config.get(section="api", option="ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section="api", option="ALATION_API_REFRESH_TOKEN", fallback=None)
ALATION_OAUTH_CLIENT_ID = config.get(section="api", option="ALATION_OAUTH_CLIENT_ID", fallback=None)
ALATION_OAUTH_CLIENT_SECRET = config.get(section="api", option="ALATION_OAUTH_CLIENT_SECRET", fallback=None)

data_product_settings = config["data_product"]
example_switches = config["data_product_examples"]

DATA_PRODUCT_ID = data_product_settings["DATA_PRODUCT_ID"]
DATA_PRODUCT_VERSION = data_product_settings["DATA_PRODUCT_VERSION"]
MARKETPLACE_ID = data_product_settings["MARKETPLACE_ID"]

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
# Build Typed Specifications From Config
# ================================

# Nested dictionaries are converted into typed descriptions, delivery systems,
# record sets, schema fields, samples, data access entries, and metrics.
data_product_spec = allie.DataProductSpec(
    product=allie.DataProductSpecDefinition(
        productId=DATA_PRODUCT_ID,
        version=DATA_PRODUCT_VERSION,
        **json.loads(data_product_settings["DATA_PRODUCT_DEFINITION"]),
    )
)

marketplace_spec = allie.DataMarketplaceSpec(
    marketplace=allie.DataMarketplaceDefinition(
        marketplaceId=MARKETPLACE_ID,
        **json.loads(data_product_settings["MARKETPLACE_DEFINITION"]),
    )
)

# ================================
# CREATE DATA PRODUCT
# ================================

if example_switches.getboolean("CREATE_DATA_PRODUCT"):
    created_data_product = alation.data_product.create_data_product(data_product_spec=data_product_spec)
    logging.info(f"Create data product result: {created_data_product}")

# ================================
# CHECK DATA PRODUCT
# ================================

if example_switches.getboolean("CHECK_DATA_PRODUCT"):
    checked_product = alation.data_product.check_data_product(
        data_product_check=allie.DataProductCheck(
            product_spec=data_product_spec,
            standards=[allie.DataProductCheckStandard.from_api_response(standard) for standard in json.loads(data_product_settings["CHECK_STANDARDS"])],
        )
    )
    logging.info(f"Standards check returned {len(checked_product)} result(s).")

# ================================
# FETCH A SINGLE DATA PRODUCT
# ================================

if example_switches.getboolean("FETCH_A_SINGLE_DATA_PRODUCT"):
    data_product = alation.data_product.get_data_product(data_product_id=DATA_PRODUCT_ID)
    logging.info(f"Fetched data product {data_product.product_id} version {data_product.version_id} with status {data_product.status}.")

# ================================
# LIST DATA PRODUCTS
# ================================

if example_switches.getboolean("LIST_DATA_PRODUCTS"):
    data_products = alation.data_product.get_data_products(
        query_params=allie.DataProductParams(
            limit=data_product_settings.getint("LIST_LIMIT"),
            group_by_product=data_product_settings.getboolean("GROUP_BY_PRODUCT"),
        )
    )
    logging.info(f"Fetched {len(data_products)} data product row(s).")

# ================================
# UPDATE DATA PRODUCT
# ================================

if example_switches.getboolean("UPDATE_DATA_PRODUCT"):
    data_product_spec.product.contactEmail = data_product_settings["UPDATED_CONTACT_EMAIL"]
    updated_data_product = alation.data_product.update_data_product(data_product_spec=data_product_spec)
    logging.info(f"Update data product result: {updated_data_product}")

# ================================
# FETCH A DATA PRODUCT VERSION
# ================================

if example_switches.getboolean("FETCH_DATA_PRODUCT_VERSION"):
    data_product_version = alation.data_product.get_data_product_version(
        product_id=DATA_PRODUCT_ID,
        version_id=DATA_PRODUCT_VERSION,
    )
    logging.info(f"Fetched version {data_product_version.version_id} with status {data_product_version.status}.")

# ================================
# UPDATE DATA PRODUCT VERSION STATUS
# ================================

if example_switches.getboolean("UPDATE_DATA_PRODUCT_VERSION_STATUS"):
    updated_version = alation.data_product.update_data_product_version_status(
        product_id=DATA_PRODUCT_ID,
        version_id=DATA_PRODUCT_VERSION,
        data_product_version=allie.DataProductVersionStatusUpdate(status=data_product_settings["VERSION_STATUS"]),
    )
    logging.info(f"Updated version {updated_version.version_id} to status {updated_version.status}.")

# ================================
# CREATE DATA MARKETPLACE
# ================================

if example_switches.getboolean("CREATE_DATA_MARKETPLACE"):
    create_marketplace_result = alation.data_product.create_data_marketplace(marketplace_spec=marketplace_spec)
    if create_marketplace_result is not None:
        logging.info(f"Create marketplace status: {create_marketplace_result.status}. Message: {create_marketplace_result.msg}")
    else:
        logging.info("Create marketplace request succeeded with an empty response.")

# ================================
# FETCH MARKETPLACE DETAILS
# ================================

if example_switches.getboolean("FETCH_MARKETPLACE_DETAILS"):
    marketplace = alation.data_product.get_data_marketplace(marketplace_id=MARKETPLACE_ID)
    logging.info(f"Fetched marketplace {marketplace.external_marketplace_id} with {marketplace.products_total} published product(s).")

# ================================
# LIST DATA MARKETPLACES
# ================================

if example_switches.getboolean("LIST_DATA_MARKETPLACES"):
    marketplaces = alation.data_product.get_data_marketplaces(
        query_params=allie.DataMarketplaceParams(limit=data_product_settings.getint("LIST_LIMIT")),
    )
    logging.info(f"Fetched {len(marketplaces)} marketplace(s).")

# ================================
# UPDATE DATA MARKETPLACE
# ================================

if example_switches.getboolean("UPDATE_DATA_MARKETPLACE"):
    marketplace_spec.marketplace.en.description = data_product_settings["UPDATED_MARKETPLACE_DESCRIPTION"]
    updated_marketplace = alation.data_product.update_data_marketplace(marketplace_spec=marketplace_spec)
    logging.info(f"Updated marketplace {updated_marketplace.external_marketplace_id}.")

# ================================
# PUBLISH PRODUCT TO MARKETPLACE
# ================================

if example_switches.getboolean("PUBLISH_PRODUCT_TO_MARKETPLACE"):
    published_product = alation.data_product.publish_data_product(
        marketplace_id=MARKETPLACE_ID,
        product_id=DATA_PRODUCT_ID,
        query_params=allie.DataProductPublishParams(version=DATA_PRODUCT_VERSION),
    )
    logging.info(f"Published product {published_product.product_id} version {published_product.version_id} to marketplace {MARKETPLACE_ID}.")

# ================================
# GET WORKFLOW REQUESTS
# ================================

# After a data product gets published, an approval workflow is automatically triggered.
# We have to fetch the approval workflow id.
# TODO: Support for this will be implemented at a later stage. Out of scope for this change request.

# ================================
# APPROVE WORKFLOW REQUESTS
# ================================

# Once we have the approval workflow id we can approve the request ...
# TODO: Support for this will be implemented at a later stage. Out of scope for this change request.

# ================================
# LIST AND FETCH PUBLISHED DATA PRODUCTS
# ================================

if example_switches.getboolean("LIST_PUBLISHED_DATA_PRODUCTS"):
    published_products = alation.data_product.get_published_data_products(
        marketplace_id=MARKETPLACE_ID,
        query_params=allie.PublishedDataProductParams(limit=data_product_settings.getint("LIST_LIMIT")),
    )
    logging.info(f"Fetched {len(published_products)} published product(s).")

if example_switches.getboolean("FETCH_PUBLISHED_DATA_PRODUCT"):
    published_product_details = alation.data_product.get_published_data_product(
        marketplace_id=MARKETPLACE_ID,
        product_id=DATA_PRODUCT_ID,
    )
    logging.info(f"Fetched published product {published_product_details.product_id} version {published_product_details.version_id}.")

# ================================
# UPDATE A PUBLISHED DATA PRODUCT
# ================================

if example_switches.getboolean("UPDATE_PUBLISHED_DATA_PRODUCT"):
    updated_published_product = alation.data_product.update_published_data_product(
        marketplace_id=MARKETPLACE_ID,
        product_id=DATA_PRODUCT_ID,
        query_params=allie.DataProductPublishParams(version=DATA_PRODUCT_VERSION),
    )
    logging.info(f"Updated published product {updated_published_product.product_id} to version {updated_published_product.version_id}.")

# ================================
# SEARCH PRODUCTS INSIDE A MARKETPLACE
# ================================

if example_switches.getboolean("SEARCH_PRODUCTS_INSIDE_A_MARKETPLACE"):
    search_results = alation.data_product.search_data_products_in_marketplace(
        marketplace_id=MARKETPLACE_ID,
        search_query=allie.DataProductSearchQuery(user_query=data_product_settings["SEARCH_QUERY"]),
    )
    logging.info(f"Marketplace search returned {len(search_results)} product(s).")

# ================================
# CREATE, FETCH, AND UPDATE PERMISSIONS
# ================================

permission = allie.DataProductPermission(
    subject_type=data_product_settings["PERMISSION_SUBJECT_TYPE"],
    subject_id=data_product_settings["PERMISSION_SUBJECT_ID"],
    object_type="data_product",
    object_id=DATA_PRODUCT_ID,
    role=data_product_settings["PERMISSION_ROLE"],
)

if example_switches.getboolean("CREATE_PERMISSION"):
    created_permission = alation.data_product.create_permission(permission=permission)
    logging.info(f"Create permission result: {created_permission}")

if example_switches.getboolean("FETCH_PERMISSIONS"):
    permissions = alation.data_product.get_permissions(
        query_params=allie.DataProductPermissionParams(
            subject_type=permission.subject_type,
            subject_id=permission.subject_id,
            object_type=permission.object_type,
            object_id=permission.object_id,
        )
    )
    logging.info(f"Fetched {len(permissions)} permission assignment(s).")

if example_switches.getboolean("UPDATE_PERMISSION"):
    permission.role = data_product_settings["UPDATED_PERMISSION_ROLE"]
    updated_permission = alation.data_product.update_permission(permission=permission)
    logging.info(f"Update permission result: {updated_permission}")

if example_switches.getboolean("VIEW_EFFECTIVE_PERMISSIONS"):
    user_permissions = alation.data_product.get_user_permissions()
    logging.info(f"Authenticated user has {len(user_permissions)} data product permission assignment(s).")

# ================================
# CLEANUP AFTER ALL CREATE, GET, AND UPDATE EXAMPLES
# ================================

if example_switches.getboolean("UNPUBLISH_PRODUCT_FROM_MARKETPLACE"):
    unpublished_product = alation.data_product.unpublish_data_product(
        marketplace_id=MARKETPLACE_ID,
        product_id=DATA_PRODUCT_ID,
    )
    logging.info(f"Unpublish product result: {unpublished_product}")

if example_switches.getboolean("DELETE_PERMISSION"):
    # Use the current role, including any change made by UPDATE_PERMISSION.
    deleted_permission = alation.data_product.delete_permission(permission=permission)
    logging.info(f"Delete permission result: {deleted_permission}")

if example_switches.getboolean("DELETE_DATA_PRODUCT_VERSION"):
    deleted_version = alation.data_product.delete_data_product_version(
        product_id=DATA_PRODUCT_ID,
        version_id=DATA_PRODUCT_VERSION,
    )
    logging.info(f"Delete product version result: {deleted_version}")

if example_switches.getboolean("DELETE_DATA_PRODUCT"):
    deleted_product = alation.data_product.delete_data_product(product_id=DATA_PRODUCT_ID)
    logging.info(f"Delete product result: {deleted_product}")

if example_switches.getboolean("DELETE_DATA_MARKETPLACE"):
    deleted_marketplace = alation.data_product.delete_data_marketplace(marketplace_id=MARKETPLACE_ID)
    logging.info(f"Delete marketplace result: {deleted_marketplace}")
