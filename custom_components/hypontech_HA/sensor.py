"""
Support for Hypontech HA sensors.
"""

import logging
import time
import requests
import paho.mqtt.client as mqtt

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT,
)
from homeassistant.helpers.entity import DeviceInfo

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

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    sensors = [HypontechSensor(sensor_id, config) for sensor_id, config in SENSORS.items()]
    async_add_entities(sensors)
    publish_mqtt_discovery()

class HypontechSensor(SensorEntity):
    """Representation of a Hypontech sensor."""

    def __init__(self, sensor_id, config):
        """Initialize the sensor."""
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
        try:
            url = "https://api.hypon.cloud/v2/login"
            data = {
                "email": "Joncharmant@hotmail.com",
                "password": "Aqua71150",
                "username": "Joncharmant@hotmail.com"
            }
            response = await self.hass.async_add_executor_job(requests.post, url, None, data)
            if response.status_code == 200:
                auth_token = response.json()['data']['token']
                headers = {
                    "Authorization": f"Bearer {auth_token}"
                }
                response = await self.hass.async_add_executor_job(requests.get, "https://api.hypon.cloud/v2/plant/overview", None, headers)
                if response.status_code == 200:
                    data = response.json()
                    relevant_data = {
                        'e_total': data['data']['e_total'],
                        'e_today': data['data']['e_today'],
                        'power': data['data']['power'],
                        'percent': data['data']['percent']
                    }
                    publish_mqtt_state(relevant_data)
                    self._state = relevant_data[self._sensor_id]
                else:
                    _LOGGER.error('Erreur API: %s', response.status_code)
            else:
                _LOGGER.error('Erreur API: %s', response.status_code)
        except Exception as e:
            _LOGGER.error('Erreur: %s', str(e))

def publish_mqtt_discovery():
    """Publish MQTT discovery messages."""
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

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
