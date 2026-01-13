#!/usr/bin/env python3
"""
Script zum Hinzufügen von DNS-Einträgen bei All-Inkl KAS API
für alle Sprachversionen des Notstromaggregat-Projekts

Verwendet Credentials aus MCP Hub Environment Variables oder direkt
"""

import os
import sys
import json
import requests
from typing import Dict

# All-Inkl KAS API Endpoint
KAS_API_URL = "https://kasapi.kasserver.com/soap/KasApi.php"

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


def get_credentials_from_mcp_hub() -> tuple[str, str]:
    """Versuche Credentials über MCP Hub API zu bekommen"""
    mcp_hub_url = "https://mcp-hub-lemon.vercel.app/mcp"
    token = os.getenv("MCP_HUB_TOKEN")
    
    if not token:
        return None, None
    
    # Versuche über MCP Hub die Credentials zu bekommen
    # (Dies ist ein Workaround - normalerweise würden wir die Tools direkt aufrufen)
    return None, None


def create_soap_request(kas_user: str, kas_password: str, action: str, params: Dict) -> str:
    """Erstelle SOAP Request für All-Inkl KAS API"""
    request_params = {
        "kas_login": kas_user,
        "kas_auth_type": "plain",
        "kas_auth_data": kas_password,
        "kas_action": action,
        "KasRequestParams": params
    }
    
    params_json = json.dumps(request_params)
    
    soap_envelope = f'''<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope 
    xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ns1="https://kasserver.com/"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <SOAP-ENV:Body>
    <ns1:KasApi>
      <Params xsi:type="xsd:string">{params_json}</Params>
    </ns1:KasApi>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''
    
    return soap_envelope


def call_kas_api(kas_user: str, kas_password: str, action: str, params: Dict) -> str:
    """Rufe All-Inkl KAS API auf"""
    soap_envelope = create_soap_request(kas_user, kas_password, action, params)
    
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "https://kasserver.com/#KasApi"
    }
    
    try:
        response = requests.post(
            KAS_API_URL,
            data=soap_envelope,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ Fehler beim API-Aufruf: {e}")
        return None


def add_dns_record(kas_user: str, kas_password: str, record_name: str) -> bool:
    """Füge einen DNS-Eintrag hinzu"""
    zone_host = ZONE_HOST
    if not zone_host.endswith('.'):
        zone_host += '.'
    
    params = {
        "zone_host": zone_host,
        "record_name": record_name,
        "record_type": "A",
        "record_data": VERCEL_IP,
        "record_aux": "0"
    }
    
    print(f"📝 Füge DNS-Eintrag hinzu: {record_name}.{ZONE_HOST} → {VERCEL_IP}")
    
    xml_response = call_kas_api(kas_user, kas_password, "add_dns_settings", params)
    
    if xml_response is None:
        return False
    
    # Prüfe auf Erfolg
    if "TRUE" in xml_response or "<return>TRUE</return>" in xml_response:
        print(f"✅ DNS-Eintrag erfolgreich hinzugefügt: {record_name}.{ZONE_HOST}")
        return True
    elif "faultstring" in xml_response:
        # Prüfe ob Eintrag bereits existiert
        if "already exists" in xml_response.lower() or "bereits vorhanden" in xml_response.lower():
            print(f"⚠️  DNS-Eintrag existiert bereits: {record_name}.{ZONE_HOST}")
            return True
        else:
            fault_match = xml_response.split("<faultstring>")[1].split("</faultstring>")[0] if "<faultstring>" in xml_response else "Unbekannter Fehler"
            print(f"❌ Fehler beim Hinzufügen: {fault_match}")
            return False
    else:
        print(f"⚠️  Unerwartete Antwort: {xml_response[:200]}")
        return False


def main():
    """Hauptfunktion"""
    print("🚀 DNS-Einträge für Notstromaggregat-Projekt hinzufügen\n")
    
    # Credentials aus verschiedenen Quellen versuchen
    kas_user = os.getenv("ALL_INKL_KAS_USER", "w014c572")
    kas_password = os.getenv("ALL_INKL_KAS_PASSWORD")
    
    # Wenn nicht in Environment, versuche über MCP Hub
    if not kas_password:
        print("⚠️  ALL_INKL_KAS_PASSWORD nicht in Environment Variables gefunden")
        print("📝 Versuche über MCP Hub...")
        
        # Versuche über MCP Hub Tool aufzurufen
        mcp_hub_url = "https://mcp-hub-lemon.vercel.app/mcp"
        token = os.getenv("MCP_HUB_TOKEN")
        
        if token:
            print("✅ MCP_HUB_TOKEN gefunden, verwende MCP Hub Tools...")
            # Hier würden wir die allinkl.add_dns_record Tools über MCP Hub aufrufen
            # Für jetzt zeigen wir die Anleitung
            print("\n📋 Bitte verwende eines der folgenden Verfahren:\n")
            print("Option 1: Environment Variables setzen")
            print("  export ALL_INKL_KAS_USER=w014c572")
            print("  export ALL_INKL_KAS_PASSWORD=<password>")
            print("  python3 scripts/add_dns_records_final.py\n")
            print("Option 2: Über MCP Hub (wenn Token verfügbar)")
            print("  python3 scripts/add_dns_via_mcp_hub.py\n")
            print("Option 3: Manuell über All-Inkl KAS Web-Interface")
            print("  https://kas.kasserver.com/ → Domains → baltic-ihub.com → DNS-Verwaltung\n")
            sys.exit(1)
        else:
            print("❌ MCP_HUB_TOKEN auch nicht gefunden")
            print("\n📝 Bitte Credentials manuell setzen oder über All-Inkl KAS Web-Interface hinzufügen")
            sys.exit(1)
    
    print(f"✅ All-Inkl KAS Credentials gefunden (User: {kas_user})\n")
    
    # DNS-Einträge hinzufügen
    success_count = 0
    failed_records = []
    
    for record in DNS_RECORDS:
        print(f"\n🌐 {record['language']}: {record['record_name']}.{ZONE_HOST}")
        if add_dns_record(kas_user, kas_password, record['record_name']):
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
