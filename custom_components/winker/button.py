from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the door control button platform from a config entry."""
    # Get the API instance from config_entry.runtime_data
    api = config_entry.runtime_data

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
