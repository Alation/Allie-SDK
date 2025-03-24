import logging
import requests

from ..core.request_handler import RequestHandler
# from ..core.async_handler import AsyncHandler
from ..core.custom_exceptions import *
from ..models.visual_config_model import *
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationVisualConfig(RequestHandler):
    """Alation REST API Visual Config Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Documents  object.
        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
        """
        super().__init__(session=session, host=host, access_token=access_token)

    def get_visual_configs(self) -> list[VisualConfig]:
        """Query multiple Alation Visual Configs and return their details

        Args:


        Returns:
            list[VisualConfig]: List of Visual Configs

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """

        visual_configs = self.get('/integration/visual_config/')

        if visual_configs:
            visual_configs_checked = [VisualConfig.from_api_response(v) for v in visual_configs]
            return visual_configs_checked
        return []

    def get_a_visual_config(self, visual_config_id:int) -> VisualConfig:
        """Query multiple Alation Visual Configs and return their details

        Args:
            visual_config_id: Alation Visual Config ID.

        Returns:
            VisualConfig: an Alation Visual Config

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """

        visual_config = self.get(f'/integration/visual_config/{visual_config_id}/')

        if visual_config:
            visual_config_checked = VisualConfig.from_api_response(visual_config)
            return visual_config_checked


