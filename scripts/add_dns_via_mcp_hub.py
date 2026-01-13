#!/usr/bin/env python3
"""
Script zum Hinzufügen von DNS-Einträgen über den MCP Hub
"""

import os
import sys
import json
import requests
from typing import Dict, List

# MCP Hub URL
MCP_HUB_URL = "https://mcp-hub-lemon.vercel.app/mcp"

# DNS-Einträge die hinzugefügt werden sollen
DNS_RECORDS = [
    {"record_name": "notstromaggregat", "language": "DE"},
    {"record_name": "backup-generator", "language": "EN"},
    {"record_name": "groupe-electrogene", "language": "FR"},
    {"record_name": "noodaggregaat", "language": "NL"},
    {"record_name": "agregat-pradotworczy", "language": "PL"},
]

ZONE_HOST = "baltic-ihub.com"
VERCEL_IP = "76.76.21.21"


def call_mcp_hub_tool(tool_name: str, args: Dict, token: str) -> Dict:
    """Rufe MCP Hub Tool auf"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": args
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(
            MCP_HUB_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Fehler beim MCP Hub Aufruf: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text[:200]}")
        return None


def add_dns_record(record_name: str, token: str) -> bool:
    """Füge einen DNS-Eintrag über MCP Hub hinzu"""
    args = {
        "zone_host": ZONE_HOST,
        "record_name": record_name,
        "record_type": "A",
        "record_data": VERCEL_IP,
        "record_aux": "0"
    }
    
    print(f"📝 Füge DNS-Eintrag hinzu: {record_name}.{ZONE_HOST} → {VERCEL_IP}")
    
    result = call_mcp_hub_tool("allinkl.add_dns_record", args, token)
    
    if result is None:
        return False
    
    if "error" in result:
        error_msg = result.get("error", {}).get("message", "Unbekannter Fehler")
        # Prüfe ob Eintrag bereits existiert
        if "already exists" in error_msg.lower() or "bereits vorhanden" in error_msg.lower():
            print(f"⚠️  DNS-Eintrag existiert bereits: {record_name}.{ZONE_HOST}")
            return True
        else:
            print(f"❌ Fehler: {error_msg}")
            return False
    
    # Prüfe auf Erfolg
    if "result" in result:
        result_data = result["result"]
        if isinstance(result_data, dict) and result_data.get("success"):
            print(f"✅ DNS-Eintrag erfolgreich hinzugefügt: {record_name}.{ZONE_HOST}")
            return True
        else:
            print(f"⚠️  Unerwartete Antwort: {result_data}")
            return False
    
    return False


def main():
    """Hauptfunktion"""
    print("🚀 DNS-Einträge über MCP Hub hinzufügen\n")
    
    # MCP Hub Token prüfen
    token = os.getenv("MCP_HUB_TOKEN")
    if not token:
        print("❌ Fehler: MCP_HUB_TOKEN nicht gesetzt")
        print("\nOptionen:")
        print("1. Environment Variable setzen:")
        print("   export MCP_HUB_TOKEN=<token>")
        print("\n2. Oder aus 1Password:")
        print("   export MCP_HUB_TOKEN=$(op read 'op://Automation/MCP Hub Token/credential')")
        sys.exit(1)
    
    print(f"✅ MCP Hub Token gefunden\n")
    
    # DNS-Einträge hinzufügen
    success_count = 0
    failed_records = []
    
    for record in DNS_RECORDS:
        print(f"\n🌐 {record['language']}: {record['record_name']}.{ZONE_HOST}")
        if add_dns_record(record['record_name'], token):
            success_count += 1
        else:
            failed_records.append(record)
    
    # Zusammenfassung
    print("\n" + "="*60)
    print("📊 Zusammenfassung")
    print("="*60)
    print(f"✅ Erfolgreich: {success_count}/{len(DNS_RECORDS)}")
    if failed_records:
        print(f"❌ Fehlgeschlagen: {len(failed_records)}")
        for record in failed_records:
            print(f"   - {record['record_name']}.{ZONE_HOST} ({record['language']})")
    
    print("\n⏱️  DNS-Propagation: 5-60 Minuten")
    print("📧 Vercel sendet automatisch eine E-Mail-Bestätigung")
    print("\n✅ Fertig!")


if __name__ == "__main__":
    main()
