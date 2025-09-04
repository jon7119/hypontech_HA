"""Intégration Hypontech pour Home Assistant."""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    Platform,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    CONF_USERNAME,
    CONF_PLANT_ID,
)
from .hypontech_api import HypontechAPI

_LOGGER = logging.getLogger(__name__)

# Pas de configuration YAML - configuration via l'interface graphique uniquement

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configuration de l'intégration Hypontech."""
    hass.data.setdefault(DOMAIN, {})

    # Récupération des données de configuration
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    plant_id = entry.data[CONF_PLANT_ID]
    scan_interval = entry.options.get("scan_interval", entry.data.get("scan_interval", 60))
    if isinstance(scan_interval, int):
        scan_interval = timedelta(seconds=scan_interval)

    # Création de l'API client
    api = HypontechAPI(username, password, plant_id)

    # Création du coordinateur de données
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=api.async_get_data,
        update_interval=scan_interval,
    )

    # Test de connexion initial
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as ex:
        raise ConfigEntryNotReady(f"Impossible de se connecter à l'API Hypontech: {ex}") from ex

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Configuration des plateformes
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Déchargement de l'intégration Hypontech."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok 