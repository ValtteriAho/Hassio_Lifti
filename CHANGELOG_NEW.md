# Changelog

All notable changes to the Vaasa Lifti integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-07

### Added - Custom Component
- **Full Home Assistant custom component** with UI-based configuration
- **Config flow** for easy setup through Settings → Devices & Services
- **No YAML editing required** - everything configured through UI
- **Unlimited bus stops** - add as many stops as you need
- **Real-time departure tracking** with GPS data from Digitransit API
- **Delay indicators** showing when buses are delayed or early
- **Auto-refresh** every 60 seconds using DataUpdateCoordinator
- **HACS compatibility** for easy installation and updates

### Features
- Entity created per bus stop with friendly names
- State shows minutes until next departure ("5 min", "Now", etc.)
- Rich attributes including:
  - `lahto_1` through `lahto_5` - formatted departure strings
  - `departures` - full array of departure objects
  - `next_departure` - detailed next departure info
  - `stop_code`, `stop_id`, `stop_name` - stop information
- Configurable number of departures (1-20 per stop)
- API key validation during setup
- Stop ID validation with automatic name lookup
- Multi-step configuration flow with "add another stop" option
- Options flow for future configuration changes

### Technical Implementation
- Uses `DataUpdateCoordinator` for efficient updates
- `CoordinatorEntity` pattern for sensors
- Async/await throughout for performance
- Proper error handling and logging
- Digitransit API v2 (Waltti GTFS) GraphQL integration
- Type hints and modern Python patterns
- Full Home Assistant integration standards compliance

### Documentation
- Comprehensive README_CUSTOM_COMPONENT.md
- Installation guide for HACS
- Dashboard examples (Markdown, Entities, Conditional cards)
- Automation examples
- Troubleshooting guide
- API key and stop code instructions

## [0.1.0] - 2026-01-07

### Added - Initial YAML Configuration
- Initial release of YAML-based configuration
- REST sensor configuration for Digitransit API v2
- Template sensors for formatting bus departure data
- 4 different Lovelace card options
- Support for Vaasa Lifti routes
- Real-time GPS tracking with visual indicators
- Example configuration files

### Features
- Monitor 2 bus stops (expandable)
- Display route number, destination, scheduled time, countdown
- Real-time delay indicators (🔴 emoji)
- Auto-refresh every 60 seconds (configurable)
- GraphQL query support

### Documentation
- Basic README with installation guide
- Configuration examples
- Troubleshooting section

[1.0.0]: https://github.com/valtteri-aho/Hassio_Lifti/releases/tag/v1.0.0
[0.1.0]: https://github.com/valtteri-aho/Hassio_Lifti/releases/tag/v0.1.0
