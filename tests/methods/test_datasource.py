import requests_mock
from allie_sdk.methods.datasource import *



MOCK_USER = AlationDatasource(
    access_token='test'
    , session=requests.session()
    , host='https://test.com'
)

def test_get_ocf_datasources(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the document request?
    datasource_api_response = [
        {
            "uri": "mysql://<hostname>:<port>/<db_name>",
            "connector_id": 101,
            "db_username": "alation",
            "title": "test_mysql",
            "description": "Sample mysql datasource setup",
            "private": False,
            "is_hidden": False,
            "id": 0,
            "supports_explain": True,
            "data_upload_disabled_message": "string",
            "is_gone": True,
            "supports_qli_diagnostics": True,
            "latest_extraction_time": "2024-06-17T12:23:27.154Z",
            "negative_filter_words": [
                "string"
            ],
            "can_data_upload": True,
            "qualified_name": "string",
            "all_schemas": "string",
            "has_previewable_qli": True,
            "supports_qli_daterange": True,
            "latest_extraction_successful": True,
            "owner_ids": [
                0
            ],
            "favorited_by_list": True,
            "supports_compose": True,
            "enable_designated_credential": True,
            "deleted": True,
            "limit_schemas": "string",
            "obfuscate_literals": [
                "string"
            ],
            "remove_filtered_schemas": True,
            "profiling_tip": "string",
            "supports_profiling": True,
            "icon": "string",
            "url": "string",
            "otype": "string",
            "exclude_schemas": "string",
            "exclude_additional_columns_in_qli": True,
            "can_toggle_ds_privacy": True,
            "supports_md_diagnostics": True,
            "supports_ocf_query_service_api": True,
            "uses_ocf_agent": True,
            "nosql_mde_sample_size": 0,
            "disable_auto_extraction": True,
            "unresolved_mention_fingerprint_method": "string",
            "enable_default_schema_extraction": True,
            "enabled_in_compose": True,
            "builtin_datasource": "string",
            "cron_extraction": "string",
            "supports_default_schema_extraction": True
        }
    ]

    success_datasources = [ OCFDatasource.from_api_response(item) for item in datasource_api_response ]

    # Override the policy API call
    requests_mock.register_uri(
        method = 'GET'
        , url = '/integration/v2/datasource/'
        , json = datasource_api_response
        , status_code = 200
    )

    # --- TEST THE FUNCTION --- #
    datasources = MOCK_USER.get_ocf_datasources()

    assert success_datasources == datasources

def test_get_native_datasources(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the document request?
    datasource_api_response = [
        {
            "dbtype": "mysql",
            "host": "10.11.21.125",
            "port": 3306,
            "uri": "mysql://<hostname>:<port>/<db_name>",
            "dbname": "sample_dbname",
            "db_username": "alation",
            "title": "test_mysql",
            "description": "Sample mysql datasource setup",
            "deployment_setup_complete": True,
            "private": False,
            "is_virtual": False,
            "is_hidden": False,
            "id": 0,
            "supports_explain": True,
            "data_upload_disabled_message": "string",
            "hive_logs_source_type": 0,
            "metastore_uri": True,
            "is_hive": True,
            "is_gone": True,
            "webhdfs_server": "string",
            "supports_qli_diagnostics": True,
            "is_presto_hive": True,
            "latest_extraction_time": "2024-06-17T12:05:41.542Z",
            "negative_filter_words": [
                "string"
            ],
            "has_hdfs_based_qli": True,
            "can_data_upload": True,
            "qualified_name": "string",
            "all_schemas": "string",
            "has_previewable_qli": True,
            "hive_tez_logs_source": "string",
            "has_metastore_uri": True,
            "webhdfs_port": 0,
            "supports_qli_daterange": True,
            "latest_extraction_successful": True,
            "owner_ids": [
                0
            ],
            "favorited_by_list": True,
            "supports_compose": True,
            "hive_logs_source": "string",
            "enable_designated_credential": True,
            "deleted": True,
            "limit_schemas": "string",
            "obfuscate_literals": [
                "string"
            ],
            "remove_filtered_schemas": True,
            "profiling_tip": "string",
            "supports_profiling": True,
            "webhdfs_username": "string",
            "icon": "string",
            "url": "string",
            "otype": "string",
            "exclude_schemas": "string",
            "qli_aws_region": "string",
            "has_aws_glue_metastore": True,
            "exclude_additional_columns_in_qli": True,
            "can_toggle_ds_privacy": True,
            "aws_region": "string",
            "aws_access_key_id": "string",
            "supports_md_diagnostics": True,
            "nosql_mde_sample_size": 0,
            "disable_auto_extraction": True,
            "metastore_type": "string",
            "unresolved_mention_fingerprint_method": "string",
            "qli_hive_connection_source": "string",
            "compose_oauth_enabled": True,
            "enable_default_schema_extraction": True,
            "enabled_in_compose": True,
            "builtin_datasource": "string",
            "has_aws_s3_based_qli": True,
            "qli_aws_access_key_id": "string",
            "jdbc_driver": "string",
            "cron_extraction": "string",
            "supports_default_schema_extraction": True
        }
    ]

    success_datasources = [ NativeDatasource.from_api_response(item) for item in datasource_api_response ]

    # Override the policy API call
    requests_mock.register_uri(
        method = 'GET'
        , url = '/integration/v1/datasource/'
        , json = datasource_api_response
        , status_code = 200
    )

    # --- TEST THE FUNCTION --- #
    datasources = MOCK_USER.get_native_datasources()

    assert success_datasources == datasources