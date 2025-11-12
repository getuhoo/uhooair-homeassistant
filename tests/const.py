"""Constants for uhoo tests."""
from typing import Any, Dict

from homeassistant.const import CONF_API_KEY

# Mock config data to be used across multiple tests
MOCK_CONFIG: dict = { CONF_API_KEY: "tes1232421232" }

MOCK_DEVICE: Dict[str, Any] = {
    "deviceName": "Office Room",
    "macAddress": "239239fj29j23f",
    "serialNumber": "23f9239m92m3ffkkdkdd",
    "floorNumber": 1,
    "roomName": "Living Room",
    "timezone": "(UTC+05:30) Chennai, Kolkata, Mumbai, New Delhi",
    "utcOffset": "+05:30",
    "ssid": "ssidsample"
}

MOCK_DEVICE_DATA = [
    {
        "virusIndex": 3,
        "moldIndex": 4,
        "temperature": 28.9,
        "humidity": 67.6,
        "pm25": 9,
        "tvoc": 1,
        "co2": 771,
        "co": 0,
        "airPressure": 1008.2,
        "ozone": 5,
        "no2": 0,
        "timestamp": 1762946521
    },
    {
        "virusIndex": 3,
        "moldIndex": 4,
        "temperature": 28.9,
        "humidity": 67.5,
        "pm25": 6,
        "tvoc": 1,
        "co2": 773,
        "co": 0,
        "airPressure": 1008.2,
        "ozone": 5,
        "no2": 1,
        "timestamp": 1762946581
    },
    {
        "virusIndex": 3,
        "moldIndex": 4,
        "temperature": 28.9,
        "humidity": 67.5,
        "pm25": 6,
        "tvoc": 1,
        "co2": 774,
        "co": 0,
        "airPressure": 1008.2,
        "ozone": 5,
        "no2": 1,
        "timestamp": 1762946641
    },
    {
        "virusIndex": 3,
        "moldIndex": 4,
        "temperature": 29,
        "humidity": 67.5,
        "pm25": 6,
        "tvoc": 1,
        "co2": 775,
        "co": 0,
        "airPressure": 1008.2,
        "ozone": 5,
        "no2": 0,
        "timestamp": 1762946701
    },
    {
        "virusIndex": 3,
        "moldIndex": 4,
        "temperature": 28.9,
        "humidity": 67.6,
        "pm25": 9,
        "tvoc": 1,
        "co2": 779,
        "co": 0,
        "airPressure": 1008.3,
        "ozone": 5,
        "no2": 0,
        "timestamp": 1762946761
    }
]
