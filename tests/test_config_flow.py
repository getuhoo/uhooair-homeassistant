from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.uhoo_ha_component.const import DOMAIN
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.config_entries import SOURCE_USER
from homeassistant.const import CONF_API_KEY

from .const import MOCK_CONFIG


async def test_show_form(hass):
    """Test that the form is served with no input."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == SOURCE_USER


async def test_invalid_credentials(hass, error_on_login):
    """Test that errors are shown when credentials are invalid."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}, data=MOCK_CONFIG
    )

    assert result["errors"] == {"base": "auth"}


async def test_second_instance_error(
    hass, bypass_login, bypass_get_latest_data, bypass_get_devices, bypass_setup_devices
):
    """Test that errors are shown when a second instance is added."""

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="1",
        data=MOCK_CONFIG,
    )
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}, data=MOCK_CONFIG
    )

    assert result["type"] == "abort"
    assert result["reason"] == "single_instance_allowed"


async def test_create_entry(
    hass,
    bypass_async_setup_entry,
    bypass_login,
    bypass_get_latest_data,
    bypass_get_devices,
    bypass_setup_devices,
):
    """Test that the user step works."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}, data=MOCK_CONFIG
    )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["data"][CONF_API_KEY] == MOCK_CONFIG[CONF_API_KEY]
