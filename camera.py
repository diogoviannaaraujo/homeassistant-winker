import logging
from homeassistant.components.camera import Camera
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from datetime import datetime, timedelta
from .winker_api import WinkerAPI  # Import the API class
import aiohttp
import os

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass: HomeAssistant, config, async_add_entities: AddEntitiesCallback, discovery_info=None):
    """Set up the custom camera platform."""
    _LOGGER.error("Setting up the camera platform")
    api = WinkerAPI()

    cameras = await api.fetch_cameras()

    entities = [ControlCamera(api, camera) for camera in cameras]
    async_add_entities(entities)

class ControlCamera(Camera):
    def __init__(self, api, camera):
        super().__init__()
        self._name = camera['name']
        self._api = api
        self._camera = camera
        self._camera_id = camera['id_camera']
        self._camera_url = camera['url']
        self._camera_token = camera['authorization']
        self._streaming = False  # Indicates if the camera is streaming
        self._last_image = None
        self._last_image_time = None

    @property
    def name(self):
        return self._name

    @property
    def is_streaming(self):
        return self._streaming
    
    @property
    def frame_interval(self):
        return 1.1

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return the image stream from the camera."""
        _LOGGER.debug("Getting image from camera")

        if self._camera is None:
            _LOGGER.error("Error getting image from camera")
            return None

        if self._last_image_time is not None and datetime.utcnow() - self._last_image_time < timedelta(minutes=2) and self._camera['jpg'] is not None:
            _LOGGER.debug("No need to check camera status")
            self._last_image = await self.get_image_bytes(self._camera['jpg'])
            if self._last_image is not None:
                _LOGGER.debug("Updating image")
                self._last_image_time = datetime.utcnow()
                self._streaming = True
                return self._last_image

        if (self._camera['status'] == "started" and self._camera['jpg'] is not None):
            self._last_image = await self.get_image_bytes(self._camera['jpg'])
            _LOGGER.debug("Updating image")
            self._last_image_time = datetime.utcnow()
            self._streaming = True
            return self._last_image

        return None

    async def get_image_bytes(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._camera_url, headers={'Authorization': self._camera_token}) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    _LOGGER.error(f"Failed to fetch image for camera {self._name}: {response.status}")
                    return None

