"""Configuration de l'intégration Hypontech."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_USERNAME, CONF_PLANT_ID
from .hypontech_api import HypontechAPI

_LOGGER = logging.getLogger(__name__)


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
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                    user_input[CONF_PLANT_ID]
                )
                
                # Test de l'authentification
                await api._login()
                
                # Création de l'entrée de configuration
                return self.async_create_entry(
                    title=f"Hypontech - {user_input[CONF_USERNAME]}",
                    data=user_input,
                )
                
            except Exception as ex:
                errors["base"] = "cannot_connect"
                _LOGGER.error(f"Erreur de configuration: {ex}")

        # Schéma de configuration
        data_schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_PLANT_ID): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "username": "Votre nom d'utilisateur Hypontech",
                "password": "Votre mot de passe Hypontech",
                "plant_id": "ID de votre installation (ex: 1332746207645638656)",
            },
        )

    async def async_step_reauth(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Étape de reconfiguration des identifiants."""
        errors = {}

        if user_input is not None:
            try:
                # Test de connexion avec les nouveaux identifiants
                api = HypontechAPI(
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                    user_input[CONF_PLANT_ID]
                )
                
                # Test de l'authentification
                await api._login()
                
                # Mise à jour de l'entrée de configuration existante
                existing_entry = self._get_existing_entry()
                if existing_entry:
                    self.hass.config_entries.async_update_entry(
                        existing_entry,
                        data=user_input,
                        title=f"Hypontech - {user_input[CONF_USERNAME]}"
                    )
                    await self.hass.config_entries.async_reload(existing_entry.entry_id)
                    return self.async_abort(reason="reauth_successful")
                
            except Exception as ex:
                errors["base"] = "cannot_connect"
                _LOGGER.error(f"Erreur de reconfiguration: {ex}")

        # Schéma de reconfiguration avec les valeurs actuelles pré-remplies
        existing_entry = self._get_existing_entry()
        current_data = existing_entry.data if existing_entry else {}
        
        data_schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME, default=current_data.get(CONF_USERNAME, "")): str,
                vol.Required(CONF_PASSWORD, default=""): str,  # Mot de passe vide pour sécurité
                vol.Required(CONF_PLANT_ID, default=current_data.get(CONF_PLANT_ID, "")): str,
            }
        )

        return self.async_show_form(
            step_id="reauth",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "username": "Votre nom d'utilisateur Hypontech",
                "password": "Votre mot de passe Hypontech",
                "plant_id": "ID de votre installation (ex: 1332746207645638656)",
            },
        )

    def _get_existing_entry(self):
        """Récupère l'entrée de configuration existante."""
        for entry in self.hass.config_entries.async_entries(DOMAIN):
            if entry.source == config_entries.SOURCE_USER:
                return entry
        return None


class CannotConnect(HomeAssistantError):
    """Erreur de connexion à l'API Hypontech."""


class InvalidAuth(HomeAssistantError):
    """Erreur d'authentification Hypontech.""" 