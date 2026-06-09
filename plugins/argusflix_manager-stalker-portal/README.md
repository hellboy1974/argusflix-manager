# ArgusFlix Stalker Portals Integrator Plugin

Integrate Stalker IPTV portals (Live TV, VOD Movies, and TV Series) into ArgusFlix using portal URLs and MAC addresses. Features automatic random stream verification to only import verified active content.

## Features

- **Stateless Playback Routing**: Registers a dynamic playback URL (`/stalker/play/<portal_key>/`) that resolves session keys and Stalker links on-the-fly and redirects streaming clients instantly.
- **Dynamic VOD Patching**: Extends ArgusFlix's built-in VOD and TV Series proxy engine at runtime to seamlessly play Stalker portal VOD movies and episodes.
- **Selective Synchronization**: Choose exactly what content types to sync (Live TV, VOD Movies, and/or TV Series) according to your preferences.
- **Pre-Import Filtering**: Clean, high-performance whitelisting and blacklisting before content is imported or tested.
  - **Category Whitelist**: Sync *only* items belonging to specified categories (e.g. `Sports, Action`).
  - **Category Blacklist**: Ignore entire categories (e.g. `Adult, XXX, Radios`).
  - **Title Keyword Blacklist**: Skip items that contain unwanted keywords in their name (e.g. `SD, Backup, 3D`).
- **Automatic Background Scheduling**: Set a 5-field standard cron schedule (e.g., `0 3 * * *` to run at 3:00 AM every night) to automatically synchronize the Stalker portals in the background. It dynamically integrates into ArgusFlix's native `django-celery-beat` scheduler.
- **Visual Highlighting of New Entries**: Automatically prefixes newly discovered and imported channels, movies, series, or episodes with a `🆕 ` emoji in their names, making them immediately recognizable in the ArgusFlix library dashboard.
- **Random Stream Verification**: Samples a configurable number of channels, movies, and episodes, validating that their streams are active and transmitting data before writing them to the database or M3U playlist.
- **Native UI Management**: Imports everything into ArgusFlix's native database models. Manage your channels, movies, and series directly using ArgusFlix's native dashboard UI (enable/disable, custom logos, metadata).

## Installation

1. Package this directory as a `.zip` file:
   ```bash
   zip -r argusflix_manager-stalker-portal.zip argusflix_manager-stalker-portal/
   ```
2. In the ArgusFlix UI, navigate to the **Plugins** page.
3. Click the **Import** button and select the generated `.zip` file.
4. Enable the **Stalker Portals Integrator** plugin.

## Configuration

The plugin supports two modes of configuration:

### Mode A: Single Portal (Simple)
Configure a single portal using the standard input fields:
- **Portal Name**: e.g., `My Stalker Portal`
- **Portal URL**: e.g., `http://stalker.example.com/c/`
- **MAC Address**: e.g., `00:1A:79:XX:XX:XX`
- **User-Agent Override**: Optional (default MAG250 User-Agent is used)

### Mode B: Multiple Portals (Advanced JSON)
Configure multiple portals by entering a JSON array in the **Portals JSON List** field. Example:
```json
[
  {
    "name": "Portal One",
    "url": "http://stalker1.example.com/c/",
    "mac": "00:1A:79:11:22:33"
  },
  {
    "name": "Portal Two",
    "url": "http://stalker2.example.com/c/",
    "mac": "00:1A:79:44:55:66",
    "user_agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) ..."
  }
]
```

### Detailed Content Filters
- **Synchronize Live TV**: (Checkbox) Select whether to load Live TV channels.
- **Synchronize Movies (VOD)**: (Checkbox) Select whether to load VOD movies.
- **Synchronize TV Series**: (Checkbox) Select whether to load TV Series and all their episodes.

### Pre-Import Sync Filters
- **Category Whitelist**: Comma-separated list of category names to include (e.g. `Sports, Action, Comedy`).
- **Category Blacklist**: Comma-separated list of category names to skip (e.g. `Adult, XXX, Radio`).
- **Title Keyword Blacklist**: Comma-separated list of keywords. Items containing these words in their name will be skipped (e.g. `SD, Backup, 3D`).

### Global Options
- **Mark New Entries with 🆕**: (Checkbox) Visually prefix newly discovered items with a `🆕 ` marker.
- **Test Sample Size**: Controls how many random channels, movies, and episodes of each portal are tested and imported (default: `5`).
- **Cron Sync Schedule**: Standard crontab schedule (e.g. `0 3 * * *` for 3:00 AM daily).
- **Local Stream Host**: The URL where your ArgusFlix backend is accessible by its proxy server (e.g., `http://127.0.0.1:5656` for local dev, or `http://web:9191` for Docker environment).
