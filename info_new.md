# Vaasa Lifti - Home Assistant Integration

Display real-time Vaasa Lifti bus schedules from Digitransit API directly in your Home Assistant dashboard.

## Features

- ✅ Real-time departures with GPS tracking
- ✅ UI-based configuration (no YAML editing)
- ✅ Multiple stop monitoring
- ✅ Delay indicators (🔴 for real-time data)
- ✅ Auto-refresh every 60 seconds
- ✅ Up to 20 departures per stop
- ✅ HACS compatible

## Quick Setup

1. Install through HACS
2. Restart Home Assistant
3. Get a free API key from [portal-api.digitransit.fi](https://portal-api.digitransit.fi)
4. Find your stop codes at [vaasa.digitransit.fi](https://vaasa.digitransit.fi)
5. Add the integration: **Settings** → **Devices & Services** → **Add Integration** → **Vaasa Lifti**
6. Enter your API key and stop codes

## Common Vaasa Stops

- Melaniementie / Kaarnatie B: `Vaasa:159712`
- Melaniementie / Kaarnatie A: `Vaasa:302812`
- Vaasa Railway Station: `Vaasa:100600`
- Vaasa Travel Center: `Vaasa:100100`

## What You Get

Each bus stop creates a sensor with:
- State showing minutes until next departure
- Formatted departure strings (lahto_1 through lahto_5)
- Full departure details in attributes
- Stop name and code information

## Dashboard Examples

Add a simple markdown card:

```yaml
type: markdown
content: |
  ## 🚌 Bus Departures
  {% for i in range(1, 6) %}
  {% set lahto = state_attr('sensor.melaniementie_kaarnatie_b', 'lahto_' ~ i) %}
  {% if lahto %}{{ lahto }}{% endif %}
  {% endfor %}
```

## Documentation

Full documentation available in [README_CUSTOM_COMPONENT.md](https://github.com/valtteri-aho/Hassio_Lifti/blob/master/README_CUSTOM_COMPONENT.md)

## Support

- 🐛 [Report Issues](https://github.com/valtteri-aho/Hassio_Lifti/issues)
- 📖 [Full Documentation](https://github.com/valtteri-aho/Hassio_Lifti)
