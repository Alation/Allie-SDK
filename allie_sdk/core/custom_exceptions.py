"""Custom Exceptions to use across the SDK."""


class UnsupportedQueryParams(Exception):
    pass


class UnsupportedPostBody(Exception):
    pass


class InvalidPostBody(Exception):
    pass


def validate_query_params(parameters: any, expected_type: any):
    """Validate the Query Parameters used in an Alation REST API Call.

    Args:
        parameters (any): Parameter Dataclass Object to be checked.
        expected_type (any): Expected Dataclass Object Type.

    """
    if parameters and not isinstance(parameters, expected_type):
        raise UnsupportedQueryParams(
            f"Unsupported type '{type(parameters)}' was passed for API Query Parameters\n"
            f"Please use '{'.'.join((expected_type.__module__, expected_type.__qualname__))}'")


def validate_rest_payload(payload: list, expected_types: tuple):
    """Validate the Body used in an Alation REST API Call.

    Args:
        payload (list): Payload Body Dataclass Objects to be checked.
        expected_types (tuple): Expected Dataclass Object Type.

    """
    type_locations = ""
    for object_type in expected_types:
        type_locations += f"- {'.'.join((object_type.__module__, object_type.__qualname__))}\n"

    for item in payload:
            if not isinstance(item, tuple(expected_types)):
                raise UnsupportedPostBody(
                    f"Unsupported type '{type(item)}' was passed for API Body Payload\n"
                    f"Please use:\n {type_locations}")
