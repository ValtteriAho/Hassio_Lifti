# 🚌 Digitransit Bus Timetables for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/YOUR_USERNAME/ha-digitransit-bus.svg)](https://github.com/YOUR_USERNAME/ha-digitransit-bus/releases)
[![License](https://img.shields.io/github/license/YOUR_USERNAME/ha-digitransit-bus.svg)](LICENSE)

Display real-time Finnish bus schedules from Digitransit API directly in your Home Assistant dashboard.

This integration works with all Finnish cities using Digitransit: Helsinki (HSL), Tampere, Turku, Oulu, Vaasa, and more.

## 📋 Contents

This repository provides a complete configuration package for displaying Finnish bus timetables in Home Assistant.

**Files included:**
- **sensor_config.yaml** - REST sensors to fetch data from Digitransit API
- **sensor_config.example.yaml** - Template configuration file with placeholders
- **template_sensors.yaml** - Template sensors to format the data
- **lovelace_card.yaml** - 4 different dashboard card options
- **README.md** - Complete documentation
- **info.md** - HACS information
- **hacs.json** - HACS integration metadata

## 🎯 Features

- ✅ **Real-time departures** - Live GPS-tracked bus locations and times
- ✅ **Delay indicators** - Visual indicator (🔴) when real-time data is available
- ✅ **Up to 5 departures** per stop (configurable)
- ✅ **Multiple stops** - Monitor 2 or more bus stops simultaneously
- ✅ **Auto-refresh** - Updates every 60 seconds (configurable)
- ✅ **Minutes to departure** - Shows countdown until bus leaves
- ✅ **All Finnish cities** - Works with any Digitransit-powered region
- ✅ **Flexible display** - 4 pre-built Lovelace card options

## 🇫🇮 Supported Cities

This integration works with **all** Finnish cities and regions that use Digitransit:

| Region | Router | Example Stop Code |
|--------|--------|------------------|
| **Helsinki (HSL)** | `hsl` | `HSL:1010105` |
| **Tampere** | `waltti` | `tampere:0001` |
| **Turku (FOLI)** | `waltti` | `FOLI:1` |
| **Oulu** | `waltti` | `oulu:1001` |
| **Vaasa** | `waltti` | `Vaasa:159712` |
| **Jyväskylä** | `waltti` | `jyvaskyla:1001` |
| **Kuopio** | `waltti` | `kuopio:1001` |
| **Lahti** | `waltti` | `lahti:1001` |
| **Lappeenranta** | `waltti` | `lappeenranta:1` |
| **Other cities** | `waltti` or `finland` | Varies |

## 📦 Requirements

- **Home Assistant** 2023.1.0 or newer
- **Digitransit API key** (free registration at [digitransit.fi](https://digitransit.fi))
- Built-in integrations: REST, Template (no additional installs needed)

## � Quick Start Installation

### Step 1: Get Your Digitransit API Key

1. Visit [digitransit.fi](https://digitransit.fi)
2. Register for a free API key (required for API access)
3. Save your subscription key

### Step 2: Find Your Bus Stop Codes

**For Helsinki (HSL):**
- Visit [reittiopas.hsl.fi](https://reittiopas.hsl.fi)
- Search for your stop
- URL will show: `HSL:XXXXXXX` (e.g., `HSL:1010105`)

**For other cities (Waltti):**
- Visit your city's Digitransit site:
  - Tampere: [tampere.digitransit.fi](https://tampere.digitransit.fi)
  - Turku: [turku.digitransit.fi](https://turku.digitransit.fi)
  - Oulu: [oulu.digitransit.fi](https://oulu.digitransit.fi)
  - Vaasa: [vaasa.digitransit.fi](https://vaasa.digitransit.fi)
- Click on your stop
- URL will show: `CITY:XXXXXX` (e.g., `Vaasa:159712`)

### Step 3: Download Configuration Files

Download these files to your Home Assistant `config` directory:

```bash
# Create directory
mkdir -p config/bussiaikataulu

# Download files (or copy from repository)
# - sensor_config.yaml
# - template_sensors.yaml
# - lovelace_card.yaml
```

### Step 4: Configure REST Sensors

**Option A: Copy and edit `sensor_config.example.yaml`**

1. Copy `sensor_config.example.yaml` to `sensor_config.yaml`
2. Edit the file and replace:
   - `YOUR_API_KEY` with your Digitransit subscription key
   - `ROUTER` with your city's router (`hsl` or `waltti`)
   - `CITY:STOPCODE` with your actual stop codes

**Option B: Include existing configuration**

Add to `configuration.yaml`:

```yaml
rest: !include bussiaikataulu/sensor_config.yaml
```

**Important placeholders to replace:**
- Line 2: `https://api.digitransit.fi/routing/v2/ROUTER/gtfs/v1`
  - Replace `ROUTER` with:
    - `hsl` for Helsinki region
    - `waltti` for other cities (Tampere, Turku, Oulu, Vaasa, etc.)
    - `finland` for national data
  
- Line 3: `"query": "{ stop(id: \"CITY:STOPCODE\") {`
  - Replace `CITY:STOPCODE` with your actual stop code
  - Examples: `HSL:1010105`, `Vaasa:159712`, `tampere:0001`

- Line 6: `digitransit-subscription-key: "YOUR_API_KEY"`
  - Replace with your actual API key

### Step 5: Configure Template Sensors

Add to `configuration.yaml`:

```yaml
template: !include bussiaikataulu/template_sensors.yaml
```

No editing needed in `template_sensors.yaml` unless you want to customize the output format.

### Step 6: Restart Home Assistant

```yaml
# Settings → System → Restart
# OR
# Developer Tools → YAML → Check Configuration → Restart
```

### Step 7: Add Dashboard Card

1. Go to your dashboard
2. Click "Edit Dashboard"
3. Click "+ Add Card"
4. Select "Manual" (Manual YAML)
5. Copy one of the 4 options from `lovelace_card.yaml`
6. Paste and save

**Choose from 4 card styles:**
- **Option 1:** Vertical stack - Two separate compact cards
- **Option 2:** Combined markdown view - All stops in one card
- **Option 3:** Entities card - List format with attributes
- **Option 4:** Conditional card - Only shows on weekday mornings (6-10 AM)

## 📊 Available Sensors

After configuration, you'll have these sensors:

### Raw Data Sensors (internal use)
- `sensor.bussi_pysakki_1_raw` - Raw JSON from API for stop 1
- `sensor.bussi_pysakki_2_raw` - Raw JSON from API for stop 2

### Formatted Sensors (for display)
- `sensor.bussiaikataulu_pysakki_1` - Stop 1 timetable
  - **State:** Minutes until next departure (e.g., "5 min")
  - **Attributes:** `lahto_1` through `lahto_5`, `pysakki_nimi`, `pysakki_koodi`
  
- `sensor.bussiaikataulu_pysakki_2` - Stop 2 timetable
  - **State:** Minutes until next departure
  - **Attributes:** `lahto_1` through `lahto_5`, `pysakki_nimi`, `pysakki_koodi`
  
- `sensor.bussiaikataulu_yhdistetty` - Combined view of both stops
  - **State:** Next departure from either stop
  - **Attributes:** `kaikki_lahdot` - Formatted list of all departures

### Attribute Format

Each `lahto_X` attribute contains:
```
[Route] → [Destination] | [Time] ([Minutes] min) [🔴 if real-time]
```

Example:
```
3 → Palosaari | 08:45 (12 min) 🔴
```

## 🎨 Lovelace Dashboard Options

The `lovelace_card.yaml` file includes 4 ready-to-use card configurations:

### Option 1: Compact Vertical Stack (Recommended)
Shows both stops in a clean, space-efficient format with markdown rendering.

```yaml
type: vertical-stack
title: 🚌 Bus Timetables
```

### Option 2: Combined Markdown View
Single card showing all departures from both stops using the combined sensor.

```yaml
type: markdown
title: 🚌 Bus Timetables
```

### Option 3: Entities Card
Traditional list format showing each departure as a separate entity.

```yaml
type: entities
title: 🚌 Bus Timetables
```

### Option 4: Conditional Card (School Hours)
Only displays during weekday mornings (6 AM - 10 AM). Requires `workday` integration.

```yaml
type: conditional
conditions:
  - condition: state
    entity: binary_sensor.workday_sensor
    state: "on"
```

## 📱 Icon Legend

- **🔴** = Real-time GPS tracking active (live position data)
- No red dot = Schedule-based time (no GPS data)
- **min** = Minutes until departure

## 🔧 Troubleshooting

### Sensors Not Appearing

1. **Check configuration.yaml includes:**
   ```yaml
   rest: !include bussiaikataulu/sensor_config.yaml
   template: !include bussiaikataulu/template_sensors.yaml
   ```

2. **Restart Home Assistant** - Full restart required, not just reload

3. **Check logs:**
   - Settings → System → Logs
   - Look for errors mentioning `rest`, `template`, or `bussi`

### "No Departures" Showing Constantly

1. **Verify stop code:**
   - Check `sensor_config.yaml` has correct stop code format
   - Helsinki: `HSL:1010105`
   - Other cities: `CityName:XXXXXX`

2. **Test API directly:**
   - Use [GraphiQL interface](https://api.digitransit.fi/graphiql/hsl) (change `hsl` to `waltti` for other cities)
   - Test your GraphQL query manually

3. **Verify router:**
   - URL should have correct router: `/v2/hsl/gtfs/v1` or `/v2/waltti/gtfs/v1`

4. **Check API key:**
   - Ensure `digitransit-subscription-key` header is correct
   - Verify key is active at digitransit.fi

### Template Errors

1. **Test templates:**
   - Developer Tools → Template
   - Copy template code from `template_sensors.yaml`
   - Look for syntax errors

2. **Check raw sensor data:**
   - Developer Tools → States
   - Find `sensor.bussi_pysakki_1_raw`
   - Verify it has `stoptimesWithoutPatterns` attribute

### Updates Not Working

**Refresh rate:** REST sensor updates every 60 seconds by default.

**To change update interval:**
Edit `sensor_config.yaml` and modify:
```yaml
scan_interval: 30  # Update every 30 seconds (in seconds)
```

**Note:** Too frequent updates may hit API rate limits.

## 🔄 Customization & Advanced Usage

### Adding a Third Bus Stop

1. **In `sensor_config.yaml`:**
   - Copy the entire second stop configuration block
   - Change name to `"Bussi Pysäkki 3 Raw"`
   - Change `unique_id` to `bussi_pysakki_3_raw`
   - Update stop code in the GraphQL query

2. **In `template_sensors.yaml`:**
   - Copy the second stop's template sensor block
   - Change names: `bussiaikataulu_pysakki_3`
   - Change `unique_id` to `bussiaikataulu_pysakki_3`
   - Update references to `sensor.bussi_pysakki_3_raw`

3. **In `lovelace_card.yaml`:**
   - Add a third section using the same pattern

### Changing Number of Departures

**To show only 3 departures instead of 5:**

1. **In `sensor_config.yaml`:**
   ```yaml
   numberOfDepartures: 3  # Change from 5 to 3
   ```

2. **In `template_sensors.yaml`:**
   - Keep only `lahto_1`, `lahto_2`, `lahto_3` attributes
   - Remove `lahto_4` and `lahto_5` sections

3. **In `lovelace_card.yaml`:**
   - Update loops: `{% for i in range(1, 4) %}`  # Was range(1, 6)

### Creating Automations

**Example: Notify when bus is leaving soon**

```yaml
automation:
  - alias: "School Bus Reminder"
    trigger:
      - platform: numeric_state
        entity_id: sensor.bussiaikataulu_pysakki_1
        below: 5  # Less than 5 minutes
    condition:
      - condition: time
        after: "07:00:00"
        before: "08:30:00"
      - condition: state
        entity: binary_sensor.workday_sensor
        state: "on"
    action:
      - service: notify.mobile_app
        data:
          message: "Bus leaving in {{ states('sensor.bussiaikataulu_pysakki_1') }}!"
          title: "🚌 Bus Reminder"
```

**Example: Dashboard visibility based on time**

Use the conditional card (Option 4) in `lovelace_card.yaml` to show timetables only during school hours.

### Custom Formatting

Edit the `lahto_X` attributes in `template_sensors.yaml` to customize the display format:

```yaml
lahto_1: >
  {% set d = data[0] %}
  # Current format:
  {{ d.trip.route.shortName }} → {{ d.headsign }} | {{ (departure_time | timestamp_custom('%H:%M')) }} ({{ minutes }} min){{ ' 🔴' if d.realtime else '' }}
  
  # Alternative formats:
  # Simple: {{ d.headsign }} at {{ (departure_time | timestamp_custom('%H:%M')) }}
  # With route: Line {{ d.trip.route.shortName }}: {{ d.headsign }} ({{ minutes }}min)
  # Time only: {{ (departure_time | timestamp_custom('%H:%M')) }}
```

## 📚 Additional Resources

### Official Documentation
- **[Digitransit API](https://digitransit.fi/en/developers/apis/1-routing-api/)** - Complete API documentation
- **[GraphQL API Reference](https://digitransit.fi/en/developers/apis/1-routing-api/stops/)** - Stop queries and examples
- **[Home Assistant REST Sensor](https://www.home-assistant.io/integrations/rest/)** - REST integration docs
- **[Home Assistant Template](https://www.home-assistant.io/integrations/template/)** - Template sensor docs

### City-Specific Resources
- **Helsinki (HSL):** [reittiopas.hsl.fi](https://reittiopas.hsl.fi) | [dev.hsl.fi](https://dev.hsl.fi)
- **Tampere:** [tampere.digitransit.fi](https://tampere.digitransit.fi)
- **Turku:** [turku.digitransit.fi](https://turku.digitransit.fi)
- **Oulu:** [oulu.digitransit.fi](https://oulu.digitransit.fi)
- **Vaasa:** [vaasa.digitransit.fi](https://vaasa.digitransit.fi)

### GraphiQL Testing Interfaces
Test your queries before adding to Home Assistant:
- **HSL (Helsinki):** [api.digitransit.fi/graphiql/hsl](https://api.digitransit.fi/graphiql/hsl)
- **Waltti (other cities):** [api.digitransit.fi/graphiql/waltti](https://api.digitransit.fi/graphiql/waltti)
- **Finland (national):** [api.digitransit.fi/graphiql/finland](https://api.digitransit.fi/graphiql/finland)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

**Ideas for contributions:**
- Additional Lovelace card designs
- Multi-language support
- More example configurations
- Improved error handling
- Integration with other transit types (trains, trams, metro)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support & Community

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/ha-digitransit-bus/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/ha-digitransit-bus/discussions)
- **Home Assistant Community:** [community.home-assistant.io](https://community.home-assistant.io/)

## 📝 Changelog

### Version 0.1.0 (2026-01-07)
- Initial release
- Support for all Digitransit cities
- REST and Template sensor configurations
- 4 Lovelace card options
- Real-time departure tracking
- HACS-ready repository structure

## 🙏 Acknowledgments

- **Digitransit** - For providing the excellent open-source transit API
- **Home Assistant Community** - For inspiration and support
- **Finnish Transport Infrastructure Agency** - For open transit data

---

**Made with ❤️ for the Home Assistant community**

**Star ⭐ this repo if you find it useful!**
