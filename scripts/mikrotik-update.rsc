# ============================================================================
# MikroTik Auto-Update Script for UK-Blocking Hosts
# ============================================================================
#
# This script runs ON your MikroTik router and automatically downloads
# the latest UK-blocking hosts list from GitHub.
#
# SETUP:
# 1. Upload this file to your MikroTik router (Files menu in Winbox or via FTP)
# 2. In terminal: /import file=mikrotik-update.rsc
# 3. Schedule it (see SCHEDULING section below)
# 4. Run manually: /system script run uk-blocking-hosts-update
#
# CONFIGURATION:
# Edit the ADDRESS_LIST_NAME variable below to customize the list name
# ============================================================================

/system script add name="uk-blocking-hosts-update" source={
# CONFIGURATION
:local addressListName "uk-blocked"

# DO NOT EDIT BELOW THIS LINE
:local updateURL "https://raw.githubusercontent.com/the-Jamz/dns-censored/main/domains/uk-blocking-hosts.txt"
:local tempFile "uk-hosts.txt"

:log info "UK-Blocking: Starting update"

# Download latest list
:do {
    /tool fetch url=$updateURL dst-path=$tempFile mode=https
    :delay 3s
} on-error={
    :log error "UK-Blocking: Download failed"
    :error "Download failed"
}

# Verify download succeeded
:local content [/file get $tempFile contents]
:if ([:len $content] = 0) do={
    :log error "UK-Blocking: Downloaded file is empty"
    /file remove $tempFile
    :error "Downloaded file is empty"
}

# Parse file and add domains
:local added 0
:local lineEnd 0
:local line ""

:while ([:len $content] > 0) do={
    :set lineEnd [:find $content "\n"]

    :if ([:typeof $lineEnd] = "nil") do={
        :set line $content
        :set content ""
    } else={
        :set line [:pick $content 0 $lineEnd]
        :set content [:pick $content ($lineEnd + 1) [:len $content]]
    }

    # Clean up line
    :if ([:len $line] > 0) do={
        # Remove \r if present
        :if ([:pick $line ([:len $line] - 1)] = "\r") do={
            :set line [:pick $line 0 ([:len $line] - 1)]
        }
    }

    # Trim spaces
    :while ([:len $line] > 0 && [:pick $line 0] = " ") do={
        :set line [:pick $line 1 [:len $line]]
    }
    :while ([:len $line] > 0 && [:pick $line ([:len $line] - 1)] = " ") do={
        :set line [:pick $line 0 ([:len $line] - 1)]
    }

    # Add valid domains
    :if ([:len $line] > 0 && [:pick $line 0] != "#") do={
        :if ([:typeof [:find $line "."]] != "nil") do={
            :do {
                /ip firewall address-list add list=$addressListName address=$line comment="auto-added"
                :set added ($added + 1)
            } on-error={}
        }
    }
}

# Cleanup
/file remove $tempFile

:log info "UK-Blocking: Complete - $added domains added"
:put "Update complete: $added domains added to $addressListName"
}

# ============================================================================
# SCHEDULING
# ============================================================================
# To run this script daily at 3 AM, paste this in terminal:
#
# /system scheduler add name="uk-blocking-hosts-daily" \
#     start-date=[/system clock get date] \
#     start-time=03:00:00 \
#     interval=1d \
#     on-event="uk-blocking-hosts-update"
#
# Or run it manually anytime:
# /system script run uk-blocking-hosts-update
# ============================================================================
