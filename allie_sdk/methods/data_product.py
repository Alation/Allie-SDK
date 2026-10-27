"""Alation Data Products API methods."""
import json
import logging
from typing import Any

import requests

from ..core.custom_exceptions import (
    InvalidPostBody,
    UnsupportedPostBody,
    validate_query_params,
    validate_rest_payload,
)
from ..core.request_handler import RequestHandler
from ..models.data_product_model import (
    DataMarketplace,
    DataMarketplaceParams,
    DataMarketplaceSpec,
    DataProduct,
    DataProductCheck,
    DataProductCheckResultItem,
    DataProductParams,
    DataProductPermission,
    DataProductPermissionParams,
    DataProductPublishParams,
    DataProductSearchQuery,
    DataProductSpec,
    DataProductVersionUpdate,
    DataProductWithMarketplaceInfo,
    PublishedDataProductParams,
)
from ..models.job_model import JobDetails

LOGGER = logging.getLogger("allie_sdk_logger")


class AlationDataProduct(RequestHandler):
    """Interact with the Alation Data Products API endpoints."""

    def __init__(self, access_token: str, session: requests.Session, host: str) -> None:
        """Initialize a client for the Alation Data Products API.

        Args:
            access_token (str): Alation REST API access token used to authenticate
                requests.
            session (requests.Session): Shared HTTP session used for API calls.
            host (str): Base URL of the Alation server.

        Returns:
            None: Initializes the client's connection and authentication settings.
        """
        super().__init__(session=session, host=host, access_token=access_token)

    @staticmethod
    def _validate_identifier(value: str, field_name: str) -> None:
        """Ensure a required identifier is present before building a request URL.

        Args:
            value (str): Identifier to validate; must not be None or an empty string.
            field_name (str): Parameter name to include in the validation error.

        Returns:
            None: Returns without a value when the identifier is present.

        Raises:
            InvalidPostBody: If the identifier is None or an empty string.
        """
        if value is None or value == "":
            raise InvalidPostBody(f"'{field_name}' must be provided for the Data Products request.")

    @staticmethod
    def _prepare_spec_payload(
        spec_payload: DataProductSpec | DataMarketplaceSpec | dict[str, Any] | str,
        expected_type: type[DataProductSpec] | type[DataMarketplaceSpec],
        payload_name: str,
    ) -> tuple[dict[str, Any] | str, dict[str, str] | None]:
        """Prepare a product or marketplace specification for an API request.

        Dictionaries are converted to the expected model and validated alongside
        model instances. YAML strings are passed through without local validation.

        Args:
            spec_payload (DataProductSpec | DataMarketplaceSpec | dict[str, Any] | str):
                Specification as a model, dictionary, or YAML string.
            expected_type (type[DataProductSpec] | type[DataMarketplaceSpec]): Model
                class required by the endpoint and used to convert dictionaries.
            payload_name (str): Argument name to include in validation errors.

        Returns:
            tuple[dict[str, Any] | str, dict[str, str] | None]: Request body and
            optional headers. YAML bodies have an application/x-yaml Content-Type
            header; model and dictionary bodies are serialized to dictionaries
            with no header override.

        Raises:
            InvalidPostBody: If the specification is missing or its model fields
                fail payload validation.
            UnsupportedPostBody: If the payload is not the expected model, a
                dictionary, or a string.
        """
        if spec_payload is None:
            raise InvalidPostBody(f"'{payload_name}' is required for the Data Products request.")

        if isinstance(spec_payload, str):
            return spec_payload, {"Content-Type": "application/x-yaml; charset=utf-8"}

        if isinstance(spec_payload, dict):
            spec_payload = expected_type.from_api_response(spec_payload)

        if not isinstance(spec_payload, expected_type):
            raise UnsupportedPostBody(
                f"Unsupported type '{type(spec_payload)}' was passed for API Body Payload\n"
                f"Please use:\n - {'.'.join((expected_type.__module__, expected_type.__qualname__))}\n"
                " - dict\n - str"
            )

        validate_rest_payload(payload=[spec_payload], expected_types=(expected_type,))
        return spec_payload.generate_api_payload(), None

    @staticmethod
    def _paginate_when_unbounded(query_params: DataProductParams | DataMarketplaceParams | PublishedDataProductParams | None) -> bool:
        """Determine whether a list request should automatically fetch more pages.

        Args:
            query_params (DataProductParams | DataMarketplaceParams | PublishedDataProductParams | None):
                Optional query parameters whose limit and offset control pagination.

        Returns:
            bool: True when no parameters are supplied or both limit and offset
            are None; False when either pagination bound is explicitly set.
        """
        if query_params is None:
            return True
        return getattr(query_params, "limit", None) is None and getattr(query_params, "offset", None) is None

    def get_data_products(
        self,
        query_params: DataProductParams | None = None,
    ) -> list[DataProduct]:
        """List data products with optional filtering, ordering, and grouping.

        All result pages are fetched unless query_params explicitly sets a limit
        or offset.

        Args:
            query_params (DataProductParams, optional): Product IDs, role and action
                filters, sort order, grouping, and pagination bounds. Defaults to
                None to use the API defaults and fetch all pages.

        Returns:
            list[DataProduct]: Matching products, including version summaries when
            grouping is requested. Returns an empty list if no products are found.
        """
        validate_query_params(query_params, DataProductParams)
        params = query_params.generate_params_dict() if query_params else None
        paginate = self._paginate_when_unbounded(query_params)

        LOGGER.info("Fetching data products.")
        response = self.get_nested_results(
            url="/dps/integration/data-products/v1/data-product/",
            query_params=params,
            pagination=paginate,
        )

        if response:
            return [DataProduct.from_api_response(item) for item in response]
        return []

    def create_data_product(
        self,
        data_product_spec: DataProductSpec | dict[str, Any] | str,
    ) -> JobDetails | None:
        """Create a data product from its specification.

        Args:
            data_product_spec (DataProductSpec | dict[str, Any] | str): Complete
                product specification as a typed model, a dictionary containing
                the product definition, or a YAML string. Models and dictionaries
                are validated locally; YAML is sent directly to the API.

        Returns:
            JobDetails | None: Operation status with the API response stored in
            result, or None if the API response is empty.
        """
        payload, headers = self._prepare_spec_payload(
            spec_payload=data_product_spec,
            expected_type=DataProductSpec,
            payload_name="data_product_spec",
        )

        LOGGER.info("Creating a data product.")
        response = self.post(
            url="/dps/integration/data-products/v1/data-product/",
            body=payload,
            headers=headers,
        )
        if response:

            mapped_response = self._map_request_success_to_job_details(
                response_data=response
            )
            LOGGER.info("Data product created")
            return JobDetails.from_api_response(mapped_response)
        else:
            return None

    def update_data_product(
        self,
        data_product_spec: DataProductSpec | dict[str, Any] | str,
    ) -> JobDetails | None:
        """Update a data product using the identifiers in its specification.

        Args:
            data_product_spec (DataProductSpec | dict[str, Any] | str): Complete
                replacement specification as a typed model, a dictionary containing
                the product definition, or a YAML string. Models and dictionaries
                are validated locally; YAML is sent directly to the API.

        Returns:
            JobDetails | None: Operation status with the API's message stored in
            msg, or None if the API response is empty.
        """
        payload, headers = self._prepare_spec_payload(
            spec_payload=data_product_spec,
            expected_type=DataProductSpec,
            payload_name="data_product_spec",
        )

        LOGGER.info("Updating a data product.")
        response = self.put(
            url="/dps/integration/data-products/v1/data-product/",
            body=payload,
            headers=headers,
        )

        if response:
            response_message = response.get("message")
            mapped_response = self._map_request_success_to_job_details(
                msg = response_message
            )

            return JobDetails.from_api_response(mapped_response)
        else:
            return None

    def get_data_product(self, data_product_id: str) -> DataProduct:
        """Retrieve a data product by its product identifier.

        Args:
            data_product_id (str): Non-empty identifier of the product to retrieve.

        Returns:
            DataProduct: Product details, including identifiers, status, and any
            specifications or marketplace associations supplied by the API.
        """
        self._validate_identifier(data_product_id, "product_id")

        LOGGER.info("Fetching data product '%s'.", data_product_id)
        response = self.get(
            url=f"/dps/integration/data-products/v1/data-product/{data_product_id}/",
            pagination=False,
        )
        return DataProduct.from_api_response(response)

    def delete_data_product(self, product_id: str) -> JobDetails:
        """Delete a data product by its product identifier.

        Args:
            product_id (str): Non-empty identifier of the product to delete.

        Returns:
            JobDetails: Deletion status and any response message from the API.
        """
        self._validate_identifier(product_id, "product_id")

        LOGGER.info("Deleting data product '%s'.", product_id)
        response = self.delete(
            url=f"/dps/integration/data-products/v1/data-product/{product_id}/",
        )
        return JobDetails.from_api_response(response)

    def get_data_product_version(self, product_id: str, version_id: str) -> DataProduct:
        """Retrieve the details and specification of a particular product version.

        Args:
            product_id (str): Non-empty identifier of the data product.
            version_id (str): Non-empty identifier of the version to retrieve.

        Returns:
            DataProduct: Product details for the requested version, including its
            status and any specification supplied by the API.
        """
        self._validate_identifier(product_id, "product_id")
        self._validate_identifier(version_id, "version_id")

        LOGGER.info("Fetching data product '%s' version '%s'.", product_id, version_id)
        response = self.get(
            url=f"/dps/integration/data-products/v1/data-product/{product_id}/version/{version_id}/",
            pagination=False,
        )
        return DataProduct.from_api_response(response)

    def update_data_product_version(
        self,
        product_id: str,
        version_id: str,
        data_product_version: DataProductVersionUpdate,
    ) -> DataProduct:
        """Change the status of a particular data product version.

        Args:
            product_id (str): Non-empty identifier of the data product.
            version_id (str): Non-empty identifier of the version to update.
            data_product_version (DataProductVersionUpdate): Status update payload.
                Its status must be "draft" or "ready".

        Returns:
            DataProduct: Updated product version returned by the API.
        """
        self._validate_identifier(product_id, "product_id")
        self._validate_identifier(version_id, "version_id")
        if data_product_version is None:
            raise InvalidPostBody("'data_product_version' is required for the Data Products request.")

        validate_rest_payload(payload=[data_product_version], expected_types=(DataProductVersionUpdate,))
        payload = data_product_version.generate_api_payload()

        LOGGER.info("Updating data product '%s' version '%s'.", product_id, version_id)
        response = self.put(
            url=f"/dps/integration/data-products/v1/data-product/{product_id}/version/{version_id}/",
            body=payload,
        )
        return DataProduct.from_api_response(response)

    def delete_data_product_version(self, product_id: str, version_id: str) -> JobDetails:
        """Delete a particular version of a data product.

        Args:
            product_id (str): Non-empty identifier of the data product.
            version_id (str): Non-empty identifier of the version to delete.

        Returns:
            JobDetails: Version deletion status and any response message from
            the API.
        """
        self._validate_identifier(product_id, "product_id")
        self._validate_identifier(version_id, "version_id")

        LOGGER.info("Deleting data product '%s' version '%s'.", product_id, version_id)
        response = self.delete(
            url=f"/dps/integration/data-products/v1/data-product/{product_id}/version/{version_id}/",
        )
        return JobDetails.from_api_response(response)

    def get_data_marketplaces(
        self,
        query_params: DataMarketplaceParams | None = None,
    ) -> list[DataMarketplace]:
        """List data marketplaces, fetching all pages unless bounds are supplied.

        Args:
            query_params (DataMarketplaceParams, optional): Limit and offset for
                the request. Defaults to None. Automatic pagination is enabled
                when neither bound is set.

        Returns:
            list[DataMarketplace]: Marketplaces returned by the API, including
            any specifications and product summaries. Returns an empty list if
            no marketplaces are found.
        """
        validate_query_params(query_params, DataMarketplaceParams)
        params = query_params.generate_params_dict() if query_params else None
        paginate = self._paginate_when_unbounded(query_params)

        LOGGER.info("Fetching data marketplaces.")
        response = self.get(
            url="/dps/integration/data-products/v1/marketplace/",
            query_params=params,
            pagination=paginate,
        )

        if response:
            return [DataMarketplace.from_api_response(item) for item in response]
        return []

    def create_data_marketplace(
        self,
        marketplace_spec: DataMarketplaceSpec | dict[str, Any] | str,
    ) -> DataMarketplace:
        """Create a data marketplace from its specification.

        Args:
            marketplace_spec (DataMarketplaceSpec | dict[str, Any] | str): Complete
                marketplace specification as a typed model, a dictionary containing
                the marketplace definition, or a YAML string. Models and dictionaries
                are validated locally; YAML is sent directly to the API.

        Returns:
            DataMarketplace: Created marketplace, including any specification and
            product information supplied by the API.
        """
        payload, headers = self._prepare_spec_payload(
            spec_payload=marketplace_spec,
            expected_type=DataMarketplaceSpec,
            payload_name="marketplace_spec",
        )

        LOGGER.info("Creating a data marketplace.")
        response = self.post(
            url="/dps/integration/data-products/v1/marketplace/",
            body=payload,
            headers=headers,
        )
        return DataMarketplace.from_api_response(response)

    def update_data_marketplace(
        self,
        marketplace_spec: DataMarketplaceSpec | dict[str, Any] | str,
    ) -> DataMarketplace:
        """Update a data marketplace using the identifier in its specification.

        Args:
            marketplace_spec (DataMarketplaceSpec | dict[str, Any] | str): Complete
                replacement specification as a typed model, a dictionary containing
                the marketplace definition, or a YAML string. Models and dictionaries
                are validated locally; YAML is sent directly to the API.

        Returns:
            DataMarketplace: Updated marketplace, including any specification and
            product information supplied by the API.
        """
        payload, headers = self._prepare_spec_payload(
            spec_payload=marketplace_spec,
            expected_type=DataMarketplaceSpec,
            payload_name="marketplace_spec",
        )

        LOGGER.info("Updating a data marketplace.")
        response = self.put(
            url="/dps/integration/data-products/v1/marketplace/",
            body=payload,
            headers=headers,
        )
        return DataMarketplace.from_api_response(response)

    def get_data_marketplace(
        self,
        marketplace_id: str,
        query_params: DataMarketplaceParams | None = None,
    ) -> DataMarketplace:
        """Retrieve a marketplace and any product information supplied by the API.

        Args:
            marketplace_id (str): Non-empty identifier of the marketplace to retrieve.
            query_params (DataMarketplaceParams, optional): Limit and offset to send
                with the detail request. Defaults to None. This method does not
                automatically fetch additional pages.

        Returns:
            DataMarketplace: Marketplace details, including its specification,
            products, and product count when provided by the API.
        """
        self._validate_identifier(marketplace_id, "marketplace_id")
        validate_query_params(query_params, DataMarketplaceParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info("Fetching data marketplace '%s'.", marketplace_id)
        response = self.get(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/",
            query_params=params,
            pagination=False,
        )
        return DataMarketplace.from_api_response(response)

    def delete_data_marketplace(self, marketplace_id: str) -> JobDetails:
        """Delete a data marketplace by its identifier.

        Args:
            marketplace_id (str): Non-empty identifier of the marketplace to delete.

        Returns:
            JobDetails: Marketplace deletion status and any response message from
            the API.
        """
        self._validate_identifier(marketplace_id, "marketplace_id")

        LOGGER.info("Deleting data marketplace '%s'.", marketplace_id)
        response = self.delete(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/",
        )
        return JobDetails.from_api_response(response)

    def get_published_data_products(
        self,
        marketplace_id: str,
        query_params: PublishedDataProductParams | None = None,
    ) -> list[DataProductWithMarketplaceInfo]:
        """List the data products published in a particular marketplace.

        All result pages are fetched unless query_params explicitly sets a limit
        or offset.

        Args:
            marketplace_id (str): Non-empty identifier of the marketplace to browse.
            query_params (PublishedDataProductParams, optional): Limit and offset
                for the request. Defaults to None to fetch all pages.

        Returns:
            list[DataProductWithMarketplaceInfo]: Published products with any
            marketplace context, such as badges, supplied by the API. Returns an
            empty list if no products are found.
        """
        self._validate_identifier(marketplace_id, "marketplace_id")
        validate_query_params(query_params, PublishedDataProductParams)
        params = query_params.generate_params_dict() if query_params else None
        paginate = self._paginate_when_unbounded(query_params)

        LOGGER.info("Fetching published data products for marketplace '%s'.", marketplace_id)
        response = self.get(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/data-product/",
            query_params=params,
            pagination=paginate,
        )

        if response:
            return [DataProductWithMarketplaceInfo.from_api_response(item) for item in response]
        return []

    def get_published_data_product(
        self,
        marketplace_id: str,
        product_id: str,
    ) -> DataProductWithMarketplaceInfo:
        """Retrieve a published product and its context within a marketplace.

        Args:
            marketplace_id (str): Non-empty identifier of the marketplace containing
                the published product.
            product_id (str): Non-empty identifier of the published data product.

        Returns:
            DataProductWithMarketplaceInfo: Published product details with any
            marketplace context, such as badges, supplied by the API.
        """
        self._validate_identifier(marketplace_id, "marketplace_id")
        self._validate_identifier(product_id, "product_id")

        LOGGER.info(
            "Fetching published data product '%s' from marketplace '%s'.",
            product_id,
            marketplace_id,
        )
        response = self.get(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/data-product/{product_id}/",
            pagination=False,
        )
        return DataProductWithMarketplaceInfo.from_api_response(response)

    def publish_data_product(
        self,
        marketplace_id: str,
        product_id: str,
        query_params: DataProductPublishParams | None = None,
    ) -> DataProduct:
        """Publish a data product in a particular marketplace.

        Args:
            marketplace_id (str): Non-empty identifier of the target marketplace.
            product_id (str): Non-empty identifier of the product to publish.
            query_params (DataProductPublishParams, optional): Version to publish.
                Defaults to None to let the API choose the version.

        Returns:
            DataProduct: Product details returned by the API after publication.
        """
        self._validate_identifier(marketplace_id, "marketplace_id")
        self._validate_identifier(product_id, "product_id")
        validate_query_params(query_params, DataProductPublishParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info("Publishing data product '%s' into marketplace '%s'.", product_id, marketplace_id)
        response = self.post(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/data-product/{product_id}/",
            body={},
            query_params=params,
        )
        return DataProduct.from_api_response(response)

    def update_published_data_product(
        self,
        marketplace_id: str,
        product_id: str,
        query_params: DataProductPublishParams | None = None,
    ) -> DataProduct:
        """Update which version of a product is published in a marketplace.

        Args:
            marketplace_id (str): Non-empty identifier of the marketplace containing
                the published product.
            product_id (str): Non-empty identifier of the product to update.
            query_params (DataProductPublishParams, optional): Version to publish
                in place of the current version. Defaults to None to let the API
                choose the version.

        Returns:
            DataProduct: Product details returned after updating the publication.
        """
        self._validate_identifier(marketplace_id, "marketplace_id")
        self._validate_identifier(product_id, "product_id")
        validate_query_params(query_params, DataProductPublishParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info(
            "Updating published data product '%s' in marketplace '%s'.",
            product_id,
            marketplace_id,
        )
        response = self.put(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/data-product/{product_id}/",
            body={},
            query_params=params,
        )
        return DataProduct.from_api_response(response)

    def unpublish_data_product(self, marketplace_id: str, product_id: str) -> JobDetails:
        """Remove a product's publication from a particular marketplace.

        Args:
            marketplace_id (str): Non-empty identifier of the marketplace from
                which to remove the product.
            product_id (str): Non-empty identifier of the product to unpublish.

        Returns:
            JobDetails: Unpublish status and any response message from the API.
        """
        self._validate_identifier(marketplace_id, "marketplace_id")
        self._validate_identifier(product_id, "product_id")

        LOGGER.info("Unpublishing data product '%s' from marketplace '%s'.", product_id, marketplace_id)
        response = self.delete(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/data-product/{product_id}/",
        )
        return JobDetails.from_api_response(response)

    def check_data_product(self, data_product_check: DataProductCheck) -> list[DataProductCheckResultItem]:
        """Evaluate a data product specification against supplied standards.

        Args:
            data_product_check (DataProductCheck): Product specification and a
                non-empty list of standards to evaluate. Each standard defines
                its type, check, and key.

        Returns:
            list[DataProductCheckResultItem]: Parsed evaluation results containing
            each standard's key, check, type, pass status, and explanation. Returns
            an empty list if the API response is empty.
        """
        if data_product_check is None:
            raise InvalidPostBody("'data_product_check' is required for the Data Products request.")

        validate_rest_payload(payload=[data_product_check], expected_types=(DataProductCheck,))
        payload = data_product_check.generate_api_payload()

        LOGGER.info("Checking data product against supplied standards.")
        response = self.post(
            url="/dps/integration/data-products/v1/data-product-check/",
            body=payload,
        )

        if response:
            evaluation = response.get("evaluation")
            if isinstance(evaluation, str):
                evaluation_converted = json.loads(evaluation)
                result = [DataProductCheckResultItem.from_api_response(item) for item in evaluation_converted]
            elif isinstance(response, list):
                result = [DataProductCheckResultItem.from_api_response(item) for item in evaluation]

            return result
        return []

    def search_data_products_in_marketplace(
        self,
        marketplace_id: str,
        search_query: DataProductSearchQuery,
    ) -> list[DataProductWithMarketplaceInfo]:
        """Find data products in a marketplace using a natural-language query.

        Args:
            marketplace_id (str): Non-empty identifier of the marketplace to search.
            search_query (DataProductSearchQuery): Search payload whose user_query
                contains the natural-language description of the desired products.

        Returns:
            list[DataProductWithMarketplaceInfo]: Matching products with any
            marketplace context, such as badges, supplied by the API. Returns an
            empty list if no products are found.
        """
        self._validate_identifier(marketplace_id, "marketplace_id")
        if search_query is None:
            raise InvalidPostBody("'search_query' is required for the Data Products request.")

        validate_rest_payload(payload=[search_query], expected_types=(DataProductSearchQuery,))
        payload = search_query.generate_api_payload()

        LOGGER.info("Searching data products inside marketplace '%s'.", marketplace_id)
        response = self.post(
            url=f"/dps/integration/data-products/v1/search-internally/{marketplace_id}/",
            body=payload,
        )

        if response:
            return [DataProductWithMarketplaceInfo.from_api_response(item) for item in response]
        return []

    def get_permissions(
        self,
        query_params: DataProductPermissionParams | None = None,
    ) -> list[DataProductPermission]:
        """List configured Data Products permissions with optional subject and object filters.

        Args:
            query_params (DataProductPermissionParams, optional): Filters for
                subject type and ID, object type and ID, and role. Subject type
                and ID must be supplied together, as must object type and ID.
                Defaults to None to retrieve permissions without these filters.

        Returns:
            list[DataProductPermission]: Matching permission assignments, each
            identifying a subject, object, and role. Returns an empty list if no
            permissions are found.
        """
        validate_query_params(query_params, DataProductPermissionParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info("Fetching data product permissions.")
        response = self.get(
            url="/dps/integration/data-products/v1/data-products/permissions/",
            query_params=params,
            pagination=False,
        )

        if response:
            return [DataProductPermission.from_api_response(item) for item in response]
        return []

    def create_permission(self, permission: DataProductPermission) -> JobDetails:
        """Assign a Data Products role to a subject for a particular object.

        Args:
            permission (DataProductPermission): Permission assignment containing
                subject_type, subject_id, object_type, object_id, and role.

        Returns:
            JobDetails: Creation status with any API response stored in result.
        """
        if permission is None:
            raise InvalidPostBody("'permission' is required for the Data Products request.")

        validate_rest_payload(payload=[permission], expected_types=(DataProductPermission,))
        payload = permission.generate_api_payload()

        LOGGER.info("Creating a data product permission.")
        response = self.post(
            url="/dps/integration/data-products/v1/data-products/permissions/",
            body=payload,
        )
        mapped_response = self._map_request_success_to_job_details(response if response else None)
        return JobDetails.from_api_response(mapped_response)

    def update_permission(self, permission: DataProductPermission) -> JobDetails:
        """Update a Data Products permission assignment for a subject and object.

        Args:
            permission (DataProductPermission): Permission assignment containing
                subject_type, subject_id, object_type, object_id, and the role
                to submit for the update.

        Returns:
            JobDetails: Update status with any API response stored in result.
        """
        if permission is None:
            raise InvalidPostBody("'permission' is required for the Data Products request.")

        validate_rest_payload(payload=[permission], expected_types=(DataProductPermission,))
        payload = permission.generate_api_payload()

        LOGGER.info("Updating a data product permission.")
        response = self.put(
            url="/dps/integration/data-products/v1/data-products/permissions/",
            body=payload,
        )
        mapped_response = self._map_request_success_to_job_details(response if response else None)
        return JobDetails.from_api_response(mapped_response)

    def delete_permission(self, permission: DataProductPermission) -> JobDetails:
        """Remove a Data Products permission assignment from a subject.

        Args:
            permission (DataProductPermission): Assignment to remove, identified
                by subject_type, subject_id, object_type, object_id, and role.

        Returns:
            JobDetails: Deletion status and any response message from the API.
        """
        if permission is None:
            raise InvalidPostBody("'permission' is required for the Data Products request.")

        validate_rest_payload(payload=[permission], expected_types=(DataProductPermission,))
        payload = permission.generate_api_payload()

        LOGGER.info("Deleting a data product permission.")
        response = self.delete(
            url="/dps/integration/data-products/v1/data-products/permissions/",
            body=payload,
        )
        return JobDetails.from_api_response(response)

    def get_user_permissions(self) -> list[DataProductPermission]:
        """Retrieve the authenticated user's effective Data Products permissions.

        Args:
            None: Uses the access token configured on this client.

        Returns:
            list[DataProductPermission]: Effective permission assignments for the
            authenticated user. Returns an empty list if no permissions are found.
        """
        LOGGER.info("Fetching effective data product permissions for the authenticated user.")
        response = self.get(
            url="/dps/integration/data-products/v1/data-products/check-permissions/",
            pagination=False,
        )

        if response:
            return [DataProductPermission.from_api_response(item) for item in response]
        return []
