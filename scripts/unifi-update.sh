#!/bin/bash
# ============================================================================
# UniFi/VyOS/EdgeOS Auto-Update Script for UK-Blocking Hosts
# ============================================================================
#
# This script runs ON your UniFi/VyOS/EdgeOS router and automatically
# downloads the latest UK-blocking hosts list from GitHub.
#
# SETUP:
# 1. Copy this script to your router: scp unifi-update.sh user@router:/config/scripts/
# 2. Make it executable: chmod +x /config/scripts/unifi-update.sh
# 3. Run once to test: sudo /config/scripts/unifi-update.sh
# 4. Add to cron for daily updates (see SCHEDULING section at bottom)
#
# CONFIGURATION:
# Edit DOMAIN_GROUP_NAME below to customize the domain group name
# ============================================================================

set -e

# CONFIGURATION
DOMAIN_GROUP_NAME="${1:-UK_BLOCKED}"

# DO NOT EDIT BELOW THIS LINE
UPDATE_URL="https://raw.githubusercontent.com/the-Jamz/dns-censored/main/domains/uk-blocking-hosts.txt"
TEMP_FILE="/tmp/uk-blocking-hosts-$$.txt"

echo "UK-Blocking Hosts: Starting update..."

# Download latest list
if ! curl -sSL "$UPDATE_URL" -o "$TEMP_FILE"; then
    echo "ERROR: Failed to download domain list from GitHub" >&2
    rm -f "$TEMP_FILE"
    exit 1
fi

echo "UK-Blocking Hosts: Downloaded latest list"

# Verify download succeeded
if [ ! -s "$TEMP_FILE" ]; then
    echo "ERROR: Downloaded file is empty" >&2
    rm -f "$TEMP_FILE"
    exit 1
fi

# Source VyOS functions
source /opt/vyatta/etc/functions/script-template

# Start configuration session
configure

# Create domain group if it doesn't exist
set firewall group domain-group "$DOMAIN_GROUP_NAME" description "UK-blocking hosts (auto-updated)"

# Add domains from file (only new ones)
added=0
while IFS= read -r line; do
    # Skip comments and empty lines
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$line" ]] && continue

    # Trim whitespace
    domain=$(echo "$line" | xargs)

    # Validate domain (must contain a dot)
    if [[ "$domain" == *.* ]]; then
        set firewall group domain-group "$DOMAIN_GROUP_NAME" address "$domain"
        ((added++))
    fi
done < "$TEMP_FILE"

# Commit changes
if commit; then
    save
    echo "UK-Blocking Hosts: Update complete - $added domains in '$DOMAIN_GROUP_NAME'"
else
    echo "ERROR: Failed to commit changes" >&2
    exit 1
fi

# Cleanup
rm -f "$TEMP_FILE"

exit

# ============================================================================
# SCHEDULING (CRON)
# ============================================================================
# To run this script daily at 3 AM, add to cron:
#
# 1. Edit crontab: crontab -e
# 2. Add this line:
#    0 3 * * * /config/scripts/unifi-update.sh >> /var/log/uk-blocking-update.log 2>&1
#
# Or run it manually:
# sudo /config/scripts/unifi-update.sh
# ============================================================================
