# Installation Guide - Vaasa Lifti Custom Component

This guide will help you install and configure the Vaasa Lifti integration in Home Assistant.

## Prerequisites

Before you begin, make sure you have:
- Home Assistant 2023.1.0 or newer
- HACS (Home Assistant Community Store) installed
- Internet connection

## Step-by-Step Installation

### 1. Install HACS (if not already installed)

If you don't have HACS installed:
1. Visit [hacs.xyz](https://hacs.xyz) for installation instructions
2. Follow the official HACS installation guide
3. Restart Home Assistant after installation

### 2. Add Custom Repository to HACS

1. Open Home Assistant
2. Click on **HACS** in the sidebar
3. Click the three dots **⋮** in the top right corner
4. Select **Custom repositories**
5. In the "Repository" field, enter: `https://github.com/valtteri-aho/Hassio_Lifti`
6. In the "Category" dropdown, select: **Integration**
7. Click **Add**

### 3. Install Vaasa Lifti Integration

1. In HACS, click on **Integrations**
2. Click the **Explore & Download Repositories** button
3. Search for **"Vaasa Lifti"**
4. Click on **Vaasa Lifti**
5. Click **Download**
6. Select the latest version
7. Click **Download** again to confirm

### 4. Restart Home Assistant

**Important:** You must restart Home Assistant after installing the integration.

1. Go to **Settings** → **System**
2. Click **Restart** (top right corner)
3. Click **Restart** in the confirmation dialog
4. Wait for Home Assistant to restart (usually 1-2 minutes)

### 5. Get Your Digitransit API Key

1. Visit [https://portal-api.digitransit.fi](https://portal-api.digitransit.fi)
2. Click **Sign up** in the top right
3. Fill in your details and create an account
4. Log in to the portal
5. Click on **Products** in the top menu
6. Find **"Routing v2 Waltti GTFS"**
7. Click **Subscribe**
8. Go to your **Profile** page
9. Find **"Subscriptions"** section
10. Copy your **subscription key** (starts with a long string of letters and numbers)

**Keep this key safe - you'll need it in the next step!**

### 6. Find Your Bus Stop Codes

1. Visit [https://vaasa.digitransit.fi](https://vaasa.digitransit.fi)
2. Search for your address or bus stop name in the search bar
3. Click on the bus stop on the map
4. Look at the browser URL bar
5. The stop code is in the format: `Vaasa:XXXXXX`

**Common Vaasa Lifti Stops:**

| Location | Stop Code |
|----------|-----------|
| Melaniementie / Kaarnatie B | `Vaasa:159712` |
| Melaniementie / Kaarnatie A | `Vaasa:302812` |
| Vaasa Railway Station | `Vaasa:100600` |
| Vaasa Travel Center | `Vaasa:100100` |

**Write down the stop codes you want to monitor!**

### 7. Add the Integration in Home Assistant

1. Go to **Settings** → **Devices & Services**
2. Click the **+ Add Integration** button (bottom right corner)
3. Search for **"Vaasa Lifti"**
4. Click on **Vaasa Lifti** in the search results

### 8. Configure the Integration

#### Step 1: Enter API Key
1. Paste your Digitransit subscription key
2. Click **Submit**
3. Wait for validation (takes a few seconds)

**If you get an error:**
- Double-check you copied the entire key
- Make sure you subscribed to "Routing v2 Waltti GTFS"
- Check your internet connection

#### Step 2: Add First Bus Stop
1. Enter the stop ID (e.g., `Vaasa:159712`)
2. Choose number of departures to show (1-20, default: 5)
3. Click **Submit**
4. Wait for validation

**If you get an error:**
- Check the stop code format (must be `Vaasa:XXXXXX`)
- Verify the stop exists on vaasa.digitransit.fi
- Make sure there are no extra spaces

#### Step 3: Add More Stops (Optional)
1. Check **"Add another stop"** if you want to add more stops
2. Click **Submit**
3. Repeat Step 2 for each additional stop
4. When done, uncheck **"Add another stop"** and click **Submit**

### 9. Verify Installation

1. Go to **Settings** → **Devices & Services**
2. You should see **"Vaasa Lifti"** in the list
3. Click on **"Vaasa Lifti"** to see your configured stops
4. Click on a stop to see the sensor entity

### 10. Check Your Sensors

1. Go to **Developer Tools** → **States**
2. Search for **"vaasa_lifti"** or your stop name
3. You should see sensor entities like:
   - `sensor.melaniementie_kaarnatie_b`
   - `sensor.melaniementie_kaarnatie_a`
4. Click on a sensor to see its state and attributes

**Expected State:** 
- "5 min" (if bus in 5 minutes)
- "Now" (if bus departing now)
- "No departures" (if no buses scheduled)

**Expected Attributes:**
- `stop_code`, `stop_id`, `stop_name`
- `lahto_1`, `lahto_2`, etc. (formatted departures)
- `departures` (array of departure objects)

## Adding to Dashboard

### Quick Method - Auto Card

1. Go to your dashboard
2. Click **Edit Dashboard** (top right)
3. Click **+ Add Card**
4. Search for your sensor (e.g., "melaniementie")
5. Select the entity
6. Click **Add Card**

### Manual Method - Markdown Card

1. Click **Edit Dashboard**
2. Click **+ Add Card**
3. Select **Markdown**
4. Paste this code:

```yaml
type: markdown
title: 🚌 Bus Departures
content: |
  ## {{ state_attr('sensor.melaniementie_kaarnatie_b', 'stop_name') }}
  
  {% for i in range(1, 6) %}
  {% set lahto = state_attr('sensor.melaniementie_kaarnatie_b', 'lahto_' ~ i) %}
  {% if lahto %}
  {{ lahto }}
  {% endif %}
  {% endfor %}
```

5. Replace sensor name with your actual sensor
6. Click **Save**

### Advanced - Multiple Stops Card

```yaml
type: vertical-stack
cards:
  - type: markdown
    title: 🚌 Kaarnatie B → City Center
    content: |
      {% for i in range(1, 4) %}
      {% set lahto = state_attr('sensor.melaniementie_kaarnatie_b', 'lahto_' ~ i) %}
      {% if lahto %}{{ lahto }}{% endif %}
      {% endfor %}
  
  - type: markdown
    title: 🚌 Kaarnatie A → Gerby
    content: |
      {% for i in range(1, 4) %}
      {% set lahto = state_attr('sensor.melaniementie_kaarnatie_a', 'lahto_' ~ i) %}
      {% if lahto %}{{ lahto }}{% endif %}
      {% endfor %}
```

## Troubleshooting

### Integration Doesn't Appear

**Problem:** Can't find Vaasa Lifti in Add Integration list

**Solutions:**
1. Make sure you restarted Home Assistant after installing via HACS
2. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
3. Check HACS to confirm the integration is installed
4. Check Home Assistant logs for errors

### Invalid API Key Error

**Problem:** "Invalid API key" during setup

**Solutions:**
1. Go back to [portal-api.digitransit.fi](https://portal-api.digitransit.fi)
2. Verify you subscribed to "Routing v2 Waltti GTFS" product
3. Copy the entire subscription key (it's long!)
4. Make sure there are no extra spaces before/after the key
5. Try regenerating the key if it still doesn't work

### Invalid Stop ID Error

**Problem:** "Invalid stop ID" when adding stop

**Solutions:**
1. Verify format is exactly: `Vaasa:XXXXXX` (capital V)
2. Test the stop on [vaasa.digitransit.fi](https://vaasa.digitransit.fi)
3. Make sure there are no spaces in the stop code
4. Try copying the stop code directly from the URL

### Sensors Show "Unavailable"

**Problem:** Sensors exist but show "Unavailable"

**Solutions:**
1. Check your internet connection
2. Verify API key is still valid at portal-api.digitransit.fi
3. Go to **Settings** → **Devices & Services**
4. Find **Vaasa Lifti** and click **⋮** → **Reload**
5. Check Home Assistant logs for API errors
6. Wait a minute - it might just be updating

### No Departures Showing

**Problem:** Sensor works but shows "No departures"

**Solutions:**
1. Check current time - are buses running now?
2. Verify on vaasa.digitransit.fi that buses are scheduled
3. Some routes don't run on weekends/holidays
4. Wait for next departure time to appear

### Sensors Not Updating

**Problem:** Departure times don't refresh

**Solutions:**
1. Integration updates every 60 seconds
2. Check if times change after waiting a minute
3. Reload the integration
4. Check internet connection
5. Restart Home Assistant

## Getting Help

If you're still having issues:

1. **Check the logs:**
   - **Settings** → **System** → **Logs**
   - Search for "vaasa_lifti" or "digitransit"
   - Look for error messages

2. **Report an issue:**
   - Visit [https://github.com/valtteri-aho/Hassio_Lifti/issues](https://github.com/valtteri-aho/Hassio_Lifti/issues)
   - Click "New Issue"
   - Describe your problem
   - Include relevant log entries
   - Mention your Home Assistant version

3. **Community help:**
   - [Home Assistant Community Forum](https://community.home-assistant.io/)
   - Search for "Vaasa Lifti" or "Digitransit"

## Next Steps

- [View full documentation](https://github.com/valtteri-aho/Hassio_Lifti/blob/master/README_CUSTOM_COMPONENT.md)
- [Create automations](https://github.com/valtteri-aho/Hassio_Lifti/blob/master/README_CUSTOM_COMPONENT.md#-automation-examples)
- [Try advanced dashboard cards](https://github.com/valtteri-aho/Hassio_Lifti/blob/master/README_CUSTOM_COMPONENT.md#-dashboard-examples)

---

**Congratulations! You've successfully installed Vaasa Lifti!** 🎉

Enjoy real-time bus tracking in your Home Assistant dashboard!
