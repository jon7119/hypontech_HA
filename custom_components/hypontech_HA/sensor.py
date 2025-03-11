"""
Support for Hypontech HA sensors.
"""

import logging
import time
import requests
import paho.mqtt.client as mqtt
import voluptuous as vol
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_HOST,
    CONF_PORT,
    CONF_USERNAME,
    CONF_PASSWORD,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    CONF_HYPONTECH_USERNAME,
    CONF_HYPONTECH_PASSWORD,
    CONF_SYSTEM_ID,
)

_LOGGER = logging.getLogger(__name__)

MQTT_BROKER = '192.168.1.155'
MQTT_PORT = 1883
MQTT_USERNAME = 'mosquitto'
MQTT_PASSWORD = 'mosquitto'
MQTT_DISCOVERY_PREFIX = 'homeassistant'
DEVICE_NAME = 'hypontec'

SENSORS = {
    'e_total': {'name': 'Energy Total', 'unit': 'kWh', 'icon': 'mdi:chart-line'},
    'e_today': {'name': 'Energy Today', 'unit': 'kWh', 'icon': 'mdi:solar-power'},
    'power': {'name': 'Power', 'unit': 'W', 'icon': 'mdi:flash'},
    'percent': {'name': 'Percentage', 'unit': '%', 'icon': 'mdi:percent'}
}

class HypontechDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Hypontech data."""

    def __init__(self, hass, config):
        """Initialize global Hypontech data updater."""
        self.hass = hass
        self.config = config

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )

    async def _async_update_data(self):
        """Fetch data from Hypontech API."""
        try:
            url = "https://api.hypon.cloud/v2/login"
            data = {
                "email": self.config[CONF_HYPONTECH_USERNAME],
                "password": self.config[CONF_HYPONTECH_PASSWORD],
                "username": self.config[CONF_HYPONTECH_USERNAME],
            }
            _LOGGER.debug("Envoi de la requête de connexion à l'API avec les données: %s", data)
            response = await self.hass.async_add_executor_job(requests.post, url, None, data)
            response.raise_for_status()
            auth_token = response.json()['data']['token']
            _LOGGER.debug("Token d'authentification reçu: %s", auth_token)
            headers = {
                "Authorization": f"Bearer {auth_token}"
            }
            response = await self.hass.async_add_executor_job(requests.get, "https://api.hypon.cloud/v2/plant/overview", None, headers)
            response.raise_for_status()
            _LOGGER.debug("Données reçues de l'API: %s", response.json())
            return response.json()
        except requests.HTTPError as http_err:
            _LOGGER.error('Erreur HTTP: %s', str(http_err))
        except Exception as e:
            _LOGGER.error('Erreur: %s', str(e))

        return None

class HypontechSensor(SensorEntity):
    """Representation of a Hypontech sensor."""

    def __init__(self, coordinator, sensor_id, config):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._sensor_id = sensor_id
        self._name = config['name']
        self._unit_of_measurement = config['unit']
        self._icon = config['icon']
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f'{DEVICE_NAME}_{self._sensor_id}'

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self):
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, DEVICE_NAME)},
            name='Hypontec System',
            manufacturer='Hypontec'
        )

    async def async_update(self):
        """Fetch new state data for the sensor."""
        await self.coordinator.async_request_refresh()
        data = self.coordinator.data
        if data:
            relevant_data = {
                'e_total': data['data']['e_total'],
                'e_today': data['data']['e_today'],
                'power': data['data']['power'],
                'percent': data['data']['percent']
            }
            publish_mqtt_state(relevant_data)
            self._state = relevant_data[self._sensor_id]

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    coordinator = HypontechDataUpdateCoordinator(hass, config)
    await coordinator.async_config_entry_first_refresh()

    sensors = [HypontechSensor(coordinator, sensor_id, config) for sensor_id, config in SENSORS.items()]
    async_add_entities(sensors)

    publish_mqtt_discovery(config)

def publish_mqtt_discovery(config):
    """Publish MQTT discovery messages."""
    client = mqtt.Client()
    client.username_pw_set(config[CONF_USERNAME], config[CONF_PASSWORD])
    client.connect(config[CONF_HOST], config[CONF_PORT], 60)

    for sensor_id, config in SENSORS.items():
        topic = f'{MQTT_DISCOVERY_PREFIX}/sensor/{DEVICE_NAME}/{sensor_id}/config'
        payload = {
            'name': config['name'],
            'unit_of_measurement': config['unit'],
            'state_topic': f'{DEVICE_NAME}/state',
            'value_template': f'{{{{ value_json.{sensor_id} }}}}',
            'unique_id': f'{DEVICE_NAME}_{sensor_id}',
            'device': {
                'identifiers': [DEVICE_NAME],
                'name': 'Hypontec System',
                'manufacturer': 'Hypontec'
            },
            'icon': config['icon']
        }
        client.publish(topic, str(payload), retain=True)

    client.disconnect()

def publish_mqtt_state(data):
    """Publish MQTT state messages."""
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(f'{DEVICE_NAME}/state', str(data))
    client.disconnect()
