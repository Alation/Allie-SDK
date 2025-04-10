"""Alation REST API BI Source Methods."""

import logging
import requests

from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import validate_query_params, InvalidParams
from ..models.bi_source_model import *

LOGGER = logging.getLogger()


class AlationBISource(AsyncHandler):
    """Alation REST API BI Source Methods."""

    def __init__(self, access_token: str, session: requests.Session,
                 host: str):
        """Creates an instance of the BI Source object.

        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(access_token, session, host)

        self._bi_source_endpoint = '/integration/v2/bi/server/'

    def get_bi_servers(self, query_params: BIServerParams = None) -> list:
        """Get multiple Alation BI Servers.

        Args:
            query_params (BIServerParams): REST API Get Filter Values.

        Returns:
            list: Alation BI Servers

        """
        validate_query_params(query_params, BIServerParams)
        params = query_params.generate_params_dict() if query_params else None
        bi_servers = self.get(self._bi_source_endpoint, query_params=params)

        if bi_servers:
            return [BIServer.from_api_response(bi_server) for bi_server in bi_servers]

    def get_a_bi_server(self, bi_server_id: int) -> BIServer:
        """Get an Alation BI Server by BI Server ID.

        Args:
            bi_server_id (int): Alation BI Server ID.

        Returns:
            BI Server: Alation BI Server.

        """
        bi_server = self.get(f'{self._bi_source_endpoint}{bi_server_id}/', pagination=False)

        if bi_server:
            return BIServer.from_api_response(bi_server)

    def post_bi_servers(self, bi_servers: list) -> CreateBIServersSuccessResponse:
        """Post (Create) Alation BI Servers. Used for creating Virtual BI Servers.

        Args:
            bi_servers (list): list of Alation BI Servers to be created.

        Returns:
            CreateBIServersSuccessResponse: Created Alation BI Servers response.

        """
        validate_rest_payload(bi_servers, (BIServerItem,))
        payload = [item.generate_api_payload('post') for item in bi_servers]
        LOGGER.debug(payload)
        bi_servers_response = self.post(self._bi_source_endpoint, body=payload)

        if bi_servers_response:
            return CreateBIServersSuccessResponse._from_api_response(bi_servers_response)

    def patch_bi_server(self, bi_server_id: int, bi_server: BIServerItem) -> UpdateBIServersSuccessResponse:
        """PATCH (Update) Alation BI Server. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to update.
            bi_server (BIServerItem): Alation BI Server to be updated.

        Returns:
            UpdateBIServersSuccessResponse: Updated Alation BI Server response.

        """
        validate_rest_payload([bi_server], (BIServerItem,))
        payload = bi_server.generate_api_payload('patch')
        LOGGER.debug(payload)
        updated_bi_server = self.patch(f'{self._bi_source_endpoint}{bi_server_id}/', body=payload)

        if updated_bi_server:
            return UpdateBIServersSuccessResponse.from_api_response(updated_bi_server)

    def delete_bi_folders(self, bi_server_id: int, query_params: BaseBISourceParams) -> bool:
        """Delete Alation BI Folders. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to delete the BI folders from.
            query_params (BaseBISourceParams): Alation BI Folder params.

        Returns:
            bool: Success of the API DELETE Call.

        """

        validate_query_params(query_params, BaseBISourceParams)
        params = query_params.generate_params_dict()

        if isinstance(params.get('oids'), list):
            params['oids'] = ','.join(map(str, params['oids']))

        deleted = self.delete(f'{self._bi_source_endpoint}{bi_server_id}/folder/', query_params=params)

        if deleted:
            return True

    def get_bi_folders(self, bi_server_id: int, query_params: BISourceParams = None) -> list:
        """Get multiple Alation BI Folders.

        Args:
            bi_server_id (int): Alation BI Server ID to get BI folders from.
            query_params (BISourceParams): REST API Get Filter Values.

        Returns:
            list: Alation BI Folders

        """
        validate_query_params(query_params, BISourceParams)
        params = query_params.generate_params_dict() if query_params else None
        if params and params.get('oids') and isinstance(params.get('oids'), list):
            params['oids'] = ','.join(map(str, params['oids']))
        bi_folders = self.get(f'{self._bi_source_endpoint}{bi_server_id}/folder/', query_params=params)

        if bi_folders:
            return [BIFolder.from_api_response(bi_folder) for bi_folder in bi_folders]

    def post_bi_folders(self, bi_server_id: int, bi_folders: list) -> bool:
        """Post (Create/Update) Alation BI Folders. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to create/update BI Folders for.
            bi_folders (list): list of Alation BI Folders to be created or updates.

        Returns:
            bool: Success of the API POST Call.

        """
        validate_rest_payload(bi_folders, (BIFolderItem,))
        payload = [item.generate_api_payload() for item in bi_folders]
        LOGGER.debug(payload)
        async_result = self.async_post(f'{self._bi_source_endpoint}{bi_server_id}/folder/', payload)

        return True if not async_result else False

    def delete_a_bi_folder(self, bi_server_id: int, bi_folder_oid: int) -> bool:
        """Delete an Alation BI Folder. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to delete the BI folder from.
            bi_folder_oid (int): Alation BI Folder object id to delete.

        Returns:
            bool: Success of the API DELETE Call.

        """
        deleted = self.delete(f'{self._bi_source_endpoint}{bi_server_id}/folder/{bi_folder_oid}/')

        if deleted:
            return True

    def get_a_bi_folder(self, bi_server_id: int, bi_folder_oid: int) -> list:
        """Get an Alation BI Folder.

        Args:
            bi_server_id (int): Alation BI Server ID to get a BI folder from.
            bi_folder_oid (int): Alation BI Folder object id.

        Returns:
            list: Alation BI Folders

        """
        bi_folder = self.get(f'{self._bi_source_endpoint}{bi_server_id}/folder/{bi_folder_oid}/', pagination=False)

        if bi_folder:
            return BIFolder.from_api_response(bi_folder)

    def patch_bi_folder(self, bi_server_id: int, bi_folder_oid: int, bi_folder: BIFolderItem) -> BIFolder:
        """PATCH (Update) an Alation BI Folder. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID of the BI Folder that will be updated.
            bi_folder_oid (int): Alation BI Folder object id of the BI Folder to be updated.
            bi_folder (BIFolderItem): Alation BI Folder with updated fields.

        Returns:
            BIFolder: Updated Alation BI Folder that was updated.

        """
        validate_rest_payload([bi_folder], (BIFolderItem,))
        payload = bi_folder.generate_api_payload()
        LOGGER.debug(payload)
        updated_bi_folder = self.patch(f'{self._bi_source_endpoint}{bi_server_id}/folder/{bi_folder_oid}/',
                                       body=payload)

        if updated_bi_folder:
            return BIFolder.from_api_response(updated_bi_folder)

    def post_bi_reports(self, bi_server_id: int, bi_reports: list) -> bool:
        """Post (Create/Update) Alation BI Reports. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to create/update BI Reports for.
            bi_reports (list): list of Alation BI Reports to be created/updated.

        Returns:
            bool: Success of the API POST Call.

        """
        validate_rest_payload(bi_reports, (BIReportItem,))
        payload = [item.generate_api_payload() for item in bi_reports]
        LOGGER.debug(payload)
        async_result = self.async_post(f'{self._bi_source_endpoint}{bi_server_id}/report/', payload=payload)

        return True if not async_result else False

    def delete_bi_reports(self, bi_server_id: int, query_params: BaseBISourceParams) -> bool:
        """Delete Alation BI reports. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to delete the BI reports from.
            query_params (BaseBISourceParams): Alation BI Folder params.

        Returns:
            bool: Success of the API DELETE Call.

        """

        validate_query_params(query_params, BaseBISourceParams)
        params = query_params.generate_params_dict()

        if isinstance(params.get('oids'), list):
            params['oids'] = ','.join(map(str, params['oids']))

        deleted = self.delete(f'{self._bi_source_endpoint}{bi_server_id}/report/', query_params=params)

        if deleted:
            return True

    def get_bi_reports(self, bi_server_id: int, query_params: BISourceParams = None) -> list:
        """Get multiple Alation BI Reports.

        Args:
            bi_server_id (int): Alation BI Server ID to get BI reports from.
            query_params (BISourceParams): REST API Get Filter Values.

        Returns:
            list: Alation BI Reports

        """
        validate_query_params(query_params, BISourceParams)
        params = query_params.generate_params_dict() if query_params else None
        if params and params.get('oids') and isinstance(params.get('oids'), list):
            params['oids'] = ','.join(map(str, params['oids']))
        bi_reports = self.get(f'{self._bi_source_endpoint}{bi_server_id}/report/', query_params=params)

        if bi_reports:
            return [BIReport.from_api_response(bi_report) for bi_report in bi_reports]

    def delete_a_bi_report(self, bi_server_id: int, bi_report_oid: int) -> bool:
        """Delete an Alation BI report. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to delete the BI report from.
            bi_report_oid (int): Alation BI Folder object id to delete.

        Returns:
            bool: Success of the API DELETE Call.

        """

        deleted = self.delete(f'{self._bi_source_endpoint}{bi_server_id}/report/{bi_report_oid}')

        if deleted:
            return True

    def get_a_bi_report(self, bi_server_id: int, bi_report_oid: int) -> BIReport:
        """Get an Alation BI Report.

        Args:
            bi_server_id (int): Alation BI Server ID to get a BI Report from.
            bi_report_oid (int): Alation BI Report object id.

        Returns:
            BIReport: Alation BI Report

        """
        bi_report = self.get(f'{self._bi_source_endpoint}{bi_server_id}/report/{bi_report_oid}/', pagination=False)

        if bi_report:
            return BIReport.from_api_response(bi_report)

    def patch_bi_report(self, bi_server_id: int, bi_report_oid: int, bi_report: BIReportItem) -> BIReport:
        """PATCH (Update) an Alation BI Report. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID of the BI Report that will be updated.
            bi_report_oid (int): Alation BI Report object id of the BI Report to be updated.
            bi_report (BIReportItem): Alation BI Report with updated fields.

        Returns:
            BIReport: Updated Alation BI Report that was updated.

        """
        validate_rest_payload([bi_report], (BIReportItem,))
        payload = bi_report.generate_api_payload()
        LOGGER.debug(payload)
        updated_bi_report = self.patch(f'{self._bi_source_endpoint}{bi_server_id}/report/{bi_report_oid}/',
                                       body=payload)

        if updated_bi_report:
            return BIReport.from_api_response(updated_bi_report)

    def post_bi_report_columns(self, bi_server_id: int, bi_report_columns: list) -> bool:
        """Post (Create/Update) Alation BI Report Columns.
        If an object with a matching external_id exists, it is updated with the given payload. Otherwise, it is created.
        This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to create/update BI Report Columns for.
            bi_report_columns (list): list of Alation BI Report Columns to be created/updated.

        Returns:
            bool: Success of the API POST Call.

        """
        validate_rest_payload(bi_report_columns, (BIReportColumnItem,))
        payload = [item.generate_api_payload() for item in bi_report_columns]
        LOGGER.debug(payload)
        async_result = self.async_post(f'{self._bi_source_endpoint}{bi_server_id}/report/column/', payload=payload)

        return True if not async_result else False
