"""Alation REST API Methods."""

import logging.config

import requests

from .core.logs import LoggingConfigs
from .methods import (
    AlationAuthentication,
    AlationBusinessPolicy,
    AlationConnector,
    AlationCustomField,
    AlationCustomTemplate,
    AlationDataDictionary,
    AlationDataflow,
    AlationDataQuality,
    AlationDatasource,
    AlationDocument,
    AlationDocumentHubFolder,
    AlationDomain,
    AlationGlossaryTerm,
    AlationGroup,
    AlationOtype,
    AlationPolicyGroup,
    AlationQuery,
    AlationRDBMS,
    AlationTrustChecks,
    AlationUser,
    AlationVirtualDataSource,
    AlationVirtualFileSystem,
    AlationVisualConfig,
)
from .models import JobDetails

logging.config.dictConfig(LoggingConfigs.logging_configs())
LOGGER = logging.getLogger('allie_sdk_logger')


class Alation(object):
    """Alation REST API Methods."""

    def __init__(self, host: str, user_id: int, refresh_token: str = None,
                 access_token: str = None, validate_ssl: bool = True,
                 private_ssl_cert: str = None, disable_authentication: bool = False):
        """Creates an instance of the Alation object.

        Args:
            host (str): Alation URL.
            refresh_token (str): Alation REST API Refresh Token.
            user_id (int): Alation User ID.
            access_token (str): Alation REST API Access Token.
            validate_ssl (bool): Validate the SSL Cert when using HTTPS Requests.
            private_ssl_cert (str): Path to the Private SSL Cert or CA Bundle.
            disable_authentication (bool): if True, this Alation instance can be instantiated without authenticating first

        """
        self._access_token = None
        session = requests.session()
        session.verify = validate_ssl
        if private_ssl_cert:
            session.verify = private_ssl_cert
            
        if not disable_authentication:
            # Initialize the Authentication Class and generate the Access Token
            self.authentication = AlationAuthentication(
                refresh_token=refresh_token
                , user_id=user_id
                , session=session
                , host=host
            )
            if access_token:
                self.access_token = self.authentication.validate_access_token(
                    access_token).api_access_token
            else:
                create_access_token_response = self.authentication.create_access_token()
                if isinstance(create_access_token_response, JobDetails):
                    if create_access_token_response.status == "failed":
                        cat_response_error_detail = create_access_token_response.result.get("detail")
                        if cat_response_error_detail:
                            LOGGER.error(cat_response_error_detail)
                else:
                    self.access_token = create_access_token_response.api_access_token
        else:
            self.authentication = AlationAuthentication(
                refresh_token=refresh_token
                , user_id=user_id
                , session=session
                , host=host
            )

        # Initialize Remaining Alation API Methods
        self.connector = AlationConnector(
            access_token=self.access_token, session=session, host=host
        )
        self.custom_field = AlationCustomField(
            access_token=self.access_token, session=session, host=host
        )
        self.custom_template = AlationCustomTemplate(
            access_token=self.access_token, session=session, host=host
        )
        self.dataflow = AlationDataflow(
            access_token=self.access_token, session=session, host=host
        )
        self.data_quality = AlationDataQuality(
            access_token=self.access_token, session=session, host=host
        )
        self.data_dictionary = AlationDataDictionary(
            access_token=self.access_token, session=session, host=host
        )
        self.datasource = AlationDatasource(
            access_token=self.access_token, session=session, host=host
        )
        self.document = AlationDocument(
            access_token=self.access_token, session=session, host=host
        )
        self.document_hub_folder = AlationDocumentHubFolder(
            access_token=self.access_token, session=session, host=host
        )
        self.domain = AlationDomain(
            access_token=self.access_token, session=session, host=host
        )
        self.glossary_term = AlationGlossaryTerm(
            access_token=self.access_token, session=session, host=host
        )
        self.group = AlationGroup(
            access_token=self.access_token, session=session, host=host
        )
        self.otype = AlationOtype(
            access_token=self.access_token, session=session, host=host
        )
        self.rdbms = AlationRDBMS(
            access_token=self.access_token, session=session, host=host
        )
        self.user = AlationUser(
            access_token=self.access_token, session=session, host=host
        )
        self.trust_checks = AlationTrustChecks(
            access_token=self.access_token, session=session, host=host
        )
        self.business_policy = AlationBusinessPolicy(
            access_token=self.access_token, session=session, host=host
        )
        self.policy_group = AlationPolicyGroup(
            access_token=self.access_token, session=session, host=host
        )
        self.query = AlationQuery(
            access_token=self.access_token, session=session, host=host
        )
        self.virtual_filesystem = AlationVirtualFileSystem(
            access_token=self.access_token, session=session, host=host
        )
        self.virtual_datasource = AlationVirtualDataSource(
            access_token=self.access_token, session=session, host=host
        )
        self.visual_config = AlationVisualConfig(
            access_token=self.access_token, session=session, host=host
        )

    @property
    def access_token(self) -> str:
        """Return the Alation API Access Token.

        Returns:
            str: Alation API Access Token.

        """
        return self._access_token

    @access_token.setter
    def access_token(self, token: str):
        """Set the Alation API Access Token.

        Args:
            token (str): Alation API Access Token.

        """
        self._access_token = token
