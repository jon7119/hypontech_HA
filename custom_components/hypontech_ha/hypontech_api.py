"""API client pour Hypontech."""
import asyncio
import logging
from typing import Any, Dict

import aiohttp
import async_timeout

from .const import API_LOGIN_URL, API_OVERVIEW_URL, API_BASE_URL

_LOGGER = logging.getLogger(__name__)


class HypontechAPI:
    """Client API pour Hypontech."""

    def __init__(self, username: str, password: str, plant_id: str):
        """Initialisation du client API."""
        self._username = username
        self._password = password
        self._plant_id = plant_id
        self._auth_token = None
        self._session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Obtient ou crée une session HTTP."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _login(self) -> bool:
        """Authentification auprès de l'API Hypontech."""
        session = await self._get_session()
        
        login_data = {
            "password": self._password,
            "username": self._username
        }

        try:
            async with async_timeout.timeout(10):
                async with session.post(API_LOGIN_URL, json=login_data) as response:
                    if response.status == 200:
                        data = await response.json()
                        self._auth_token = data['data']['token']
                        _LOGGER.debug("Authentification réussie")
                        return True
                    else:
                        _LOGGER.error(f"Erreur d'authentification: {response.status}")
                        return False
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout lors de l'authentification")
            return False
        except Exception as e:
            _LOGGER.error(f"Erreur lors de l'authentification: {e}")
            return False

    async def _get_overview_data(self) -> Dict[str, Any]:
        """Récupère les données d'aperçu de l'installation."""
        if not self._auth_token:
            if not await self._login():
                raise Exception("Impossible de s'authentifier")

        session = await self._get_session()
        headers = {"Authorization": f"Bearer {self._auth_token}"}

        try:
            async with async_timeout.timeout(10):
                async with session.get(API_OVERVIEW_URL, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['data']
                    elif response.status == 401:
                        # Token expiré, nouvelle authentification
                        _LOGGER.debug("Token expiré, nouvelle authentification")
                        self._auth_token = None
                        if await self._login():
                            return await self._get_overview_data()
                        else:
                            raise Exception("Impossible de se réauthentifier")
                    else:
                        _LOGGER.error(f"Erreur API: {response.status}")
                        raise Exception(f"Erreur API: {response.status}")
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout lors de la récupération des données")
            raise Exception("Timeout lors de la récupération des données")
        except Exception as e:
            _LOGGER.error(f"Erreur lors de la récupération des données: {e}")
            raise

    async def _get_production2_data(self) -> Dict[str, Any]:
        """Récupère les données de production détaillées de l'installation."""
        if not self._auth_token:
            if not await self._login():
                raise Exception("Impossible de s'authentifier")

        session = await self._get_session()
        headers = {"Authorization": f"Bearer {self._auth_token}"}
        
        # Construction de l'URL avec le plant_id dynamique
        production2_url = f"{API_BASE_URL}/plant/{self._plant_id}/production2"

        try:
            async with async_timeout.timeout(10):
                async with session.get(production2_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['data']
                    elif response.status == 401:
                        # Token expiré, nouvelle authentification
                        _LOGGER.debug("Token expiré, nouvelle authentification")
                        self._auth_token = None
                        if await self._login():
                            return await self._get_production2_data()
                        else:
                            raise Exception("Impossible de se réauthentifier")
                    else:
                        _LOGGER.error(f"Erreur API production2: {response.status}")
                        raise Exception(f"Erreur API production2: {response.status}")
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout lors de la récupération des données de production")
            raise Exception("Timeout lors de la récupération des données de production")
        except Exception as e:
            _LOGGER.error(f"Erreur lors de la récupération des données de production: {e}")
            raise

    async def async_get_data(self) -> Dict[str, Any]:
        """Récupère toutes les données de l'installation."""
        try:
            # Récupération des données d'aperçu
            overview_data = await self._get_overview_data()
            
            # Récupération des données de production détaillées
            production_data = await self._get_production2_data()
            
            # Extraction des données pertinentes de l'aperçu
            raw_power = overview_data.get('power', 0)
            
            # Correction automatique de la puissance : détection kW vs W
            corrected_power = self._correct_power_value(raw_power)
            
            relevant_data = {
                'e_total': overview_data.get('e_total', 0),
                'e_today': overview_data.get('e_today', 0),
                'total_co2': overview_data.get('total_co2', 0),
                'total_tree': overview_data.get('total_tree', 0),
                'power': corrected_power,
                'normal_dev_num': overview_data.get('normal_dev_num', 0),
                'offline_dev_num': overview_data.get('offline_dev_num', 0),
                'fault_dev_num': overview_data.get('fault_dev_num', 0),
                'wait_dev_num': overview_data.get('wait_dev_num', 0),
                'capacity': overview_data.get('capacity', 0),
            }
            
            # Ajout des données de production détaillées
            relevant_data.update({
                'today_generation': production_data.get('today_generation', 0),
                'month_generation': production_data.get('month_generation', 0),
                'year_generation': production_data.get('year_generation', 0),
                'total_generation': production_data.get('total_generation', 0),
                'co2_saved': production_data.get('co2', 0),
                'tree_equivalent': production_data.get('tree', 0),
                'diesel_saved': production_data.get('diesel', 0),
                'today_revenue': production_data.get('today_revenue', 0),
                'month_revenue': production_data.get('month_revenue', 0),
                'total_revenue': production_data.get('total_revenue', 0),
            })
            
            _LOGGER.debug(f"Données récupérées: {relevant_data}")
            return relevant_data
            
        except Exception as e:
            _LOGGER.error(f"Erreur lors de la récupération des données: {e}")
            raise

    def _correct_power_value(self, raw_power: float) -> float:
        """
        Normalise la valeur de puissance pour un affichage cohérent.
        
        L'API Hypontech retourne parfois la puissance en kW au lieu de W
        quand elle dépasse 1000W. Cette méthode garde les kW en kW et les W en W.
        
        Args:
            raw_power: Valeur brute de puissance de l'API
            
        Returns:
            Puissance normalisée (kW si < 10, W si >= 1000)
        """
        if raw_power is None or raw_power == 0:
            return 0
        
        # Détection des valeurs en kW (généralement < 10)
        # Exemples: 1.2kW reste 1.2kW, 2.5kW reste 2.5kW
        if raw_power < 10 and raw_power > 0:
            # Probablement en kW, on garde en kW
            _LOGGER.debug(f"Puissance détectée en kW: {raw_power}kW")
            return raw_power
        elif raw_power >= 10 and raw_power < 1000:
            # Valeur intermédiaire, vérification si c'est décimal (probablement kW)
            if raw_power != int(raw_power):
                # Valeur décimale entre 10-1000, probablement en kW
                _LOGGER.debug(f"Puissance décimale détectée en kW: {raw_power}kW")
                return raw_power
        
        # Valeur >= 1000, probablement en W, conversion en kW pour l'affichage
        if raw_power >= 1000:
            converted = raw_power / 1000
            _LOGGER.debug(f"Conversion W vers kW: {raw_power}W -> {converted}kW")
            return converted
        
        # Valeur entre 10-1000 entière, probablement en W
        return raw_power

    async def close(self):
        """Ferme la session HTTP."""
        if self._session and not self._session.closed:
            await self._session.close() 