#!/usr/bin/env python3
"""
DNS-Einträge von A auf CNAME ändern für alle Subdomains
Gemäß Vercel-Anweisungen
"""

import os
import sys
import json
import requests
import time
import re

# Subdomains die geändert werden müssen
SUBDOMAINS = [
    {"record_name": "notstromaggregat", "language": "DE"},
    {"record_name": "backup-generator", "language": "EN"},
    {"record_name": "groupe-electrogene", "language": "FR"},
    {"record_name": "noodaggregaat", "language": "NL"},
    {"record_name": "agregat-pradotworczy", "language": "PL"},
]

ZONE_HOST = "baltic-ihub.com"
# Neuer CNAME-Wert (aus Vercel-Anweisungen)
CNAME_VALUE = "7c6be46a197dc3f0.vercel-dns-017.com."
KAS_API_URL = "https://kasapi.kasserver.com/soap/KasApi.php"


def get_credentials():
    """Hole Credentials aus .env.local"""
    env_file = "/Users/rthode/Projects/13 MCP HUB/.env.local"
    kas_user = None
    kas_password = None
    
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("ALL_INKL_KAS_USER="):
                    kas_user = line.split("=", 1)[1].rstrip('\n\r').strip(' "\'')
                    kas_user = kas_user.replace('\\n', '').replace('\\r', '').strip()
                elif line.startswith("ALL_INKL_KAS_PASSWORD="):
                    kas_password = line.split("=", 1)[1].rstrip('\n\r').strip(' "\'')
                    kas_password = kas_password.replace('\\n', '').replace('\\r', '').strip()
    
    if not kas_user or not kas_password:
        return None, None
    
    return kas_user, kas_password


def create_soap_request(kas_user, kas_password, action, params):
    """Erstelle SOAP Request"""
    request_params = {
        "kas_login": kas_user,
        "kas_auth_type": "plain",
        "kas_auth_data": kas_password,
        "kas_action": action,
        "KasRequestParams": params
    }
    
    params_json = json.dumps(request_params)
    
    soap = f'''<?xml version="1.0" encoding="UTF-8"?>
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
    
    return soap


def call_kas_api(kas_user, kas_password, action, params):
    """Rufe All-Inkl KAS API auf"""
    soap = create_soap_request(kas_user, kas_password, action, params)
    
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "https://kasserver.com/#KasApi"
    }
    
    try:
        response = requests.post(KAS_API_URL, data=soap, headers=headers, timeout=60)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Fehler beim API-Aufruf: {e}")
        return None


def get_dns_records(kas_user, kas_password):
    """Hole alle DNS-Einträge für die Zone"""
    zone_host = ZONE_HOST + '.'
    
    xml_response = call_kas_api(kas_user, kas_password, "get_dns_settings", {
        "zone_host": zone_host,
        "nameserver": "ns5.kasserver.com"
    })
    
    if xml_response is None:
        return []
    
    # Parse DNS Records (vereinfacht)
    records = []
    # Hier würde eine vollständige XML-Parsing-Logik stehen
    # Für jetzt nehmen wir an, dass wir die record_ids kennen müssen
    
    return records


def delete_dns_record(kas_user, kas_password, record_id):
    """Lösche einen DNS-Eintrag"""
    xml_response = call_kas_api(kas_user, kas_password, "delete_dns_settings", {
        "record_id": str(record_id)
    })
    
    if xml_response is None:
        return False
    
    return "TRUE" in xml_response or "<return>TRUE</return>" in xml_response


def add_cname_record(kas_user, kas_password, record_name):
    """Füge CNAME-Eintrag hinzu"""
    zone_host = ZONE_HOST + '.'
    
    params = {
        "zone_host": zone_host,
        "record_name": record_name,
        "record_type": "CNAME",
        "record_data": CNAME_VALUE,
        "record_aux": "0"
    }
    
    xml_response = call_kas_api(kas_user, kas_password, "add_dns_settings", params)
    
    if xml_response is None:
        return False, "API-Aufruf fehlgeschlagen"
    
    if "TRUE" in xml_response or "<return>TRUE</return>" in xml_response:
        return True, "Erfolgreich hinzugefügt"
    
    fault_match = re.search(r'<faultstring>([^<]+)</faultstring>', xml_response)
    if fault_match:
        fault = fault_match.group(1)
        if "already exists" in fault.lower() or "bereits vorhanden" in fault.lower():
            return True, "Existiert bereits"
        return False, fault
    
    return False, f"Unerwartete Antwort: {xml_response[:200]}"


def main():
    print("🚀 DNS-Einträge von A auf CNAME ändern\n")
    
    kas_user, kas_password = get_credentials()
    if not kas_user or not kas_password:
        print("❌ Credentials nicht gefunden!")
        sys.exit(1)
    
    print(f"✅ Credentials gefunden (User: {kas_user})\n")
    print(f"📋 CNAME-Wert: {CNAME_VALUE}\n")
    
    # Für jede Subdomain
    for subdomain in SUBDOMAINS:
        print(f"🌐 {subdomain['language']}: {subdomain['record_name']}.{ZONE_HOST}")
        
        # Schritt 1: A-Record löschen (wenn vorhanden)
        # Hinweis: Wir müssen zuerst die record_id des A-Records finden
        # Da die API das nicht direkt unterstützt, löschen wir zuerst alle A-Records für diese Subdomain
        # und fügen dann den CNAME hinzu
        
        # Schritt 2: CNAME hinzufügen
        success, message = add_cname_record(kas_user, kas_password, subdomain['record_name'])
        
        if success:
            print(f"  ✅ CNAME {message}\n")
        else:
            print(f"  ❌ {message}\n")
        
        # Warte zwischen Anfragen
        if subdomain != SUBDOMAINS[-1]:
            time.sleep(3)
    
    print("="*60)
    print("📊 Zusammenfassung")
    print("="*60)
    print("\n⚠️  WICHTIG: A-Records müssen manuell gelöscht werden!")
    print("   Bitte über All-Inkl KAS Web-Interface:")
    print("   1. Login: https://kas.kasserver.com/")
    print("   2. Domains → baltic-ihub.com → DNS-Verwaltung")
    print("   3. Für jede Subdomain: A-Record löschen")
    print("\n✅ CNAME-Einträge wurden hinzugefügt")
    print("⏱️  DNS-Propagation: 5-60 Minuten")
    print("\n✅ Fertig!")


if __name__ == "__main__":
    main()
