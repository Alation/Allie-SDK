# Initial Setup

Rename config.ini.sample to config.ini and adjust the settings.

Adjust the config settings in each example file. Each file will list any prerequisites that are required for running the code - these are listed at the beginning of the file.

## Data Products example

`example_data_product.py` demonstrates every public method in
`allie_sdk/methods/data_product.py`: product and marketplace CRUD, versions,
individual and bulk publishing, search, standards checks, product-specific and
cross-product reports, and permissions.

Copy the `[data_product]` and `[data_product_examples]` sections from
`config.ini.sample` into your `config.ini`, alongside your existing `[api]`
credentials. All inputs and switches for this example are configured there.
`PRODUCT_DEFINITION`, `MARKETPLACE_DEFINITION`, and `CHECK_STANDARDS` contain JSON;
keep continuation lines indented. Product/version/marketplace IDs come from the
shared ID settings and do not need to be repeated in the JSON definitions.
The definitions are converted into typed SDK models, including nested schema
fields, samples, access instructions, and metrics.

Run `python example_data_product.py` from the `examples` directory after selecting
switches. Every switch is initially `False`. Enable the create, get, and update
switches together for a lifecycle demonstration, or supply existing object IDs
when running selected examples. Set `VERSION_STATUS=ready` and enable
`UPDATE_DATA_PRODUCT_VERSION` before publishing a draft version. The bulk example
uses the `update` list, so it needs an existing publication or the preceding
`PUBLISH_PRODUCT_TO_MARKETPLACE` example. `BulkPublishInfo` also supports `publish`
and `unpublish` lists. Permission examples use the configured test user/group;
set `PERMISSION_SUBJECT_ID` to an existing subject other than your own account.

All reads and updates precede cleanup. Cleanup runs in this order when enabled:
unpublish the product, delete the permission using its current role, delete the
product version, delete the product, and delete the marketplace. Enable those
switches only for disposable objects. The script never enables a prerequisite or
cleanup switch automatically.
