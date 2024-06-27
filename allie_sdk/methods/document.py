import logging
import requests

# from ..core.request_handler import RequestHandler
from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import *
from ..models.document_model import *
from ..models.custom_field_model import *
from ..models.custom_template_model import *
from ..models.job_model import *

LOGGER = logging.getLogger()

class AlationDocument(AsyncHandler):
    """Alation REST API Documents Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Documents  object.
        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
        """
        super().__init__(session = session, host = host, access_token=access_token)

    def get_documents(self, query_params:DocumentParams = None) -> list:
        """Query multiple Alation Documents and return their details
        Args:
            query_params (DocumentParams): REST API Documents Query Parameters.
        Returns:
            list: Alation Documents
        """

        validate_query_params(query_params, DocumentParams)
        params = query_params.generate_params_dict() if query_params else None

        documents = self.get('/integration/v2/document/', query_params = params)

        if documents:
            documents_checked = [Document.from_api_response(document) for document in documents]
            return documents_checked
    
    def create_documents (
        self
        , documents: list[DocumentPostItem]
    )->list[JobDetailsDocumentPost]:

        """Create documents in Bulk
        Args:
            documents: list of Allie.DocumentPostItem objects. This is the main payload which has to conform to the payload outlined here:
            https://developer.alation.com/dev/reference/postdocuments

        Returns:
            List of JobDetailsDocumentPost: Status report of the executed background jobs.
        """


        # make sure input data matches expected structure
        item: DocumentPostItem
        validate_rest_payload(documents, (DocumentPostItem,))
        # make sure we only include fields with values in the payload
        payload = [item.generate_api_post_payload() for item in documents]

        # The policys APIs returns a job id which needs to be used in conjunction with the Jobs ID to get the job details
        async_results = self.async_post(
            url = '/integration/v2/document/'
            , payload = payload
        )

        if async_results:
            return [JobDetailsDocumentPost.from_api_response(item) for item in async_results]

    
    def update_documents (
            self
            , documents: list[DocumentPutItem]
        )->list[JobDetailsDocumentPut]:

        """Bulk Update Documents in Bulk
        Args:
            documents: This is the main payload which has to conform to the payload outlined here: 
            https://developer.alation.com/dev/reference/updatedocuments

        Returns:
            List of JobDetailsDocumentPut: Status report of the executed background jobs.
        """

        # make sure input data matches expected structure
        item: DocumentPutItem
        validate_rest_payload(documents, (DocumentPutItem,))
        # make sure we only include fields with values in the payload
        payload = [item.generate_api_put_payload() for item in documents]

        # The policys APIs returns a job id which needs to be used in conjunction with the Jobs ID to get the job details
        async_results = self.async_put(
            url = '/integration/v2/document/'
            , payload = payload
        )
        if async_results:
            return [JobDetailsDocumentPut.from_api_response(item) for item in async_results]


    def delete_documents(
            self
            , documents:list[Document]
        ):
        """Bulk delete documents

        Args:
            documents (list): List of Document
        """

        item: Document
        validate_rest_payload(documents, (Document,))
        payload = {'id': [item.id for item in documents]}
        # The policys APIs returns a job id which needs to be used in conjunction with the Jobs ID to get the job details
        delete_result = self.delete('/integration/v2/document/', payload)
        # There's no job ID or result returned here
        return True if delete_result else False