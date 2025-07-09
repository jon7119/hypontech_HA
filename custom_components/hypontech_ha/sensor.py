"""Capteurs pour l'intégration Hypontech."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_EMAIL,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, SENSOR_TYPES


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration des capteurs Hypontech."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(HypontechSensor(coordinator, sensor_type, config_entry))

    async_add_entities(entities)


class HypontechSensor(CoordinatorEntity, SensorEntity):
    """Représentation d'un capteur Hypontech."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        sensor_type: str,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialisation du capteur."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._config_entry = config_entry
        self._attr_name = f"Hypontech {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name="Hypontech Solar",
            manufacturer="Hypontech",
            model="Solar Inverter",
            configuration_url="https://hypon.cloud",
        )

    @property
    def native_value(self) -> StateType:
        """Retourne la valeur native du capteur."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._sensor_type, 0)

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Retourne l'unité de mesure du capteur."""
        return SENSOR_TYPES[self._sensor_type]["unit"]

    @property
    def icon(self) -> str | None:
        """Retourne l'icône du capteur."""
        return SENSOR_TYPES[self._sensor_type]["icon"]

    @property
    def device_class(self) -> str | None:
        """Retourne la classe du dispositif."""
        return SENSOR_TYPES[self._sensor_type]["device_class"]

    @property
    def state_class(self) -> SensorStateClass | None:
        """Retourne la classe d'état du capteur."""
        state_class = SENSOR_TYPES[self._sensor_type]["state_class"]
        if state_class == "total_increasing":
            return SensorStateClass.TOTAL_INCREASING
        elif state_class == "measurement":
            return SensorStateClass.MEASUREMENT
        return None

    @property
    def available(self) -> bool:
        """Retourne si le capteur est disponible."""
        return self.coordinator.last_update_success 