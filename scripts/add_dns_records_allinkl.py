#!/usr/bin/env python3
"""
Script zum Hinzufügen von DNS-Einträgen bei All-Inkl KAS API
für alle Sprachversionen des Notstromaggregat-Projekts
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import requests

# All-Inkl KAS API Endpoint
KAS_API_URL = "https://kasapi.kasserver.com/soap/KasApi.php"

# DNS-Einträge die hinzugefügt werden sollen
DNS_RECORDS = [
    {
        "record_name": "notstromaggregat",
        "record_type": "A",
        "record_data": "76.76.21.21",
        "language": "DE"
    },
    {
        "record_name": "backup-generator",
        "record_type": "A",
        "record_data": "76.76.21.21",
        "language": "EN"
    },
    {
        "record_name": "groupe-electrogene",
        "record_type": "A",
        "record_data": "76.76.21.21",
        "language": "FR"
    },
    {
        "record_name": "noodaggregaat",
        "record_type": "A",
        "record_data": "76.76.21.21",
        "language": "NL"
    },
    {
        "record_name": "agregat-pradotworczy",
        "record_type": "A",
        "record_data": "76.76.21.21",
        "language": "PL"
    }
]

ZONE_HOST = "baltic-ihub.com"


def get_kas_credentials() -> tuple[str, str]:
    """Hole All-Inkl KAS Credentials aus Environment Variables oder 1Password"""
    kas_user = os.getenv("ALL_INKL_KAS_USER")
    kas_password = os.getenv("ALL_INKL_KAS_PASSWORD")
    
    if not kas_user or not kas_password:
        print("❌ Fehler: ALL_INKL_KAS_USER und ALL_INKL_KAS_PASSWORD müssen gesetzt sein")
        print("\nOptionen:")
        print("1. Environment Variables setzen:")
        print("   export ALL_INKL_KAS_USER=w014c572")
        print("   export ALL_INKL_KAS_PASSWORD=<password>")
        print("\n2. Oder aus 1Password:")
        print("   op read 'op://Automation/All-Inkl KAS (w014c572)/username'")
        print("   op read 'op://Automation/All-Inkl KAS (w014c572)/password'")
        sys.exit(1)
    
    return kas_user, kas_password


def create_soap_request(action: str, params: Dict) -> str:
    """Erstelle SOAP Request für All-Inkl KAS API"""
    request_params = {
        "kas_login": os.getenv("ALL_INKL_KAS_USER"),
        "kas_auth_type": "plain",
        "kas_auth_data": os.getenv("ALL_INKL_KAS_PASSWORD"),
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


def call_kas_api(action: str, params: Dict) -> str:
    """Rufe All-Inkl KAS API auf"""
    soap_envelope = create_soap_request(action, params)
    
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
        sys.exit(1)


def get_existing_dns_records() -> List[Dict]:
    """Hole bestehende DNS-Einträge"""
    zone_host = ZONE_HOST
    if not zone_host.endswith('.'):
        zone_host += '.'
    
    xml_response = call_kas_api("get_dns_settings", {
        "zone_host": zone_host,
        "nameserver": "ns5.kasserver.com"
    })
    
    # Parse XML Response (vereinfacht)
    records = []
    # Hier würde eine vollständige XML-Parsing-Logik stehen
    # Für jetzt nehmen wir an, dass die Einträge noch nicht existieren
    
    return records


def add_dns_record(record_name: str, record_type: str, record_data: str) -> bool:
    """Füge einen DNS-Eintrag hinzu"""
    zone_host = ZONE_HOST
    if not zone_host.endswith('.'):
        zone_host += '.'
    
    params = {
        "zone_host": zone_host,
        "record_name": record_name,
        "record_type": record_type,
        "record_data": record_data,
        "record_aux": "0"
    }
    
    print(f"📝 Füge DNS-Eintrag hinzu: {record_name}.{ZONE_HOST} → {record_data}")
    
    xml_response = call_kas_api("add_dns_settings", params)
    
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
            print(f"❌ Fehler beim Hinzufügen: {xml_response}")
            return False
    else:
        print(f"⚠️  Unerwartete Antwort: {xml_response[:200]}")
        return False


def main():
    """Hauptfunktion"""
    print("🚀 DNS-Einträge für Notstromaggregat-Projekt hinzufügen\n")
    
    # Credentials prüfen
    kas_user, kas_password = get_kas_credentials()
    print(f"✅ All-Inkl KAS Credentials gefunden (User: {kas_user})\n")
    
    # DNS-Einträge hinzufügen
    success_count = 0
    failed_records = []
    
    for record in DNS_RECORDS:
        print(f"\n🌐 {record['language']}: {record['record_name']}.{ZONE_HOST}")
        if add_dns_record(
            record['record_name'],
            record['record_type'],
            record['record_data']
        ):
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
