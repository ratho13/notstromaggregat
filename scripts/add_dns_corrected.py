#!/usr/bin/env python3
"""
DNS-Einträge bei All-Inkl hinzufügen - Korrigierte Version
Verwendet exakt das gleiche Format wie im MCP Hub
"""

import os
import sys
import json
import requests
import time
import re

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
KAS_API_URL = "https://kasapi.kasserver.com/soap/KasApi.php"


def get_credentials():
    """Hole Credentials aus Environment Variables oder .env.local"""
    kas_user = os.getenv("ALL_INKL_KAS_USER", "")
    kas_password = os.getenv("ALL_INKL_KAS_PASSWORD", "")
    
    # Wenn nicht in Environment, versuche .env.local aus MCP HUB
    if not kas_user or not kas_password:
        env_file = "/Users/rthode/Projects/13 MCP HUB/.env.local"
        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("ALL_INKL_KAS_USER="):
                        kas_user = line.split("=", 1)[1].rstrip('\n\r')
                    elif line.startswith("ALL_INKL_KAS_PASSWORD="):
                        kas_password = line.split("=", 1)[1].rstrip('\n\r')
    
    # Entferne Anführungszeichen und String-Literale wie \n
    if kas_user:
        kas_user = kas_user.strip(' "\'')
        # Entferne String-Literale wie \n, \r, \t
        kas_user = kas_user.replace('\\n', '').replace('\\r', '').replace('\\t', '')
        # Entferne echte Newlines
        kas_user = kas_user.replace('\n', '').replace('\r', '').replace('\t', '')
        kas_user = kas_user.strip()
    
    if kas_password:
        kas_password = kas_password.strip(' "\'')
        # Entferne String-Literale wie \n, \r, \t
        kas_password = kas_password.replace('\\n', '').replace('\\r', '').replace('\\t', '')
        # Entferne echte Newlines
        kas_password = kas_password.replace('\n', '').replace('\r', '').replace('\t', '')
        kas_password = kas_password.strip()
    
    if not kas_user or not kas_password:
        return None, None
    
    return kas_user, kas_password


def create_soap_request(kas_user, kas_password, action, params):
    """Erstelle SOAP Request - exakt wie im MCP Hub"""
    request_params = {
        "kas_login": kas_user,
        "kas_auth_type": "plain",
        "kas_auth_data": kas_password,
        "kas_action": action,
        "KasRequestParams": params
    }
    
    params_json = json.dumps(request_params)
    
    # Exakt das gleiche Format wie im MCP Hub
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


def call_kas_api(kas_user, kas_password, action, params):
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


def extract_fault(xml_response):
    """Extrahiere Fehlermeldung aus SOAP Response"""
    if "<faultstring>" in xml_response:
        match = re.search(r'<faultstring>([^<]+)</faultstring>', xml_response)
        if match:
            return match.group(1)
    return None


def add_dns_record(kas_user, kas_password, record_name):
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
    
    xml_response = call_kas_api(kas_user, kas_password, "add_dns_settings", params)
    
    if xml_response is None:
        return False, "API-Aufruf fehlgeschlagen"
    
    # Prüfe auf Erfolg
    if "TRUE" in xml_response or "<return>TRUE</return>" in xml_response:
        return True, "Erfolgreich hinzugefügt"
    
    # Prüfe auf Fehler
    fault = extract_fault(xml_response)
    if fault:
        if "already exists" in fault.lower() or "bereits vorhanden" in fault.lower():
            return True, "Existiert bereits"
        return False, fault
    
    # Unerwartete Antwort
    return False, f"Unerwartete Antwort: {xml_response[:200]}"


def main():
    print("🚀 DNS-Einträge bei All-Inkl hinzufügen (Korrigierte Version)\n")
    
    # Credentials holen
    print("🔑 Hole Credentials...")
    kas_user, kas_password = get_credentials()
    
    if not kas_user or not kas_password:
        print("❌ Credentials nicht gefunden!")
        print("\nBitte setzen:")
        print("  export ALL_INKL_KAS_USER=w014c572")
        print("  export ALL_INKL_KAS_PASSWORD=<password>")
        sys.exit(1)
    
    print(f"✅ Credentials gefunden (User: '{kas_user}', Länge: {len(kas_user)})\n")
    
    # DNS-Einträge hinzufügen
    success_count = 0
    failed = []
    
    for i, record in enumerate(DNS_RECORDS):
        print(f"🌐 {record['language']}: {record['record_name']}.{ZONE_HOST}")
        success, message = add_dns_record(kas_user, kas_password, record['record_name'])
        
        if success:
            print(f"  ✅ {message}\n")
            success_count += 1
        else:
            print(f"  ❌ {message}\n")
            failed.append((record, message))
        
        # Warte 5 Sekunden zwischen Anfragen (Flood Protection)
        if i < len(DNS_RECORDS) - 1:
            print("  ⏳ Warte 5 Sekunden (Flood Protection)...\n")
            time.sleep(5)
    
    # Zusammenfassung
    print("="*60)
    print("📊 Zusammenfassung")
    print("="*60)
    print(f"✅ Erfolgreich: {success_count}/{len(DNS_RECORDS)}")
    if failed:
        print(f"❌ Fehlgeschlagen: {len(failed)}")
        for record, error in failed:
            print(f"   - {record['record_name']}.{ZONE_HOST} ({record['language']}): {error}")
    
    print("\n⏱️  DNS-Propagation: 5-60 Minuten")
    print("📧 Vercel sendet automatisch E-Mail-Bestätigungen")
    print("\n✅ Fertig!")


if __name__ == "__main__":
    main()
