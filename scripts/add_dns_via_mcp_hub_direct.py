#!/usr/bin/env python3
"""
DNS-Einträge über MCP Hub hinzufügen - Direkter Aufruf
"""

import os
import sys
import json
import requests
from typing import Dict

# MCP Hub URL
MCP_HUB_URL = "https://mcp-hub-lemon.vercel.app/mcp"

# DNS-Einträge
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


def add_dns_record(record_name: str, token: str) -> tuple[bool, str]:
    """Füge einen DNS-Eintrag über MCP Hub hinzu"""
    args = {
        "zone_host": ZONE_HOST,
        "record_name": record_name,
        "record_type": "A",
        "record_data": VERCEL_IP,
        "record_aux": "0"
    }
    
    result = call_mcp_hub_tool("allinkl.add_dns_record", args, token)
    
    if result is None:
        return False, "MCP Hub Aufruf fehlgeschlagen"
    
    if "error" in result:
        error_msg = result.get("error", {}).get("message", "Unbekannter Fehler")
        if "already exists" in error_msg.lower() or "bereits vorhanden" in error_msg.lower():
            return True, "Existiert bereits"
        return False, error_msg
    
    if "result" in result:
        result_data = result["result"]
        if isinstance(result_data, dict) and result_data.get("success"):
            return True, "Erfolgreich hinzugefügt"
        return False, f"Unerwartete Antwort: {result_data}"
    
    return False, "Unbekannte Antwort-Struktur"


def main():
    print("🚀 DNS-Einträge über MCP Hub hinzufügen\n")
    
    # MCP Hub Token prüfen
    token = os.getenv("MCP_HUB_TOKEN")
    if not token:
        print("❌ MCP_HUB_TOKEN nicht gesetzt")
        print("\nBitte Token setzen:")
        print("  export MCP_HUB_TOKEN=<token>")
        print("\nOder aus Vercel Environment Variables holen")
        sys.exit(1)
    
    print(f"✅ MCP Hub Token gefunden\n")
    
    # DNS-Einträge hinzufügen
    success_count = 0
    failed = []
    
    for record in DNS_RECORDS:
        print(f"🌐 {record['language']}: {record['record_name']}.{ZONE_HOST}")
        success, message = add_dns_record(record['record_name'], token)
        
        if success:
            print(f"  ✅ {message}\n")
            success_count += 1
        else:
            print(f"  ❌ {message}\n")
            failed.append(record)
    
    # Zusammenfassung
    print("="*60)
    print("📊 Zusammenfassung")
    print("="*60)
    print(f"✅ Erfolgreich: {success_count}/{len(DNS_RECORDS)}")
    if failed:
        print(f"❌ Fehlgeschlagen: {len(failed)}")
        for r in failed:
            print(f"   - {r['record_name']}.{ZONE_HOST} ({r['language']})")
    
    print("\n⏱️  DNS-Propagation: 5-60 Minuten")
    print("📧 Vercel sendet automatisch E-Mail-Bestätigungen")
    print("\n✅ Fertig!")


if __name__ == "__main__":
    main()
