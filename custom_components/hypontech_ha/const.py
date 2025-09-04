"""Constantes pour l'intégration Hypontech."""
from datetime import timedelta

DOMAIN = "hypontech_ha"

# Configuration
CONF_USERNAME = "username"
DEFAULT_SCAN_INTERVAL = timedelta(minutes=1)

# API
API_BASE_URL = "https://api.hypon.cloud/v2"
API_LOGIN_URL = f"{API_BASE_URL}/login"
API_OVERVIEW_URL = f"{API_BASE_URL}/plant/overview"
API_PRODUCTION2_URL = f"{API_BASE_URL}/plant/1332746207645638656/production2"

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
    # Nouveaux capteurs pour l'endpoint production2
    "today_generation": {
        "name": "Génération Aujourd'hui",
        "unit": "kWh",
        "icon": "mdi:solar-panel",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "month_generation": {
        "name": "Génération du Mois",
        "unit": "kWh",
        "icon": "mdi:calendar-month",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "year_generation": {
        "name": "Génération de l'Année",
        "unit": "kWh",
        "icon": "mdi:calendar-year",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "total_generation": {
        "name": "Génération Totale",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt-circle",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "co2_saved": {
        "name": "CO2 Évité",
        "unit": "kg",
        "icon": "mdi:molecule-co2",
        "device_class": None,
        "state_class": "total_increasing",
    },
    "tree_equivalent": {
        "name": "Équivalent Arbres",
        "unit": "arbres",
        "icon": "mdi:tree",
        "device_class": None,
        "state_class": "total_increasing",
    },
    "diesel_saved": {
        "name": "Diesel Économisé",
        "unit": "L",
        "icon": "mdi:fuel",
        "device_class": None,
        "state_class": "total_increasing",
    },
    "today_revenue": {
        "name": "Revenus Aujourd'hui",
        "unit": "€",
        "icon": "mdi:currency-eur",
        "device_class": "monetary",
        "state_class": "total_increasing",
    },
    "month_revenue": {
        "name": "Revenus du Mois",
        "unit": "€",
        "icon": "mdi:calendar-month",
        "device_class": "monetary",
        "state_class": "total_increasing",
    },
    "total_revenue": {
        "name": "Revenus Totaux",
        "unit": "€",
        "icon": "mdi:bank",
        "device_class": "monetary",
        "state_class": "total_increasing",
    },
} 
