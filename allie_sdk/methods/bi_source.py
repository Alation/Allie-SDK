"""Alation REST API BI Source Methods."""

import logging
import requests

from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import *
from ..models.bi_source_model import *
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')

class AlationBISource(AsyncHandler):
    """Alation REST API BI Source Methods."""

    def __init__(self, access_token: str, session: requests.Session,
                 host: str):
        """Creates an instance of the BISource object.
        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
        """
        super().__init__(session = session, host = host, access_token=access_token)

        self._bi_source_endpoint = '/integration/v2/bi/server/'

    def get_bi_servers(self, query_params: BIServerParams = None) -> list[BIServer]:
        """Get multiple Alation BI Servers.

        Args:
            query_params (BIServerParams): REST API Get Filter Values

        Returns:
            list: Alation BI Servers

        """
        validate_query_params(query_params, BIServerParams)
        params = query_params.generate_params_dict() if query_params else None
        bi_servers = self.get(self._bi_source_endpoint, query_params=params)

        if bi_servers:
            return [BIServer.from_api_response(bi_server) for bi_server in bi_servers]
        return []

    def create_bi_servers(self, bi_servers: list[BIServerItem]) -> JobDetailsBIServerPost:
        """Post (Create) Alation BI Servers. Used for creating Virtual BI Servers.

        Args:
            bi_servers (list): list of Alation BI Servers to be created.

        Returns:
            JobDetailsBIServerPost: Job details with specifics around created Alation BI Servers.

        """
        try:
            validate_rest_payload(payload = bi_servers, expected_types = (BIServerItem,))
            payload = [item.generate_api_payload('post') for item in bi_servers]

            bi_servers_response = self.post(self._bi_source_endpoint, body=payload)

            if bi_servers_response:
                # check whether it was a success or failure
                status = bi_servers_response.get("status")
                if status:
                    if status == "failed":
                        return JobDetailsBIServerPost.from_api_response(bi_servers_response)
                else:
                    mapped_bi_servers_response = self._map_request_success_to_job_details(
                        response_data = bi_servers_response
                    )
                    return JobDetailsBIServerPost.from_api_response(mapped_bi_servers_response)
        except requests.exceptions.HTTPError as e:
            # For test compatibility, handle HTTP errors specially
            if e.response.status_code >= 400:
                # Return error in the expected format
                return JobDetailsBIServerPost(
                    status='failed',
                    msg=None,
                    result=e.response.json()
                )
            # Re-raise other HTTP errors
            raise

    def update_bi_server(self, bi_server_id: int, bi_server: BIServerItem) -> JobDetails:
        """PATCH (Update) Alation BI Server. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to update.
            bi_server (BIServerItem): Alation BI Server to be updated.

        Returns:
            JobDetails

        """
        try:
            validate_rest_payload(payload = [bi_server], expected_types = (BIServerItem,))
            payload = bi_server.generate_api_payload('patch')

            updated_bi_server = self.patch( url = f'{self._bi_source_endpoint}{bi_server_id}/', body=payload)

            if updated_bi_server:
                # check whether it was a success or failure
                status = updated_bi_server.get("status")
                if status:
                    if status == "failed":
                        return JobDetails.from_api_response(updated_bi_server)
                else:
                    mapped_updated_bi_server = self._map_request_success_to_job_details(
                        response_data=updated_bi_server
                    )
                    return JobDetails.from_api_response(mapped_updated_bi_server)

        except requests.exceptions.HTTPError as e:
            # For test compatibility, handle HTTP errors specially
            if e.response.status_code >= 400:
                # Return error in the expected format
                return JobDetails(
                    status='failed',
                    msg=None,
                    result=e.response.json()
                )
            # Re-raise other HTTP errors
            raise


    def get_bi_folders(self, bi_server_id: int, query_params: BIFolderParams = None) -> list[BIFolder]:
        """Get multiple Alation BI Folders.

        Args:
            bi_server_id (int): Alation BI Server ID to get BI folders from.
            query_params (BIFolderParams): REST API Get Filter Values.

        Returns:
            list: Alation BI Folders
        """
        validate_query_params(query_params, BIFolderParams)
        params = query_params.generate_params_dict() if query_params else None

        bi_folders = self.get(
            url = f'{self._bi_source_endpoint}{bi_server_id}/folder/'
            , query_params=params
        )

        if bi_folders:
            return [BIFolder.from_api_response(bi_folder) for bi_folder in bi_folders]
        return []

    # Note: Using get_bi_folders we can get a similar result to get_a_bi_folder
    def get_a_bi_folder(
            self
            , bi_server_id: int
            , bi_folder_id: int
    ) -> BIFolder:
        """Get an Alation BI Folder.

        Args:
            bi_server_id (int): Alation BI Server ID to get a BI folder from.
            bi_folder_id (int): Alation BI Folder object id.

        Returns:
            BIFolder

        """
        bi_folder = self.get(
            url = f'{self._bi_source_endpoint}{bi_server_id}/folder/{bi_folder_id}/'
            , pagination=False
        )

        if bi_folder:
            return BIFolder.from_api_response(bi_folder)

    def create_or_update_bi_folders_using_external_id(
            self
            , bi_server_id: int
            , bi_folders: list[BIFolderItem]
    ) -> list[JobDetails]:
        """Post (Create/Update) Alation BI Folders. This method is not allowed for non-virtual BI Servers.

        Creates and updates folder objects via external_id.
        If an object with a matching external_id exists, it is updated with the given payload.
        Otherwise, it is created.
        Note that this method is not allowed for non-virtual servers.

        Args:
            bi_server_id (int): Alation BI Server ID to create/update BI Folders for.
            bi_folders (list): list of Alation BI Folders to be created or updates.

        Returns:
            bool: Success of the API POST Call.

        """
        validate_rest_payload(payload = bi_folders, expected_types = (BIFolderItem,))
        payload = [item.generate_api_payload() for item in bi_folders]

        async_results = self.async_post(
            url = f'{self._bi_source_endpoint}{bi_server_id}/folder/'
            , payload = payload
        )

        if async_results:
            return [JobDetails.from_api_response(item) for item in async_results]
        return []

    def update_bi_folder_using_internal_id(
            self
            , bi_server_id: int
            , bi_folder_id: int
            , bi_folder: BIFolderItem
    ) -> BIFolder:
        """PATCH (Update) an Alation BI Folder. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID of the BI Folder that will be updated.
            bi_folder_id (int): Alation BI Folder object id of the BI Folder to be updated.
            bi_folder (BIFolderItem): Alation BI Folder with updated fields.

        Returns:
            BIFolder: Updated Alation BI Folder that was updated.

        """
        validate_rest_payload(
            payload = [bi_folder]
            , expected_types = (BIFolderItem,)
        )
        payload = bi_folder.generate_api_payload()

        updated_bi_folder = self.patch(
            url = f'{self._bi_source_endpoint}{bi_server_id}/folder/{bi_folder_id}/'
            , body=payload
        )

        if updated_bi_folder:
            return BIFolder.from_api_response(updated_bi_folder)

    def delete_bi_folders(
            self
            , bi_server_id: int
            , query_params: BIFolderParams = None
    ) -> JobDetails:
        """
        Delete Alation BI Folders. Note that all bulk DELETE methods require a range of IDs.
        This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to delete the BI folders from.
            query_params (BIFolderParams): Alation BI Folder params. This is mandatory.

        Returns:
            JobDetails

        """

        if query_params:
            validate_query_params(query_params, BIFolderParams)
            params = query_params.generate_params_dict() if query_params else None
        else:
            params = None

        deleted = self.delete(url = f'{self._bi_source_endpoint}{bi_server_id}/folder/', query_params=params)

        if deleted:
            return JobDetails.from_api_response(deleted)

    # Commented below since there's no need for yet another delete folder function since we can do the same with the above one.
    # def delete_a_bi_folder(
    #         self
    #         , bi_server_id: int
    #         , bi_folder_id: int
    # ) -> bool:
    #     """Delete an Alation BI Folder. This method is not allowed for non-virtual BI Servers.
    #
    #     Args:
    #         bi_server_id (int): Alation BI Server ID to delete the BI folder from.
    #         bi_folder_id (int): Alation BI Folder object id to delete.
    #
    #     Returns:
    #         bool: Success of the API DELETE Call.
    #
    #     """
    #     deleted = self.delete(f'{self._bi_source_endpoint}{bi_server_id}/folder/{bi_folder_id}/')
    #
    #     if deleted:
    #         return True

    def create_or_update_bi_reports_using_external_id(
            self
            , bi_server_id: int
            , bi_reports: list[BIReportItem]
    ) -> list[JobDetails]:
        """
        Post (Create/Update) Alation BI Reports objects via the external_id property.
        If an object with a matching external_id exists, it is updated with the given payload.
        Otherwise, it is created. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to create/update BI Reports for.
            bi_reports (list): list of Alation BI Reports to be created/updated.

        Returns:
            list of JobDetails

        """
        validate_rest_payload(payload = bi_reports, expected_types = (BIReportItem,))
        payload = [item.generate_api_payload() for item in bi_reports]

        async_results = self.async_post(
            url = f'{self._bi_source_endpoint}{bi_server_id}/report/'
            , payload = payload
        )

        if async_results:
            return [JobDetails.from_api_response(item) for item in async_results]
        return []

    def get_bi_reports(self, bi_server_id: int, query_params: BIReportParams = None) -> list:
        """Get multiple Alation BI Reports.

        Args:
            bi_server_id (int): Alation BI Server ID to get BI reports from.
            query_params (BIReportParams): REST API Get Filter Values.

        Returns:
            list: Alation BI Reports

        """
        validate_query_params(query_params, BIReportParams)
        params = query_params.generate_params_dict() if query_params else None

        bi_reports = self.get(f'{self._bi_source_endpoint}{bi_server_id}/report/', query_params=params)

        if bi_reports:
            return [BIReport.from_api_response(bi_report) for bi_report in bi_reports]

    def get_a_bi_report(self, bi_server_id: int, bi_report_id: int) -> BIReport:
        """Get an Alation BI Report.

        Args:
            bi_server_id (int): Alation BI Server ID to get a BI Report from.
            bi_report_oid (int): Alation BI Report object id.

        Returns:
            BIReport: Alation BI Report

        """
        bi_report = self.get(f'{self._bi_source_endpoint}{bi_server_id}/report/{bi_report_id}/', pagination=False)

        if bi_report:
            return BIReport.from_api_response(bi_report)

    def delete_bi_reports(
            self
            , bi_server_id: int
            , query_params: BIReportParams = None
    ) -> JobDetails:
        """Delete Alation BI reports. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to delete the BI reports from.
            query_params (BIReportParams): Alation BI Report params.

        Returns:
            JobDetails

        """

        if query_params:
            validate_query_params(query_params, BIReportParams)
            params = query_params.generate_params_dict()
        else:
            params = None

        deleted = self.delete(f'{self._bi_source_endpoint}{bi_server_id}/report/', query_params=params)

        if deleted:
            return JobDetails.from_api_response(deleted)

    def delete_a_bi_report(self, bi_server_id: int, bi_report_id: int) -> JobDetails:
        """Delete an Alation BI report. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to delete the BI report from.
            bi_report_id (int): Alation BI Folder object id to delete.

        Returns:
            bool: Success of the API DELETE Call.

        """

        deleted = self.delete(f'{self._bi_source_endpoint}{bi_server_id}/report/{bi_report_id}/')

        if deleted:
            return JobDetails.from_api_response(deleted)

    def update_bi_report_using_internal_id(
            self
            , bi_server_id: int
            , bi_report_id: int
            , bi_report: BIReportItem
    ) -> BIReport:
        """PATCH (Update) an Alation BI Report. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID of the BI Report that will be updated.
            bi_report_id (int): Alation BI Report object id of the BI Report to be updated.
            bi_report (BIReportItem): Alation BI Report with updated fields.

        Returns:
            BIReport: Alation BI Report that was updated.

        """
        validate_rest_payload(
            payload = [bi_report]
            , expected_types = (BIReportItem,)
        )
        payload = bi_report.generate_api_payload()

        updated_bi_report = self.patch(
            url = f"{self._bi_source_endpoint}{bi_server_id}/report/{bi_report_id}/"
            , body = payload
        )

        if updated_bi_report:
            return BIReport.from_api_response(updated_bi_report)

    def create_or_update_bi_report_columns_using_external_id(
            self
            , bi_server_id: int
            , bi_report_columns: list[BIReportColumnItem]
    ) -> list[JobDetails]:
        """Post (Create/Update) Alation BI Report Columns.
        If an object with a matching external_id exists, it is updated with the given payload. Otherwise, it is created.
        This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to create/update BI Report Columns for.
            bi_report_columns (list): list of Alation BI Report Columns to be created/updated.

        Returns:
            list of JobDetails

        """
        validate_rest_payload(
            payload = bi_report_columns
            , expected_types = (BIReportColumnItem,)
        )
        payload = [item.generate_api_payload() for item in bi_report_columns]

        async_results = self.async_post(
            url = f'{self._bi_source_endpoint}{bi_server_id}/report/column/'
            , payload=payload
        )

        if async_results:
            return [JobDetails.from_api_response(item) for item in async_results]
        return []

    def update_bi_report_column_using_internal_id(
            self
            , bi_server_id: int
            , bi_report_column_id: int
            , bi_report_column: BIReportColumnItem
    ) -> BIReportColumn:
        """Patch (Update) Alation BI Report Columns.
        This method will partially update a single Report Column.
        This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to update BI Report Columns for.
            bi_report_column (BIReportColumnItem): Alation BI Report Column to be updated.

        Returns:
            BIReportColumn

        """
        validate_rest_payload(
            payload = [bi_report_column]
            , expected_types = (BIReportColumnItem,)
        )
        payload = bi_report_column.generate_api_payload()

        result = self.patch(
            url = f'{self._bi_source_endpoint}{bi_server_id}/report/column/{bi_report_column_id}/'
            , body = payload
        )

        if result:
            return BIReportColumn.from_api_response(result)

    def get_bi_report_columns(
            self
            , bi_server_id: str
            , query_params: Optional[BIReportColumnParams] = None
    ) -> list[BIReportColumn]:
        """
        GET a set of report columns from a specified BI Server.

        Args:
            server_id (str): The ID of the BI server.
            query_params (BIReportColumnParams): REST API Get Filter Values.

        Returns:
            list[BIReportColumn]: A list of ReportColumn objects.
        """
        validate_query_params(query_params, BIReportColumnParams)
        params = query_params.generate_params_dict() if query_params else None

        url = f"{self._bi_source_endpoint}{bi_server_id}/report/column/"
        bi_report_columns = self.get(url=url, query_params=params)

        if bi_report_columns:
            return [BIReportColumn.from_api_response(data) for data in bi_report_columns]
        return []

    def delete_bi_report_columns(
            self
            , bi_server_id: int
            , query_params: BIReportColumnParams = None
    ) -> JobDetails:
        """Delete Alation BI report columns. This method is not allowed for non-virtual BI Servers.

        Args:
            bi_server_id (int): Alation BI Server ID to delete the BI reports from.
            query_params (BIReportColumnParams): Alation BI Report Column params.

        Returns:
            JobDetails

        """

        if query_params:
            validate_query_params(query_params, BIReportColumnParams)
            params = query_params.generate_params_dict()
        else:
            params = None

        deleted = self.delete(
            url = f'{self._bi_source_endpoint}{bi_server_id}/report/column/'
            , query_params=params
        )

        if deleted:
            return JobDetails.from_api_response(deleted)
