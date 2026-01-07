# 🚌 Vaasa Lifti - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/valtteri-aho/Hassio_Lifti.svg)](https://github.com/valtteri-aho/Hassio_Lifti/releases)
[![License](https://img.shields.io/github/license/valtteri-aho/Hassio_Lifti.svg)](LICENSE)

Display real-time Vaasa Lifti bus schedules from Digitransit API directly in your Home Assistant dashboard with easy UI-based configuration.

## 📋 What's Included

This repository provides a Home Assistant custom component for monitoring Vaasa Lifti bus schedules:

- **UI-based configuration** - No YAML editing required
- **Multiple stop monitoring** - Track unlimited bus stops
- **Real-time data** - Live GPS tracking and delays
- **HACS compatible** - Easy installation and updates

## 🎯 Features

- ✅ **Real-time departures** - Live GPS-tracked bus locations and times
- ✅ **Delay indicators** - Visual indicator (🔴) when real-time data is available
- ✅ **Up to 20 departures** per stop (configurable)
- ✅ **Multiple stops** - Monitor unlimited bus stops simultaneously
- ✅ **Auto-refresh** - Updates every 60 seconds
- ✅ **Minutes to departure** - Shows countdown until bus leaves
- ✅ **UI Configuration** - Easy setup through Home Assistant UI
- ✅ **HACS compatible** - Install and update through HACS

## 📦 Requirements

- **Home Assistant** 2023.1.0 or newer
- **Digitransit API key** (free registration required)
- **HACS** (recommended for easy installation)

## ⚡ Quick Start

### Step 1: Install via HACS

1. Open HACS in Home Assistant
2. Click the three dots ⋮ in the top right corner
3. Select "Custom repositories"
4. Add repository URL: `https://github.com/valtteri-aho/Hassio_Lifti`
5. Select category: "Integration"
6. Click "Add"
7. Find "Vaasa Lifti" in HACS and click "Download"
8. **Restart Home Assistant**

### Step 2: Get Your Digitransit API Key

1. Visit [https://portal-api.digitransit.fi](https://portal-api.digitransit.fi)
2. Sign up for a free account
3. Go to "Products" and subscribe to "Routing v2 Waltti GTFS"
4. Go to "Profile" and copy your subscription key

### Step 3: Find Your Bus Stop Codes

Visit [vaasa.digitransit.fi](https://vaasa.digitransit.fi) and:
1. Search for your bus stop
2. Click on the stop on the map
3. The URL will show the stop code format: `Vaasa:XXXXXX`

**Common Vaasa Lifti stops:**
- Melaniementie / Kaarnatie B: `Vaasa:159712`
- Melaniementie / Kaarnatie A: `Vaasa:302812`
- Vaasa Railway Station: `Vaasa:100600`
- Vaasa Travel Center: `Vaasa:100100`

### Step 4: Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for "Vaasa Lifti"
4. Enter your Digitransit API key when prompted
5. Add bus stops one at a time:
   - Enter stop ID (e.g., `Vaasa:159712`)
   - Choose number of departures to display (1-20)
6. Choose if you want to add more stops
7. Click **Submit**

Done! Your sensors will appear automatically.

## 📊 Sensor Data

Each bus stop creates a sensor entity:

**Entity ID format:** `sensor.<stop_name>`  
**Example:** `sensor.melaniementie_kaarnatie_b`

### Sensor State
Shows minutes until next departure:
- `"5 min"` - Bus in 5 minutes
- `"1 min"` - Bus in 1 minute
- `"Now"` - Bus departing now
- `"No departures"` - No buses scheduled

### Sensor Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `stop_code` | Stop code | `"159712"` |
| `stop_id` | Full stop ID | `"Vaasa:159712"` |
| `stop_name` | Stop name | `"Melaniementie / Kaarnatie"` |
| `lahto_1` to `lahto_5` | Formatted departure strings | `"3 → Palosaari \| 08:45 (12 min) 🔴"` |
| `departures` | Array of departure objects | See below |
| `next_departure` | Next departure object | See below |

### Departure Object Format

```json
{
  "route": "3",
  "destination": "Palosaari",
  "scheduled_time": "08:45",
  "minutes": 12,
  "realtime": true,
  "delay": 2,
  "departure_time": "2026-01-07T08:45:00+02:00"
}
```

## 🎨 Dashboard Examples

### Simple Markdown Card

```yaml
type: markdown
content: |
  ## 🚌 {{ state_attr('sensor.melaniementie_kaarnatie_b', 'stop_name') }}
  
  {% for i in range(1, 6) %}
  {% set lahto = state_attr('sensor.melaniementie_kaarnatie_b', 'lahto_' ~ i) %}
  {% if lahto %}
  {{ lahto }}
  {% endif %}
  {% endfor %}
```

### Entities Card

```yaml
type: entities
title: 🚌 Lifti Departures
entities:
  - entity: sensor.melaniementie_kaarnatie_b
    name: Kaarnatie B
  - entity: sensor.melaniementie_kaarnatie_a
    name: Kaarnatie A
show_header_toggle: false
```

### Multiple Stops Card

```yaml
type: vertical-stack
cards:
  - type: markdown
    title: 🚌 Kaarnatie B
    content: |
      {% for i in range(1, 6) %}
      {% set lahto = state_attr('sensor.melaniementie_kaarnatie_b', 'lahto_' ~ i) %}
      {% if lahto %}{{ lahto }}{% endif %}
      {% endfor %}
  
  - type: markdown
    title: 🚌 Kaarnatie A
    content: |
      {% for i in range(1, 6) %}
      {% set lahto = state_attr('sensor.melaniementie_kaarnatie_a', 'lahto_' ~ i) %}
      {% if lahto %}{{ lahto }}{% endif %}
      {% endfor %}
```

### Conditional Card (Only Show During Morning Commute)

```yaml
type: conditional
conditions:
  - condition: state
    entity: binary_sensor.workday_sensor
    state: "on"
  - condition: time
    after: "06:00:00"
    before: "09:00:00"
card:
  type: markdown
  title: 🚌 Morning Buses
  content: |
    {% for i in range(1, 4) %}
    {% set lahto = state_attr('sensor.melaniementie_kaarnatie_b', 'lahto_' ~ i) %}
    {% if lahto %}{{ lahto }}{% endif %}
    {% endfor %}
```

## 🔔 Automation Examples

### Notify When Bus is Arriving Soon

```yaml
automation:
  - alias: "Bus Departure Alert"
    trigger:
      - platform: state
        entity_id: sensor.melaniementie_kaarnatie_b
    condition:
      - condition: template
        value_template: "{{ trigger.to_state.state | int(0) <= 5 and trigger.to_state.state | int(0) > 0 }}"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🚌 Bus Leaving Soon!"
          message: "Bus in {{ states('sensor.melaniementie_kaarnatie_b') }}"
```

### Morning Commute Reminder

```yaml
automation:
  - alias: "Morning Bus Reminder"
    trigger:
      - platform: time
        at: "07:30:00"
    condition:
      - condition: state
        entity: binary_sensor.workday_sensor
        state: "on"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🚌 Next Bus"
          message: >
            {% set next = state_attr('sensor.melaniementie_kaarnatie_b', 'lahto_1') %}
            {{ next if next else 'No buses scheduled' }}
```

## 🔧 Configuration

### Adding More Stops

1. Go to **Settings** → **Devices & Services**
2. Find "Vaasa Lifti" integration
3. Click **Configure**
4. Add additional stops through the config flow

### Changing Update Interval

The integration updates every 60 seconds by default. To change this, you'll need to modify the component code in:
`custom_components/vaasa_lifti/__init__.py`

Look for:
```python
DEFAULT_SCAN_INTERVAL = 60  # Change to your preferred seconds
```

### Removing Stops

1. Go to **Settings** → **Devices & Services**
2. Find "Vaasa Lifti" integration
3. Click the three dots ⋮
4. Select "Delete"
5. Re-add the integration with your desired stops

## 📱 Mobile App Display

The formatted departure strings work great in mobile notifications:

**Format:** `[Route] → [Destination] | [Time] ([Minutes] min) [🔴 if real-time]`

**Examples:**
- `3 → Palosaari | 08:45 (12 min) 🔴`
- `1 → Gerby | 09:15 (25 min)`
- `7 → Sundom | 10:30 (now) 🔴`

## 🐛 Troubleshooting

### Integration Doesn't Appear After Installation

1. Make sure you restarted Home Assistant after installing through HACS
2. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
3. Check Home Assistant logs for errors

### "Invalid API Key" Error

1. Verify you copied the entire subscription key from Digitransit portal
2. Make sure you subscribed to "Routing v2 Waltti GTFS" product
3. Check if the key is still active in your profile

### "Invalid Stop ID" Error

1. Verify the stop ID format is correct: `Vaasa:XXXXXX`
2. Test the stop ID at [vaasa.digitransit.fi](https://vaasa.digitransit.fi)
3. Make sure there are no spaces or extra characters

### Sensors Show "Unavailable"

1. Check your internet connection
2. Verify API key is still valid
3. Check Home Assistant logs for API errors
4. Restart the integration: **Settings** → **Devices & Services** → **Vaasa Lifti** → **⋮** → **Reload**

### No Departures Showing

1. Verify the stop has scheduled buses at the current time
2. Check the stop on Digitransit website to confirm buses are running
3. Some routes may not operate on weekends or holidays

## 🌐 Finding More Stop Codes

### Method 1: Digitransit Website
1. Visit [vaasa.digitransit.fi](https://vaasa.digitransit.fi)
2. Click on any stop on the map
3. Copy the stop ID from the URL

### Method 2: GraphQL API
Use the GraphQL explorer to find stops near coordinates:
[https://api.digitransit.fi/graphiql/waltti](https://api.digitransit.fi/graphiql/waltti)

Query example:
```graphql
{
  stopsByRadius(lat: 63.095, lon: 21.615, radius: 500) {
    edges {
      node {
        stop {
          gtfsId
          name
          code
        }
      }
    }
  }
}
```

## 📚 Additional Resources

- **Digitransit API Documentation:** [digitransit.fi/en/developers/](https://digitransit.fi/en/developers/)
- **Vaasa Route Planner:** [vaasa.digitransit.fi](https://vaasa.digitransit.fi)
- **API Portal:** [portal-api.digitransit.fi](https://portal-api.digitransit.fi)
- **GraphQL Explorer:** [api.digitransit.fi/graphiql/waltti](https://api.digitransit.fi/graphiql/waltti)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

**Ideas for contributions:**
- Additional Lovelace card examples
- Support for other Finnish cities
- Route filtering features
- Location-based stop discovery
- Alert/disruption notifications

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Digitransit** - For providing the excellent open-source transit API
- **Vaasa Lifti** - For public transportation in Vaasa
- **Home Assistant Community** - For inspiration and support

---

**Made with ❤️ for Vaasa and the Home Assistant community**

**Star ⭐ this repo if you find it useful!**
