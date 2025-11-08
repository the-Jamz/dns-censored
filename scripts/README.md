# Auto-Update Scripts

These scripts run ON your routers and automatically pull the latest UK-blocking hosts list from GitHub.

## Available Scripts

### `mikrotik-update.rsc`
Auto-update script for MikroTik RouterOS that downloads and updates the address-list.

**Features:**
- Runs on the router itself (no external dependencies)
- Configurable address-list name
- Can be scheduled to run automatically
- Logs all operations

**Setup:**
1. Download the script
2. Upload to your MikroTik router (Files > Upload in Winbox, or via FTP)
3. Import: `/import file=mikrotik-update.rsc`
4. Schedule (runs daily at 3 AM):
   ```
   /system scheduler add name="uk-blocking-hosts-daily" \
       start-date=[/system clock get date] \
       start-time=03:00:00 \
       interval=1d \
       on-event="uk-blocking-hosts-update"
   ```
5. Run manually: `/system script run uk-blocking-hosts-update`

**Configuration:**
Edit the `ADDRESS_LIST_NAME` variable in the script (line 20) to change the list name.

---

### `unifi-update.sh`
Auto-update script for UniFi/VyOS/EdgeOS routers that downloads and updates the domain-group.

**Features:**
- Runs on the router itself using standard tools (curl, bash)
- Configurable domain-group name
- Can be scheduled via cron
- Atomic updates with commit/save

**Setup:**
1. Download the script
2. Copy to router: `scp unifi-update.sh user@router:/config/scripts/`
3. Make executable: `ssh user@router chmod +x /config/scripts/unifi-update.sh`
4. Run once to test: `ssh user@router sudo /config/scripts/unifi-update.sh`
5. Schedule via cron (runs daily at 3 AM):
   ```bash
   # SSH to router and edit crontab
   crontab -e

   # Add this line:
   0 3 * * * /config/scripts/unifi-update.sh >> /var/log/uk-blocking-update.log 2>&1
   ```

**Configuration:**
Pass the domain group name as an argument: `/config/scripts/unifi-update.sh MY_CUSTOM_GROUP`

Or edit the `DOMAIN_GROUP_NAME` variable in the script.

---

### ControlD
For ControlD, simply use the raw GitHub URL directly in Custom Rules:

```
https://raw.githubusercontent.com/the-Jamz/dns-censored/main/domains/uk-blocking-hosts.txt
```

ControlD will automatically fetch updates from the URL.

## How It Works

Each script:
1. Downloads the latest `domains/uk-blocking-hosts.txt` from GitHub
2. Parses the file (skipping comments and empty lines)
3. Removes old entries from the address-list/domain-group
4. Adds all current domains
5. Logs the results

## Requirements

**MikroTik:**
- RouterOS v6.x or v7.x
- Internet connectivity
- HTTPS support (for fetching from GitHub)

**UniFi/VyOS/EdgeOS:**
- `curl` (usually pre-installed)
- `bash` (pre-installed)
- Internet connectivity
- Root/sudo access for configuration changes

## Updating the Scripts

To get the latest version of these scripts:
```bash
git pull
```

Then re-upload to your router and re-import (MikroTik) or re-copy (UniFi).

## Troubleshooting

**MikroTik:**
- Check logs: `/log print where topics~"uk-blocking"`
- Verify internet access: `/tool fetch url=https://www.google.com mode=https`
- Check script exists: `/system script print`

**UniFi/VyOS/EdgeOS:**
- Check logs: `cat /var/log/uk-blocking-update.log`
- Verify internet access: `curl -I https://www.google.com`
- Check domain-group: `show firewall group domain-group`

## Manual Updates

Both scripts can be run manually at any time:

**MikroTik:**
```
/system script run uk-blocking-hosts-update
```

**UniFi/VyOS/EdgeOS:**
```bash
sudo /config/scripts/unifi-update.sh
```
