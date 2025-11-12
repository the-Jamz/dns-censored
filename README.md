# UK-Blocking Hosts VPN Routing List

A curated list of websites and services that block or restrict access to UK users, formatted for automatic VPN routing on MikroTik, ControlD, and UniFi devices.


---

## ⚠️ **Archived Project**

Please instead check out the very cool project [osatracker](https://osatracker.co.uk/) maintained by someone who has more time than me to develop this.

The project seems to be quickly gaining popularity too which of course helps with a community driven list, and I think splintering the efforts helps nobody.

I've spoken briefly to the creator and have been told that it will be open sourced at a later date. If that does not materialize then I will revive this project.

The RouterOS script in this repo works with the export domain from there dropped in which is also nice: `https://osatracker.co.uk/domains/export?format=newline&include_nsfw=1`.

---

## ⚠️ **EXPERIMENTAL PROJECT WARNING**

**This project is currently experimental and under active development:**

- ⚠️ **UniFi/VyOS/EdgeOS script is UNTESTED** - The `unifi-update.sh` script has not been tested on real hardware. Use at your own risk and test thoroughly before deploying to production.
- ⚠️ **Instructions may be incomplete** - Setup and configuration instructions are still being refined and may be missing steps or contain errors.

**Recommendation:** Create configuration backups before running any auto-update scripts. Report issues on GitHub.

---

## 📋 About

This project maintains a list of domains that have chosen to block, restrict, or significantly limit access from UK IP addresses, typically in response to the UK Online Safety Act and related regulations.

**Purpose:**
- Track which services are blocking UK users
- Provide transparency about internet fragmentation
- Enable automatic VPN routing for blocked services
- Help users maintain access to services via policy-based routing

## 🎯 Use Case

Unlike traditional DNS blocklists, this project is designed for **VPN routing**. When a domain on this list is accessed, your router will automatically route that traffic through a VPN connection, bypassing UK geo-restrictions.

## 📦 Auto-Update Scripts

The source domain list is maintained at `domains/uk-blocking-hosts.txt`. Auto-update scripts are available that run on your router and keep the list current:

- **Source** (`domains/uk-blocking-hosts.txt`) - Plain domain list (can be used directly)
- **Auto-Update Scripts** (`scripts/`) - Scripts that run on routers to auto-update
  - `mikrotik-update.rsc` - MikroTik RouterOS auto-update script
  - `unifi-update.sh` - UniFi/VyOS/EdgeOS auto-update script

## 🔗 Usage

### MikroTik RouterOS

**Quick Setup:**
1. Download [`mikrotik-update.rsc`](https://raw.githubusercontent.com/the-Jamz/dns-censored/main/scripts/mikrotik-update.rsc)
2. Upload to your router (Files > Upload in Winbox)
3. Import: `/import file=mikrotik-update.rsc`
4. Schedule daily updates at 3 AM:
   ```
   /system scheduler add name="uk-blocking-hosts-daily" \
       start-date=[/system clock get date] \
       start-time=03:00:00 \
       interval=1d \
       on-event="uk-blocking-hosts-update"
   ```
5. Run manually: `/system script run uk-blocking-hosts-update`

**Configure Routing:**
After the script runs, configure your firewall mangle and routing:
```
/ip firewall mangle add chain=prerouting dst-address-list=uk-blocked \
    action=mark-routing new-routing-mark=vpn-route passthrough=yes

/ip route add routing-mark=vpn-route gateway=<your-vpn-gateway>
```

**Customization:**
Edit line 20 in the script to change the address-list name from `uk-blocked` to your preferred name.

---

### UniFi/VyOS/EdgeOS

**Quick Setup:**
1. Download [`unifi-update.sh`](https://raw.githubusercontent.com/the-Jamz/dns-censored/main/scripts/unifi-update.sh)
2. Copy to router: `scp unifi-update.sh user@router:/config/scripts/`
3. Make executable: `ssh user@router chmod +x /config/scripts/unifi-update.sh`
4. Test: `ssh user@router sudo /config/scripts/unifi-update.sh`
5. Schedule via cron (daily at 3 AM):
   ```bash
   # SSH to router and edit crontab
   crontab -e

   # Add this line:
   0 3 * * * /config/scripts/unifi-update.sh >> /var/log/uk-blocking-update.log 2>&1
   ```

**Configure Routing:**
```bash
configure
set policy route VPN_ROUTE rule 10 destination group domain-group UK_BLOCKED
set policy route VPN_ROUTE rule 10 set table 1
set protocols static table 1 route 0.0.0.0/0 next-hop <vpn-gateway-ip>
commit
save
```

**Customization:**
Pass a custom domain-group name: `/config/scripts/unifi-update.sh MY_CUSTOM_GROUP`

---

### ControlD

**Direct URL Method:**
Simply add this URL to your ControlD Custom Rules:
```
https://raw.githubusercontent.com/the-Jamz/dns-censored/main/domains/uk-blocking-hosts.txt
```

ControlD will automatically fetch updates.

**Manual Import:**
1. Go to ControlD Dashboard > Filters > Custom Rules
2. Create a new folder (e.g., "UK Blocked")
3. Import using the URL above or paste domains manually
4. Set action to **REDIRECT** to route through your VPN endpoint

---

### Direct Domain List

Access the raw list directly:
```
https://raw.githubusercontent.com/the-Jamz/dns-censored/main/domains/uk-blocking-hosts.txt
```

## 📝 Contributing

We welcome contributions! If you've discovered a site blocking UK users:

1. **Verify the blocking:**
   - Confirm the site is inaccessible from UK IP addresses
   - Test with/without VPN to verify it's location-based
   - Document the error message or blocking notice

2. **Submit evidence:**
   - Open an issue with screenshots or details
   - Include the domain name and date of discovery
   - Note whether it's a complete block or partial restriction

3. **Pull requests:**
   - Add domains to `domains/uk-blocking-hosts.txt` only
   - Group domains by service with a comment header (e.g., `# Reddit`)
   - Include both the base domain and www subdomain if applicable
   - Update the entry count in the header
   - The domain list is validated automatically by CI

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## ⚖️ Scope

**Included:**
- Sites that completely block UK access
- Sites that significantly restrict functionality for UK users
- Services that have withdrawn from the UK market due to regulations

**Not included:**
- Sites that merely show cookie/GDPR notices
- Sites with UK-specific terms of service changes but no blocking
- Regional pricing differences
- Content licensing restrictions (e.g., streaming geo-blocks unrelated to OSA)

## 📜 License

See [LICENSE](LICENSE) file for details.

## 🔄 Updates

This list is updated as new blocking instances are discovered and verified. All formats include version timestamps for tracking.

## ⚠️ Disclaimer

This list is provided for informational and transparency purposes. Inclusion on this list indicates observed blocking behavior and does not constitute an endorsement or criticism of any service's decision to block UK traffic.

**Legal Note**: Users are responsible for ensuring their use of VPN routing complies with applicable laws and service terms of service.

## 🛠️ How Auto-Updates Work

**For Users:**

The auto-update scripts run on your router and automatically:
1. Download the latest domain list from GitHub
2. Update your address-list (MikroTik) or domain-group (UniFi/VyOS)
3. Log the results

You can schedule them to run daily (or any interval) so your router always has the latest blocked domains.

**For Contributors:**

Simply edit `domains/uk-blocking-hosts.txt` and submit a pull request. The domain list is validated automatically by GitHub Actions. Users' routers will automatically pull the updates on their next scheduled run.

## 🤝 Credits

This project's format and build system is **inspired by and modeled after** [HaGeZi's DNS Blocklists](https://github.com/hagezi/dns-blocklists).

**Attribution:**
- Format structure: Based on HaGeZi's multi-format blocklist approach
- Build methodology: Inspired by HaGeZi's repository organization
- Header format: Adapted from HaGeZi's metadata structure

We are grateful to HaGeZi for pioneering this comprehensive approach to DNS blocklist distribution and for providing an excellent example of how to structure and maintain such a project.

## 📊 Statistics

- **Current entries:** 4 domains
- **Last updated:** 2025-11-08
- **Auto-update scripts:** 2 (MikroTik, UniFi/VyOS)
- **Platforms supported:** ControlD, MikroTik RouterOS, UniFi USG/UDM, VyOS/EdgeOS
- **Update frequency:** Configurable (recommended: daily)

---

**Note:** This is a community-maintained list. If you believe a domain has been incorrectly included, please open an issue with evidence.
