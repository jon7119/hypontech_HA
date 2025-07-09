"""Constantes pour l'intégration Hypontech."""
from datetime import timedelta

DOMAIN = "hypontech"

# Configuration
CONF_USERNAME = "username"
DEFAULT_SCAN_INTERVAL = timedelta(minutes=1)

# API
API_BASE_URL = "https://api.hypon.cloud/v2"
API_LOGIN_URL = f"{API_BASE_URL}/login"
API_OVERVIEW_URL = f"{API_BASE_URL}/plant/overview"

# Capteurs
SENSOR_TYPES = {
    "e_total": {
        "name": "Énergie Totale",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "e_today": {
        "name": "Énergie Aujourd'hui",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "total_co2": {
        "name": "CO2 Évité Total",
        "unit": "kg",
        "icon": "mdi:molecule-co2",
        "device_class": None,
        "state_class": "total_increasing",
    },
    "total_tree": {
        "name": "Arbres Équivalents",
        "unit": "arbres",
        "icon": "mdi:tree",
        "device_class": None,
        "state_class": "total_increasing",
    },
    "power": {
        "name": "Puissance Actuelle",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "percent": {
        "name": "Pourcentage de Puissance",
        "unit": "%",
        "icon": "mdi:percent",
        "device_class": None,
        "state_class": "measurement",
    },
    "normal_dev_num": {
        "name": "Appareils Normaux",
        "unit": None,
        "icon": "mdi:check-circle",
        "device_class": None,
        "state_class": "measurement",
    },
    "offline_dev_num": {
        "name": "Appareils Hors Ligne",
        "unit": None,
        "icon": "mdi:close-circle",
        "device_class": None,
        "state_class": "measurement",
    },
    "fault_dev_num": {
        "name": "Appareils en Erreur",
        "unit": None,
        "icon": "mdi:alert-circle",
        "device_class": None,
        "state_class": "measurement",
    },
    "wait_dev_num": {
        "name": "Appareils en Attente",
        "unit": None,
        "icon": "mdi:clock",
        "device_class": None,
        "state_class": "measurement",
    },
    "capacity": {
        "name": "Capacité",
        "unit": "kW",
        "icon": "mdi:gauge",
        "device_class": "power",
        "state_class": "measurement",
    },
    "earning_today": {
        "name": "Gains Aujourd'hui",
        "unit": "€",
        "icon": "mdi:currency-eur",
        "device_class": "monetary",
        "state_class": "total_increasing",
    },
    "earning_total": {
        "name": "Gains Totaux",
        "unit": "€",
        "icon": "mdi:currency-eur",
        "device_class": "monetary",
        "state_class": "total_increasing",
    },
} 