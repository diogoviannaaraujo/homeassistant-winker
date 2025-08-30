"""The Winker integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .winker_api import WinkerAPI

DOMAIN = "winker"
PLATFORMS: list[Platform] = [Platform.BUTTON, Platform.CAMERA]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Winker from a config entry."""
    # Create API instance with the stored token
    token = entry.data.get("token")
    api = WinkerAPI(token=token)
    
    # Store the API instance in entry.runtime_data (modern best practice)
    entry.runtime_data = api
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # No need to manually clean up entry.runtime_data - it's automatic
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

