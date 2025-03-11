"""
Config flow for Hypontech HA integration.
"""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_USERNAME,
    CONF_PASSWORD,
)
from .const import DOMAIN

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default='192.168.1.155'): str,
        vol.Required(CONF_PORT, default=1883): int,
        vol.Required(CONF_USERNAME, default='mosquitto'): str,
        vol.Required(CONF_PASSWORD, default='mosquitto'): str,
        vol.Required('hypontech_username', default='Joncharmant@hotmail.com'): str,
        vol.Required('hypontech_password', default='Aqua71150'): str,
        vol.Required('system_id', default='1332746207645638656'): str,
    }
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hypontech HA."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Hypontech HA", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
        )
