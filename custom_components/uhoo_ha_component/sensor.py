from homeassistant import core
from homeassistant.components.sensor import SensorStateClass, SensorEntity
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import (
    DOMAIN,
    SENSOR_TYPES,
    ATTR_LABEL,
    ATTR_ICON,
    MANUFACTURER,
    ATTR_UNIT_OF_MEASUREMENT,
    ATTR_UNIQUE_ID,
    API_TEMP,
    MODEL,
    UnitOfTemperature,
)
from . import UhooDataUpdateCoordinator
from .uhooapi.device import Device


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: ConfigType,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensor platform"""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    sensors = []
    for serial_number in coordinator.data:
        for sensor in SENSOR_TYPES:
            sensors.append(UhooSensorEntity(sensor, serial_number, coordinator))

    async_add_entities(sensors, False)


class UhooSensorEntity(CoordinatorEntity, SensorEntity):
    def __init__(
        self, kind: str, serial_number: str, coordinator: UhooDataUpdateCoordinator
    ):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._kind = kind
        self._serial_number = serial_number

    @property
    def name(self):
        """Return the name of the particular component."""
        device: Device = self.coordinator.data[self._serial_number]
        return f"{device.device_name} {SENSOR_TYPES[self._kind][ATTR_LABEL]}"

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self._serial_number}_{SENSOR_TYPES[self._kind][ATTR_UNIQUE_ID]}"

    @property
    def device_info(self):
        device: Device = self.coordinator.data[self._serial_number]
        return {
            "identifiers": {(DOMAIN, self._serial_number)},
            "name": device.device_name,
            "model": MODEL,
            "manufacturer": MANUFACTURER,
        }

    @property
    def state(self):
        """State of the sensor."""
        device: Device = self._coordinator.data[self._serial_number]
        state = getattr(device, self._kind)
        if isinstance(state, list):
            state = state[0]
        return state

    @property
    def state_class(self) -> str:
        """Return the state class of this entity, from STATE_CLASSES, if any."""
        return str(SensorStateClass.MEASUREMENT)

    @property
    def icon(self) -> str:
        """Return the icon."""
        return str(SENSOR_TYPES[self._kind][ATTR_ICON])

    @property
    def unit_of_measurement(self) -> str:
        """Return unit of measurement."""
        if self._kind == API_TEMP:
            if self._coordinator.user_settings_temp == "f":
                return str(UnitOfTemperature.FAHRENHEIT)
            else:
                return str(UnitOfTemperature.CELSIUS)
        else:
            return str(SENSOR_TYPES[self._kind][ATTR_UNIT_OF_MEASUREMENT])
