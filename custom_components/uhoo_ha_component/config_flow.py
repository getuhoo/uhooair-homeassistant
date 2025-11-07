import logging
import voluptuous as vol
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.config_entries import (
    CONN_CLASS_CLOUD_POLL,
    ConfigFlow
)
from .const import DOMAIN, LOGGER
from typing import Any, Dict, Optional
from .uhooapi.client import Client
from .uhooapi.errors import UnauthorizedError

class UhooFlowHandler(ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize the config flow"""
        self._errors = {}
        self.data_schema = vol.Schema(
            { vol.Required(CONF_API_KEY): str }
        )

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Handle the start of the config flow."""
        self._errors = {}

        # only a single instance of this integration is allowed
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input == None:
            user_input = {}
            user_input[CONF_API_KEY] = ""
            return await self._show_config_form(user_input)

        valid = await self._test_credentials(
            user_input[CONF_API_KEY]
        )
        if valid: 
            return self.async_create_entry(
                title=user_input[CONF_API_KEY], data=user_input
            )
        else:
            self._errors["base"] = "auth"
        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input: Optional[Dict[str, Any]] = None):
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY, default=user_input[CONF_API_KEY]): str
                }
            ),
            errors=self._errors
        )
        
    async def _test_credentials(self, api_key):
        """Return true if credentials is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = Client(api_key, session)
            await client.login()
            return True
        except UnauthorizedError as err:
            LOGGER.error(
                f"Error: received a 401 Unauthorized error attempting to login:\n{err}"
            )
        except Exception as err:
            LOGGER.error(f"Error: exception while attempting to login:\n{err}")
        return False