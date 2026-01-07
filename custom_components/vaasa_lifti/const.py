"""Constants for the Vaasa Lifti integration."""

DOMAIN = "vaasa_lifti"
CONF_API_KEY = "api_key"
CONF_STOPS = "stops"
CONF_STOP_ID = "stop_id"
CONF_STOP_NAME = "stop_name"
CONF_NUM_DEPARTURES = "num_departures"
CONF_ROUTES = "routes"

DEFAULT_NUM_DEPARTURES = 5
DEFAULT_SCAN_INTERVAL = 60

# Digitransit API
API_BASE_URL = "https://api.digitransit.fi/routing/v2/waltti/gtfs/v1"
API_TIMEOUT = 10

# Attributes
ATTR_STOP_CODE = "stop_code"
ATTR_DEPARTURES = "departures"
ATTR_NEXT_DEPARTURE = "next_departure"
ATTR_ROUTE = "route"
ATTR_DESTINATION = "destination"
ATTR_SCHEDULED_TIME = "scheduled_time"
ATTR_REALTIME = "realtime"
ATTR_DELAY = "delay"
