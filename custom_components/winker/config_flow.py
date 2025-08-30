"""Config flow for Winker integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .winker_api import WinkerAPI

_LOGGER = logging.getLogger(__name__)

DOMAIN = "winker"

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class WinkerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Winker."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]

            # Create API instance and try to authenticate
            api = WinkerAPI()
            try:
                token = await api.authenticate(email, password)
                if token:
                    # Authentication successful, create the config entry
                    await self.async_set_unique_id(email)
                    self._abort_if_unique_id_configured()
                    
                    return self.async_create_entry(
                        title=f"Winker ({email})",
                        data={
                            CONF_EMAIL: email,
                            "token": token,
                        },
                    )
                else:
                    errors["base"] = "invalid_auth"
                    
            except Exception as exception:
                _LOGGER.error("Unexpected exception: %s", exception)
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
