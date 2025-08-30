from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from .winker_api import WinkerAPI  # Import the API class
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the door control button platform dynamically."""
    # Initialize the API instance here (or pass it in as a parameter)
    api = WinkerAPI()

    # Fetch button details from the API
    doors = await api.fetch_doors()  # This function should return the details for each door (e.g., ID, name)
    _LOGGER.error("setup platform")
    # Create a list of DoorControlButton entities based on the API data
    buttons = [DoorControlButton(api, door) for door in doors]

    # Add buttons to Home Assistant
    async_add_entities(buttons)

class DoorControlButton(ButtonEntity):
    """Representation of a Button to open a specific door."""

    def __init__(self, api, door):
        """Initialize the door control button."""
        self._api = api
        self._door = door
        self._name = f"Open {door['name_device'].title()}"

    @property
    def name(self):
        """Return the name of the button."""
        return self._name

    async def async_press(self):
        """Handle the button press action."""
        # Use door_info to send the correct API request
        door_id = self._door['id_device']
        _LOGGER.info(f"Opening door {self._name} (ID: {door_id})")
        await self._api.open_door(self._door)
