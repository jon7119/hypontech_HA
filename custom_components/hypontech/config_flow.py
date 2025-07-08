"""Configuration de l'intégration Hypontech."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_USERNAME
from .hypontech_api import HypontechAPI


class HypontechConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gestionnaire de configuration pour Hypontech."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Étape de configuration utilisateur."""
        errors = {}

        if user_input is not None:
            try:
                # Test de connexion
                api = HypontechAPI(
                    user_input[CONF_EMAIL],
                    user_input[CONF_PASSWORD],
                    user_input.get(CONF_USERNAME, user_input[CONF_EMAIL])
                )
                
                # Test de l'authentification
                await api._login()
                
                # Création de l'entrée de configuration
                return self.async_create_entry(
                    title=f"Hypontech - {user_input[CONF_EMAIL]}",
                    data=user_input,
                )
                
            except Exception as ex:
                errors["base"] = "cannot_connect"
                _LOGGER.error(f"Erreur de configuration: {ex}")

        # Schéma de configuration
        data_schema = vol.Schema(
            {
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Optional(CONF_USERNAME): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "email": "Votre email de connexion Hypontech",
                "password": "Votre mot de passe Hypontech",
                "username": "Nom d'utilisateur (optionnel, utilise l'email par défaut)",
            },
        )


class CannotConnect(HomeAssistantError):
    """Erreur de connexion à l'API Hypontech."""


class InvalidAuth(HomeAssistantError):
    """Erreur d'authentification Hypontech.""" 