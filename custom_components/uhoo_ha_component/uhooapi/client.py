import logging
import uuid
from aiohttp import ClientSession
from typing import Dict, Optional
from ..const import LOGGER, APP_VERSION
from .api import API
from .util import json_pp
from .device import Device
from .errors import UnauthorizedError, ForbiddenError

class Client(object):
    def __init__(self, api_key: str, websession: ClientSession, **kwargs) -> None:
        self._log: logging.Logger = LOGGER; 

        if kwargs.get("debug") is True:
            self._log.setLevel(logging.DEBUG)
            self._log.debug("Debug mode is explicitly enabled.")
        else:
            self._log.debug("Debug mode is not explicitly enabled (but may be enabled elsewhere).")

        self._app_version: int = APP_VERSION
        self._api_key: str = api_key
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._websession: ClientSession = websession
        self._mac_address: Optional[str] = None
        self._serial_number: Optional[str] = None
        self._mode: str = "minute"
        self._limit: int = 15
        self._devices: Dict[str, Device] = {}

        self._api: API = API(self._websession)

    async def login(self) -> None:
        user_token: dict = await self._api.generate_token()
        self._log.debug(f"[generate_token] returned\n{json_pp(user_token)}")
        self._access_token = user_token["access_token"]
        self._refresh_token = user_token["refresh_token"]
        self._api.set_bearer_token(self._access_token)

    async def setup_devices(self) -> None:
        try: 
            device_list: dict = await self._api.get_device_list()
        except UnauthorizedError:
            self._log.debug(
                "\033[93m"
                + "[get_latest_data] received 401 error, refreshing token and trying again"
                + "\033[0m"
            )
            await self.login()
            device_list: dict = await self._api.get_device_list()
        except ForbiddenError:
            self._log.debug(
                "\033[93m"
                + "[get_latest_data] received 403 error, refreshing token and trying again"
                + "\033[0m"
            )
            await self.login()
            device_list: dict = await self._api.get_device_list()

        device: dict
        for device in device_list:
            serial_number: str = device["serialNumber"]
            if serial_number not in self._devices:
                self._devices[serial_number] = Device(device)

    async def get_latest_data(self, serial_number: str) -> None:
        # @TODO: 
        try: 
            data_latest: dict = await self._api.get_device_data(serial_number, self._mode, self._limit)
        except UnauthorizedError:
            self._log.debug(
                "\033[93m"
                + "[get_latest_data] received 401 error, refreshing token and trying again"
                + "\033[0m"
            )
            await self.login()
            data_latest = await self._api.get_device_data(serial_number, self._mode, self._limit)
        except ForbiddenError:
            self._log.debug(
                "\033[93m"
                + "[get_latest_data] received 403 error, refreshing token and trying again"
                + "\033[0m"
            )
            await self.login()
            data_latest = await self._api.get_device_data(serial_number, self._mode, self._limit)

        if serial_number not in self._devices:
            LOGGER.error(f"[client get_latest_data], no serial number saved to setup devices")

        data: list = data_latest["data"]
        device_obj: Device = self._devices[serial_number]
        device_obj.update_data(data)
            
    def get_devices(self) -> Dict[str, Device]:
        return self._devices