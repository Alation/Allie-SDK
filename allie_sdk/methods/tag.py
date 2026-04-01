"""Alation REST API Tag Methods."""

import logging
from urllib.parse import quote

import requests

from ..core.custom_exceptions import InvalidPostBody, validate_query_params, validate_rest_payload
from ..core.request_handler import RequestHandler
from ..models.job_model import JobDetails
from ..models.tag_model import Tag, TagItem, TagObjectItem, TagParams, TaggedObject, TaggedObjectParams

LOGGER = logging.getLogger("allie_sdk_logger")


class AlationTag(RequestHandler):
    """Alation REST API Tag Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Tag object."""
        super().__init__(session=session, host=host, access_token=access_token)

    @staticmethod
    def _encode_tag_name(tag_name: str) -> str:
        if not tag_name:
            raise InvalidPostBody("'tag_name' must be provided.")
        return quote(tag_name, safe="")

    def get_tags(self, query_params: TagParams = None) -> list[Tag]:
        """Get tags in the Alation catalog.

        Args:
            query_params (TagParams, optional): Filters for listing tags, including object scoping.

        Returns:
            list[Tag]: Matching tags.
        """
        validate_query_params(query_params, TagParams)
        params = query_params.generate_params_dict() if query_params else None

        tags = self.get(
            url="/integration/tag/",
            query_params=params,
            pagination=False,
        )

        if tags:
            return [Tag.from_api_response(tag) for tag in tags]
        return []

    def get_a_tag(self, tag_id: int) -> Tag:
        """Get the details of a specific tag.

        Args:
            tag_id (int): Tag identifier.

        Returns:
            Tag: Tag details.
        """
        if tag_id is None:
            raise InvalidPostBody("'tag_id' must be provided to retrieve a tag.")

        tag = self.get(
            url=f"/integration/tag/{tag_id}/",
            pagination=False,
        )

        return Tag.from_api_response(tag)

    def get_objects_tagged_with_specific_tag(
        self, tag_name: str, query_params: TaggedObjectParams = None
    ) -> list[TaggedObject]:
        """Get all objects tagged with a specific tag.

        Args:
            tag_name (str): Tag name. Special characters are URL encoded automatically.
            query_params (TaggedObjectParams, optional): Filters for the tagged object list.

        Returns:
            list[TaggedObject]: Tagged objects for the supplied tag name.
        """
        validate_query_params(query_params, TaggedObjectParams)
        params = query_params.generate_params_dict() if query_params else None
        encoded_tag_name = self._encode_tag_name(tag_name)

        objects = self.get(
            url=f"/integration/tag/{encoded_tag_name}/subject/",
            query_params=params,
            pagination=False,
        )

        if objects:
            return [TaggedObject.from_api_response(object) for object in objects]
        return []

    def add_tag_to_object(self, tag_name: str, object: TagObjectItem) -> Tag:
        """Add a tag to an object.

        Args:
            tag_name (str): Tag name. The tag is created automatically if it does not exist yet.
            object (TagObjectItem): Target object to tag.

        Returns:
            Tag: The created or reused tag.
        """
        encoded_tag_name = self._encode_tag_name(tag_name)
        validate_rest_payload(payload=[object], expected_types=(TagObjectItem,))

        payload = object.generate_api_post_payload()
        tag_response = self.post(
            url=f"/integration/tag/{encoded_tag_name}/subject/",
            body=payload,
        )

        return Tag.from_api_response(tag_response)

    def update_tag(self, tag_id: int, tag: TagItem) -> Tag:
        """Update a tag name or description.

        Args:
            tag_id (int): Tag identifier.
            tag (TagItem): New tag values to persist.

        Returns:
            Tag: Updated tag details.
        """
        if tag_id is None:
            raise InvalidPostBody("'tag_id' must be provided to update a tag.")

        validate_rest_payload(payload=[tag], expected_types=(TagItem,))
        payload = tag.generate_api_patch_payload()
        tag_response = self.patch(
            url=f"/integration/tag/{tag_id}/",
            body=payload,
        )

        return Tag.from_api_response(tag_response)

    def remove_tag_from_object(self, tag_name: str, otype: str, oid: int | str) -> JobDetails:
        """Remove a tag from an object.

        Args:
            tag_name (str): Tag name. Special characters are URL encoded automatically.
            otype (str): Object type.
            oid (int | str): Object identifier.

        Returns:
            JobDetails: Success or failure details for the delete request.
        """
        encoded_tag_name = self._encode_tag_name(tag_name)

        if not otype:
            raise InvalidPostBody("'otype' must be provided to remove a tag from an object.")
        if oid is None:
            raise InvalidPostBody("'oid' must be provided to remove a tag from an object.")

        delete_response = self.delete(
            url=f"/integration/tag/{encoded_tag_name}/subject/{otype}/{oid}/",
            is_async=False,
        )

        if isinstance(delete_response, dict):
            return JobDetails.from_api_response(delete_response)

        return JobDetails(status="successful", msg="", result=delete_response)
