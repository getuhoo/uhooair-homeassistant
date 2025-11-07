import asyncio
from typing import Dict, List
from homeassistant import core
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import CONF_API_KEY
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, STARTUP_MESSAGE, UPDATE_INTERVAL,PLATFORMS
from .uhooapi.errors import UnauthorizedError, UhooError
from .uhooapi.client import Client
from .uhooapi.device import Device


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the uhoo-ha-component component."""
    # @TODO: Add setup code.
    return True

async def async_setup_entry(hass: core.HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up uHoo integration from a config entry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        LOGGER.info(STARTUP_MESSAGE)

    # get api key and session from configuration
    api_key = config_entry.data.get(CONF_API_KEY)
    session = async_get_clientsession(hass)

    try:
        client = Client(api_key, session)
        await client.login()
        await client.setup_devices()
    except UnauthorizedError as err:
        LOGGER.error(f"Error: 401 Unauthorized error while logging in: {err}")
        return False
    except UhooError as err:
        raise ConfigEntryNotReady(err) from err

    coordinator = UhooDataUpdateCoordinator(hass, client=client)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][config_entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True

async def async_unload_entry(hass: core.HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Handle removal of an entry"""
    coordinator=hass.data[DOMAIN][config_entry.entry_id]
    unloaded = all(
        await asyncio.gather(*(
            hass.config_entries.async_forward_entry_unload(config_entry, platform)
            for platform in PLATFORMS
            if platform in coordinator.platforms
        ))
    )
    await hass.async_block_till_done()

    if unloaded:
        hass.data[DOMAIN].pop(config_entry.entry_id)
    return unloaded

class UhooDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the uHoo API."""
    def __init__(self, hass: core.HomeAssistant, client: Client) -> None:
        self.client = client
        self.platforms: List[str] = []
        self.user_settings_temp = None

        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)

    async def _async_update_data(self) -> Dict[str, Device]:
        # @TODO: Add Device Model and think of way to set multiple devices from list
        try:
            first_key = next(iter(self.client._devices), None)
            if first_key is not None:
                await self.client.get_latest_data(first_key)
            return self.client.get_devices()
        except Exception as exception:
            LOGGER.error(
                f"Error: an exception occurred while attempting to get latest data: {exception}"
            )
            raise UpdateFailed() from exception