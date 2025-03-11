import logging
import requests

# from ..core.request_handler import RequestHandler
from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import *
from ..models.document_hub_folder_model import *
from ..models.custom_field_model import *
from ..models.custom_template_model import *
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')

class AlationDocumentHubFolder(AsyncHandler):
    """Alation REST API Documents Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Document Hub Folders  object.
        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
        """
        super().__init__(session = session, host = host, access_token=access_token)

    def get_document_hub_folders(
            self
            , query_params:DocumentHubFolderParams = None
    ) -> list[DocumentHubFolder]:
        """Query multiple Alation Document Hub Folders and return their details
        Args:
            query_params (DocumentHubFolderParams): REST API Documents Query Parameters.
        Returns:
            list: Alation Documents
        """

        validate_query_params(query_params, DocumentHubFolderParams)
        params = query_params.generate_params_dict() if query_params else None

        document_hub_folders = self.get('/integration/v2/folder/', query_params = params)

        if document_hub_folders:
            document_hub_folders_checked = [DocumentHubFolder.from_api_response(document_hub_folder) for document_hub_folder in document_hub_folders]
            return document_hub_folders_checked

    def create_document_hub_folders(
        self
        , document_hub_folders: list[DocumentHubFolderPostItem]
    ) -> list[JobDetailsDocumentHubFolderPost]:

        """Create document hub folders in Bulk
        Args:
            document_hub_folders: list of Allie.DocumentHubFolderPostItem objects. This is the main payload which has to conform to the payload outlined here:

            Additional info:
            https://developer.alation.com/dev/reference/postfolders-1

        Returns:
            List of JobDetailsDocumentHubFolderPost: Status report of the executed background jobs.
            
        Raises:
            requests.exceptions.HTTPError: If the API returns a non-success status code.
        """


        # make sure input data matches expected structure
        item: DocumentHubFolderPostItem
        validate_rest_payload(payload = document_hub_folders, expected_types = (DocumentHubFolderPostItem,))
        # make sure we only include fields with values in the payload
        payload = [item.generate_api_post_payload() for item in document_hub_folders]

        # The API returns a job id which needs to be used in conjunction with the Jobs ID to get the job details
        async_results = self.async_post(
            url = '/integration/v2/folder/'
            , payload = payload
        )

        if async_results:
            return [JobDetailsDocumentHubFolderPost.from_api_response(item) for item in async_results]
        return []

    def update_document_hub_folders(
            self
            , document_hub_folders: list[DocumentHubFolderPutItem]
        ) -> list[JobDetailsDocumentHubFolderPut]:

        """Update Document Hub Folders in Bulk
        Args:
            document_hub_folders: This is the main payload which is a list of DocumentHubFolderPutItem objects

            Additional info:
            https://developer.alation.com/dev/reference/updatefolders

        Returns:
            List of JobDetailsDocumentHubFolderPut: Status report of the executed background jobs.
            
        Raises:
            requests.exceptions.HTTPError: If the API returns a non-success status code.
        """

        # make sure input data matches expected structure
        item: DocumentHubFolderPutItem
        validate_rest_payload(payload = document_hub_folders, expected_types = (DocumentHubFolderPutItem,))
        # make sure we only include fields with values in the payload
        payload = [item.generate_api_put_payload() for item in document_hub_folders]

        # The API returns a job id which needs to be used in conjunction with the Jobs ID to get the job details
        async_results = self.async_put(
            url = '/integration/v2/folder/'
            , payload = payload
        )
        if async_results:
            return [JobDetailsDocumentHubFolderPut.from_api_response(item) for item in async_results]
        return []

    def delete_document_hub_folders(
            self
            , document_hub_folders: list[DocumentHubFolder]
    ) -> JobDetailsDocumentHubFolderDelete:
        """Bulk delete document hub folders

        Args:
            document_hub_folders: List of DocumentHubFolder objects (only need to contain the id)
        """

        if document_hub_folders:

            item: DocumentHubFolder
            validate_rest_payload(payload = document_hub_folders, expected_types = (DocumentHubFolder,))
            payload = {'ids': [item.id for item in document_hub_folders]}

            delete_result = self.delete('/integration/v2/folder/', payload)

            # There's no job ID returned here
            if delete_result:
                # make sure result conforms to JobDetails structure
                return JobDetailsDocumentHubFolderDelete.from_api_response(delete_result)