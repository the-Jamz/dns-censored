#!/usr/bin/env python3
"""
Build script to generate VPN routing lists from the source domains list.

This script generates formats for routing UK-blocked domains through VPN:
- Plain domains list (for ControlD)
- MikroTik RouterOS script
- UniFi/VyOS script (for USG)

Inspired by the format structure from HaGeZi's DNS Blocklists:
https://github.com/hagezi/dns-blocklists
"""

import os
from datetime import datetime, timezone
from pathlib import Path


class BlocklistBuilder:
    """Generates VPN routing lists in multiple formats."""

    def __init__(self, source_file: str):
        self.source_file = Path(source_file)
        self.domains = []
        self.service_comments = {}
        self.header_info = {}

    def parse_source(self):
        """Parse the source domains file."""
        print(f"📖 Reading source file: {self.source_file}")

        with open(self.source_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_service = None
        domain_count = 0

        for line in lines:
            line = line.strip()

            # Parse header metadata
            if line.startswith('#'):
                # Extract metadata from header
                if ': ' in line:
                    key_value = line[1:].strip()
                    if key_value.startswith('Version:'):
                        self.header_info['version'] = key_value.split(':', 1)[1].strip()
                    elif key_value.startswith('Description:'):
                        self.header_info['description'] = key_value.split(':', 1)[1].strip()
                    elif key_value.startswith('Homepage:'):
                        self.header_info['homepage'] = key_value.split(':', 1)[1].strip()
                    elif key_value.startswith('Expires:'):
                        self.header_info['expires'] = key_value.split(':', 1)[1].strip()

                # Check for service name comments
                if not line.startswith('# ---') and len(line) > 2:
                    potential_service = line[1:].strip()
                    if potential_service and not ':' in potential_service and len(potential_service.split()) <= 3:
                        current_service = potential_service

                continue

            # Skip empty lines
            if not line:
                current_service = None
                continue

            # Valid domain line
            if self._is_valid_domain(line):
                self.domains.append(line)
                if current_service:
                    if current_service not in self.service_comments:
                        self.service_comments[current_service] = []
                    self.service_comments[current_service].append(line)
                domain_count += 1

        print(f"✅ Parsed {domain_count} domains")
        return domain_count

    def _is_valid_domain(self, domain: str) -> bool:
        """Basic domain validation."""
        # Simple validation: contains a dot and no spaces
        return '.' in domain and ' ' not in domain and not domain.startswith('#')

    def _get_comment_header(self, format_name: str, syntax: str, entry_count: int = None) -> str:
        """Generate a header for the output file."""
        if entry_count is None:
            entry_count = len(self.domains)

        timestamp = datetime.now(timezone.utc).strftime('%d %b %Y %H:%M UTC')
        version = datetime.now(timezone.utc).strftime('%Y.%m%d.%H%M.01')

        header = f"""# Title: UK-Blocking Hosts - VPN Routing List
# Description: Routes UK-blocked domains through VPN
# Homepage: https://github.com/the-Jamz/dns-censored
# License: https://github.com/the-Jamz/dns-censored/blob/main/LICENSE
# Issues: https://github.com/the-Jamz/dns-censored/issues
# Expires: {self.header_info.get('expires', '7 days')}
# Last modified: {timestamp}
# Version: {version}
# Syntax: {syntax}
# Number of entries: {entry_count}
#
# Format inspired by HaGeZi's DNS Blocklists
# https://github.com/hagezi/dns-blocklists
#

"""
        return header

    def build_mikrotik_script(self, output_file: str):
        """Generate MikroTik RouterOS script format."""
        print(f"🔨 Building MikroTik script: {output_file}")

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self._get_comment_header('MikroTik RouterOS', 'RouterOS Script'))

            f.write("# MikroTik RouterOS Script\n")
            f.write("# Usage: Copy and paste into RouterOS terminal, or import as .rsc file\n")
            f.write("#\n")
            f.write("# This script creates an address list named 'uk-blocked' with all domains\n")
            f.write("# Use this list in your firewall mangle rules to route through VPN\n")
            f.write("#\n")
            f.write("# Example mangle rule:\n")
            f.write("# /ip firewall mangle add chain=prerouting dst-address-list=uk-blocked \\\\\n")
            f.write("#   action=mark-routing new-routing-mark=vpn-route passthrough=yes\n")
            f.write("#\n\n")

            # Group by service if available
            if self.service_comments:
                for service, domains in self.service_comments.items():
                    f.write(f"# {service}\n")
                    for domain in domains:
                        f.write(f"/ip firewall address-list add list=uk-blocked address={domain}\n")
                    f.write("\n")
            else:
                # No service grouping, just add all domains
                for domain in self.domains:
                    f.write(f"/ip firewall address-list add list=uk-blocked address={domain}\n")

        print(f"✅ Generated {output_file}")

    def build_unifi_script(self, output_file: str):
        """Generate UniFi/VyOS script format for USG."""
        print(f"🔨 Building UniFi/VyOS script: {output_file}")

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self._get_comment_header('UniFi/VyOS', 'VyOS/EdgeOS Script'))

            f.write("# UniFi Security Gateway (USG) / VyOS Script\n")
            f.write("# Usage: Connect via SSH and paste these commands\n")
            f.write("#\n")
            f.write("# This creates a domain-group named 'UK_BLOCKED' with all domains\n")
            f.write("# Use this group in your firewall and policy routing rules\n")
            f.write("#\n")
            f.write("# Example policy route:\n")
            f.write("# configure\n")
            f.write("# set policy route VPN_ROUTE rule 10 destination group domain-group UK_BLOCKED\n")
            f.write("# set policy route VPN_ROUTE rule 10 set table 1\n")
            f.write("# commit\n")
            f.write("# save\n")
            f.write("#\n\n")

            f.write("configure\n\n")

            # Group by service if available
            if self.service_comments:
                for service, domains in self.service_comments.items():
                    f.write(f"# {service}\n")
                    for domain in domains:
                        f.write(f"set firewall group domain-group UK_BLOCKED address '{domain}'\n")
                    f.write("\n")
            else:
                # No service grouping, just add all domains
                for domain in self.domains:
                    f.write(f"set firewall group domain-group UK_BLOCKED address '{domain}'\n")

            f.write("\ncommit\n")
            f.write("save\n")
            f.write("exit\n")

        print(f"✅ Generated {output_file}")

    def build_controld_list(self, output_file: str):
        """Generate ControlD-compatible domain list."""
        print(f"🔨 Building ControlD list: {output_file}")

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self._get_comment_header('ControlD', 'Domain List'))

            f.write("# ControlD Custom Rules Format\n")
            f.write("# Usage: Import this list into ControlD Custom Rules\n")
            f.write("#\n")
            f.write("# 1. Go to ControlD Dashboard > Filters > Custom Rules\n")
            f.write("# 2. Create a new folder or select existing\n")
            f.write("# 3. Import this file or copy domains below\n")
            f.write("# 4. Set action to 'REDIRECT' to route through specific resolver/VPN\n")
            f.write("#\n\n")

            # Group by service if available
            if self.service_comments:
                for service, domains in self.service_comments.items():
                    f.write(f"# {service}\n")
                    for domain in domains:
                        f.write(f"{domain}\n")
                    f.write("\n")
            else:
                # No service grouping, just add all domains
                for domain in self.domains:
                    f.write(f"{domain}\n")

        print(f"✅ Generated {output_file}")

    def build_all_formats(self):
        """Build all supported formats."""
        print("\n🚀 Building all formats...\n")

        self.parse_source()

        # Create all format files
        self.build_controld_list('controld/uk-blocking-hosts.txt')
        self.build_mikrotik_script('mikrotik/uk-blocking-hosts.rsc')
        self.build_unifi_script('unifi/uk-blocking-hosts.sh')

        print("\n✨ All formats generated successfully!\n")


def main():
    """Main entry point."""
    source_file = 'domains/uk-blocking-hosts.txt'

    if not os.path.exists(source_file):
        print(f"❌ Source file not found: {source_file}")
        return 1

    builder = BlocklistBuilder(source_file)
    builder.build_all_formats()

    return 0


if __name__ == '__main__':
    exit(main())
