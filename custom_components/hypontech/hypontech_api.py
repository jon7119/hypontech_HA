"""API client pour Hypontech."""
import asyncio
import logging
from typing import Any, Dict

import aiohttp
import async_timeout

from .const import API_LOGIN_URL, API_OVERVIEW_URL

_LOGGER = logging.getLogger(__name__)


class HypontechAPI:
    """Client API pour Hypontech."""

    def __init__(self, email: str, password: str, username: str):
        """Initialisation du client API."""
        self._email = email
        self._password = password
        self._username = username
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
            "email": self._email,
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

    async def async_get_data(self) -> Dict[str, Any]:
        """Récupère toutes les données de l'installation."""
        try:
            data = await self._get_overview_data()
            
            # Extraction des données pertinentes
            relevant_data = {
                'e_total': data.get('e_total', 0),
                'e_today': data.get('e_today', 0),
                'total_co2': data.get('total_co2', 0),
                'total_tree': data.get('total_tree', 0),
                'power': data.get('power', 0),
                'percent': data.get('percent', 0),
                'normal_dev_num': data.get('normal_dev_num', 0),
                'offline_dev_num': data.get('offline_dev_num', 0),
                'fault_dev_num': data.get('fault_dev_num', 0),
                'wait_dev_num': data.get('wait_dev_num', 0),
                'capacity': data.get('capacity', 0),
                'earning_today': data.get('earning', [{}])[0].get('today', 0) if data.get('earning') else 0,
                'earning_total': data.get('earning', [{}])[0].get('total', 0) if data.get('earning') else 0,
            }
            
            _LOGGER.debug(f"Données récupérées: {relevant_data}")
            return relevant_data
            
        except Exception as e:
            _LOGGER.error(f"Erreur lors de la récupération des données: {e}")
            raise

    async def close(self):
        """Ferme la session HTTP."""
        if self._session and not self._session.closed:
            await self._session.close() 