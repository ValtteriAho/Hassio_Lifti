"""The Vaasa Lifti integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import aiohttp

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_STOPS,
    DEFAULT_SCAN_INTERVAL,
    API_BASE_URL,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Vaasa Lifti from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    coordinator = VaasaLiftiCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


class VaasaLiftiCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Vaasa Lifti data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.api_key = entry.data[CONF_API_KEY]
        self.stops = entry.data[CONF_STOPS]
        self.session = async_get_clientsession(hass)
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from API."""
        try:
            data = {}
            
            for stop in self.stops:
                stop_id = stop["stop_id"]
                num_departures = stop.get("num_departures", 5)
                
                stop_data = await self._fetch_stop_data(stop_id, num_departures)
                data[stop_id] = stop_data
            
            return data
            
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def _fetch_stop_data(self, stop_id: str, num_departures: int) -> dict:
        """Fetch data for a single stop."""
        headers = {
            "Content-Type": "application/json",
            "digitransit-subscription-key": self.api_key,
        }
        
        query = f"""{{
            "query": "{{
                stop(id: \\"{stop_id}\\") {{
                    name
                    code
                    gtfsId
                    stoptimesWithoutPatterns(numberOfDepartures: {num_departures}) {{
                        scheduledDeparture
                        realtimeDeparture
                        realtime
                        serviceDay
                        headsign
                        trip {{
                            route {{
                                shortName
                                longName
                            }}
                        }}
                    }}
                }}
            }}"
        }}"""
        
        try:
            async with self.session.post(
                API_BASE_URL,
                data=query,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("data", {}).get("stop", {})
                else:
                    _LOGGER.error(
                        "API returned status %s for stop %s",
                        response.status,
                        stop_id,
                    )
                    return {}
        except (aiohttp.ClientError, TimeoutError) as err:
            _LOGGER.error("Error fetching data for stop %s: %s", stop_id, err)
            return {}
