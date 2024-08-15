"""Alation REST API Relational Integration Methods."""

import logging
import requests

from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.rdbms_model import (
    Schema, SchemaItem, SchemaParams,
    Table, TableItem, TableParams,
    Column, ColumnItem, ColumnParams
)
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationRDBMS(AsyncHandler):
    """Alation REST API Relational Integration Methods."""

    def __init__(self, access_token: str, host: str, session: requests.Session):
        """Creates an instance of the RDBMS object.

        Args:
            access_token (str): Alation REST API Access Token.
            host (str): Alation URL.
            session (requests.Session): Python requests common session.

        """
        super().__init__(access_token, session, host)

    def get_schemas(self, query_params: SchemaParams = None) -> list:
        """Query multiple Alation RDBMS Schemas.

        Args:
            query_params (SchemaParams): REST API Get Filter Values.

        Returns:
            list: Alation RDBMS Schemas.

        """
        validate_query_params(query_params, SchemaParams)
        params = query_params.generate_params_dict() if query_params else None
        schemas = self.get('/integration/v2/schema/', query_params=params)

        if schemas:
            return [Schema.from_api_response(schema) for schema in schemas]

    def post_schemas(self, ds_id: int, schemas: list) -> JobDetailsRdbms:
        """Post (Create or Update) Alation Schema Objects.

        Args:
            ds_id (int): ID of the Alation Schemas' Parent Datasource.
            schemas (list): Alation Schemas to be created or updated.

        Returns:
            JobDetailsRdbms: Job details

        """
        item: SchemaItem
        validate_rest_payload(schemas, (SchemaItem,))
        payload = [item.generate_api_post_payload() for item in schemas]
        async_results = self.async_post(f'/integration/v2/schema/?ds_id={ds_id}', payload)

        if async_results:
            return [JobDetailsRdbms.from_api_response(item) for item in async_results]

    def get_tables(self, query_params: TableParams = None) -> list:
        """Query multiple Alation RDBMS Tables.

        Args:
            query_params (TableParams): REST API Get Filter Values.

        Returns:
            list: Alation RDBMS Tables.

        """
        validate_query_params(query_params, TableParams)
        params = query_params.generate_params_dict() if query_params else None
        tables = self.get('/integration/v2/table/', query_params=params)

        if tables:
            return [Table.from_api_response(table) for table in tables]

    def post_tables(self, ds_id: int, tables: list) -> JobDetailsRdbms:
        """Post (Create or Update) Alation Table Objects.

        Args:
            ds_id (int): ID of the Alation Tables' Parent Datasource.
            tables (list): Alation Tables to be created or updated.

        Returns:
            JobDetailsRdbmsTablePost: Result of the job

        """
        item: TableItem
        validate_rest_payload(tables, (TableItem,))
        payload = [item.generate_api_post_payload() for item in tables]
        async_results = self.async_post(f'/integration/v2/table/?ds_id={ds_id}', payload)

        if async_results:
            return [JobDetailsRdbms.from_api_response(item) for item in async_results]

    def get_columns(self, query_params: ColumnParams = None) -> list:
        """Query multiple Alation RDBMS Columns.

        Args:
            query_params (ColumnParams): REST API Get Filter Values.

        Returns:
            list: Alation RDBMS Tables.

        """
        validate_query_params(query_params, ColumnParams)
        params = query_params.generate_params_dict() if query_params else None
        columns = self.get('/integration/v2/column/', query_params=params)

        if columns:
            return [Column.from_api_response(column) for column in columns]

    def post_columns(self, ds_id: int, columns: list) -> JobDetailsRdbms:
        """Post (Create or Update) Alation Column Objects.

        Args:
            ds_id (int): ID of the Alation Columns' Parent Datasource.
            columns (list): Alation Columns to be created or updated.

        Returns:
            JobDetailsRdbmsColumnPost: result of the job

        """
        item: ColumnItem
        validate_rest_payload(columns, (ColumnItem,))
        payload = [item.generate_api_post_payload() for item in columns]
        async_results = self.async_post(f'/integration/v2/column/?ds_id={ds_id}', payload)

        if async_results:
            return [JobDetailsRdbms.from_api_response(item) for item in async_results]
