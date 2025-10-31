"""Alation REST API Relational Integration Methods."""

import logging
import requests

from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.rdbms_model import (

    Schema, SchemaItem, SchemaParams, SchemaPatchItem,
    Table, TableItem, TablePatchItem, TableParams,
    Column, ColumnItem, ColumnIndex, ColumnPatchItem, ColumnParams
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

    def get_schemas(self, query_params: SchemaParams = None) -> list[Schema]:
        """Query multiple Alation RDBMS Schemas.

        Args:
            query_params (SchemaParams): REST API Get Filter Values.

        Returns:
            list: Alation RDBMS Schemas.

        """
        try:
            validate_query_params(query_params, SchemaParams)
            params = query_params.generate_params_dict() if query_params else None
            schemas = self.get('/integration/v2/schema/', query_params=params)

            if schemas:
                return [Schema.from_api_response(schema) for schema in schemas]
            return []
        except requests.exceptions.HTTPError:
            # Re-raise the error
            raise

    def post_schemas(self, ds_id: int, schemas: list) -> list[JobDetailsRdbms]:
        """Post (Create or Update) Alation Schema Objects.

        Args:
            ds_id (int): ID of the Alation Schemas' Parent Datasource.
            schemas (list): Alation Schemas to be created or updated.

        Returns:
            List of JobDetailsRdbms: Job details

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        item: SchemaItem
        validate_rest_payload(schemas, (SchemaItem,))
        payload = [item.generate_api_post_payload() for item in schemas]
        async_results = self.async_post(f'/integration/v2/schema/?ds_id={ds_id}', payload)

        if async_results:
            return [JobDetailsRdbms.from_api_response(item) for item in async_results]
        return []

    def patch_schemas(self, ds_id: int, schemas: list[SchemaPatchItem]) -> list[JobDetailsRdbms]:
        """Patch (Update) Alation Schema Objects.

        Args:
            ds_id (int): ID of the Alation Schemas' Parent Datasource.
            schemas (list[SchemaPatchItem]): Alation Schemas to be updated.

        Returns:
            list[JobDetailsRdbms]: result of the job

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        item: SchemaPatchItem
        validate_rest_payload(schemas, (SchemaPatchItem,))
        payload = [item.generate_api_patch_payload() for item in schemas]
        async_results = self.async_patch(f'/integration/v2/schema/?ds_id={ds_id}', payload)

        if async_results:
            return [JobDetailsRdbms.from_api_response(item) for item in async_results]
        return []

    def get_tables(self, query_params: TableParams = None) -> list[Table]:
        """Query multiple Alation RDBMS Tables.

        Args:
            query_params (TableParams): REST API Get Filter Values.

        Returns:
            list: Alation RDBMS Tables.

        """
        try:
            validate_query_params(query_params, TableParams)
            params = query_params.generate_params_dict() if query_params else None
            tables = self.get('/integration/v2/table/', query_params=params)

            if tables:
                return [Table.from_api_response(table) for table in tables]
            return []
        except requests.exceptions.HTTPError:
            # Re-raise the error
            raise

    def post_tables(self, ds_id: int, tables: list) -> list[JobDetailsRdbms]:
        """Post (Create or Update) Alation Table Objects.

        Args:
            ds_id (int): ID of the Alation Tables' Parent Datasource.
            tables (list): Alation Tables to be created or updated.

        Returns:
            list[JobDetailsRdbms]: Result of the job

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        item: TableItem
        validate_rest_payload(tables, (TableItem,))
        payload = [item.generate_api_post_payload() for item in tables]
        async_results = self.async_post(f'/integration/v2/table/?ds_id={ds_id}', payload)

        if async_results:
            return [JobDetailsRdbms.from_api_response(item) for item in async_results]
        return []

    def patch_tables(self, ds_id: int, tables: list[TablePatchItem]) -> list[JobDetailsRdbms]:
        """Patch (Update) Alation Table Objects.

        Args:
            ds_id (int): ID of the Alation Tables' Parent Datasource.
            tables (list[TablePatchItem]): Alation Tables to be updated.

        Returns:
            list[JobDetailsRdbms]: Result of the job

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        item: TablePatchItem
        validate_rest_payload(tables, (TablePatchItem,))
        payload = [item.generate_api_patch_payload() for item in tables]
        async_results = self.async_patch(f'/integration/v2/table/?ds_id={ds_id}', payload)

        if async_results:
            return [JobDetailsRdbms.from_api_response(item) for item in async_results]
        return []

    def get_columns(self, query_params: ColumnParams = None) -> list[Column]:
        """Query multiple Alation RDBMS Columns.

        Args:
            query_params (ColumnParams): REST API Get Filter Values.

        Returns:
            list: Alation RDBMS Tables.

        """
        try:
            validate_query_params(query_params, ColumnParams)
            params = query_params.generate_params_dict() if query_params else None
            columns = self.get('/integration/v2/column/', query_params=params)

            if columns:
                return [Column.from_api_response(column) for column in columns]
            return []
        except requests.exceptions.HTTPError:
            # Re-raise the error
            raise

    def patch_columns(self, ds_id: int, columns: list[ColumnPatchItem]) -> list[JobDetailsRdbms]:
        """Patch (Update) Alation Column Objects.

        Args:
            ds_id (int): ID of the Alation Columns' Parent Datasource.
            columns (list): Alation Columns to be updated.

        Returns:
            list[JobDetailsRdbms]: result of the job

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        item: ColumnPatchItem
        validate_rest_payload(columns, (ColumnPatchItem,))
        payload = [item.generate_api_patch_payload() for item in columns]
        async_results = self.async_patch(f'/integration/v2/column/?ds_id={ds_id}', payload)

        if async_results:
            return [JobDetailsRdbms.from_api_response(item) for item in async_results]
        return []

    def post_columns(self, ds_id: int, columns: list) -> list[JobDetailsRdbms]:
        """Post (Create or Update) Alation Column Objects.

        Args:
            ds_id (int): ID of the Alation Columns' Parent Datasource.
            columns (list): Alation Columns to be created or updated.

        Returns:
            list[JobDetailsRdbms]: result of the job

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        item: ColumnItem
        validate_rest_payload(columns, (ColumnItem,))
        payload = [item.generate_api_post_payload() for item in columns]
        async_results = self.async_post(f'/integration/v2/column/?ds_id={ds_id}', payload)

        if async_results:
            return [JobDetailsRdbms.from_api_response(item) for item in async_results]
        return []
