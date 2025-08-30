import logging
from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from datetime import datetime, timedelta
import aiohttp
import os

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the custom camera platform from a config entry."""
    # Get the API instance from config_entry.runtime_data
    api = config_entry.runtime_data

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

        if self._last_image_time is not None and datetime.utcnow() - self._last_image_time < timedelta(minutes=2):
            self._last_image = await self.get_image_bytes(self._camera_url)
            if self._last_image is not None:
                _LOGGER.debug("Updating image")
                self._last_image_time = datetime.utcnow()
                self._streaming = True
                return self._last_image

        if self._last_image is None:
            self._last_image = await self.get_image_bytes(self._camera_url)
            _LOGGER.debug("Updating image")
            self._last_image_time = datetime.utcnow()
            self._streaming = True
            return self._last_image

        return None

    async def get_image_bytes(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'Authorization': self._camera_token}) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    _LOGGER.error(f"Failed to fetch image for camera {self._name}: {response.status}")
                    return None

