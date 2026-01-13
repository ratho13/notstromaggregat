#!/usr/bin/env python3
"""
A-Records für Subdomains löschen (damit CNAME funktioniert)
"""

import os
import sys
import json
import requests
import time
import re

SUBDOMAINS = [
    {"record_name": "notstromaggregat", "language": "DE"},
    {"record_name": "backup-generator", "language": "EN"},
    {"record_name": "groupe-electrogene", "language": "FR"},
    {"record_name": "noodaggregaat", "language": "NL"},
    {"record_name": "agregat-pradotworczy", "language": "PL"},
]

ZONE_HOST = "baltic-ihub.com"
KAS_API_URL = "https://kasapi.kasserver.com/soap/KasApi.php"


def get_credentials():
    """Hole Credentials"""
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
        print(f"❌ Fehler: {e}")
        return None


def parse_dns_records(xml_response):
    """Parse DNS Records aus XML"""
    records = []
    
    # Suche nach allen record-Einträgen
    pattern = r'<item xsi:type="ns2:Map">(.*?)</item>'
    matches = re.finditer(pattern, xml_response, re.DOTALL)
    
    for match in matches:
        record_xml = match.group(1)
        
        record_id = re.search(r'<key[^>]*>record_id</key>\s*<value[^>]*>([^<]+)</value>', record_xml)
        record_name = re.search(r'<key[^>]*>record_name</key>\s*<value[^>]*>([^<]+)</value>', record_xml)
        record_type = re.search(r'<key[^>]*>record_type</key>\s*<value[^>]*>([^<]+)</value>', record_xml)
        record_data = re.search(r'<key[^>]*>record_data</key>\s*<value[^>]*>([^<]+)</value>', record_xml)
        
        if record_id and record_name and record_type:
            records.append({
                "id": record_id.group(1),
                "name": record_name.group(1) if record_name else "",
                "type": record_type.group(1),
                "data": record_data.group(1) if record_data else ""
            })
    
    return records


def delete_dns_record(kas_user, kas_password, record_id):
    """Lösche DNS-Eintrag"""
    xml_response = call_kas_api(kas_user, kas_password, "delete_dns_settings", {
        "record_id": str(record_id)
    })
    
    if xml_response is None:
        return False, "API-Aufruf fehlgeschlagen"
    
    if "TRUE" in xml_response or "<return>TRUE</return>" in xml_response:
        return True, "Erfolgreich gelöscht"
    
    fault_match = re.search(r'<faultstring>([^<]+)</faultstring>', xml_response)
    if fault_match:
        return False, fault_match.group(1)
    
    return False, f"Unerwartete Antwort: {xml_response[:200]}"


def main():
    print("🚀 A-Records für Subdomains löschen\n")
    
    kas_user, kas_password = get_credentials()
    if not kas_user or not kas_password:
        print("❌ Credentials nicht gefunden!")
        sys.exit(1)
    
    print(f"✅ Credentials gefunden (User: {kas_user})\n")
    
    # Hole alle DNS-Einträge
    zone_host = ZONE_HOST + '.'
    print("📋 Hole DNS-Einträge...")
    xml_response = call_kas_api(kas_user, kas_password, "get_dns_settings", {
        "zone_host": zone_host,
        "nameserver": "ns5.kasserver.com"
    })
    
    if xml_response is None:
        print("❌ Konnte DNS-Einträge nicht abrufen")
        sys.exit(1)
    
    records = parse_dns_records(xml_response)
    print(f"✅ {len(records)} DNS-Einträge gefunden\n")
    
    # Finde und lösche A-Records für unsere Subdomains
    deleted_count = 0
    for subdomain in SUBDOMAINS:
        print(f"🌐 {subdomain['language']}: {subdomain['record_name']}.{ZONE_HOST}")
        
        # Finde A-Record für diese Subdomain
        a_records = [r for r in records if r['name'] == subdomain['record_name'] and r['type'] == 'A']
        
        if not a_records:
            print(f"  ⚠️  Kein A-Record gefunden (bereits gelöscht oder nicht vorhanden)\n")
            continue
        
        for a_record in a_records:
            print(f"  📝 Lösche A-Record: {a_record['name']} → {a_record['data']} (ID: {a_record['id']})")
            success, message = delete_dns_record(kas_user, kas_password, a_record['id'])
            
            if success:
                print(f"  ✅ {message}\n")
                deleted_count += 1
            else:
                print(f"  ❌ {message}\n")
        
        time.sleep(2)
    
    print("="*60)
    print("📊 Zusammenfassung")
    print("="*60)
    print(f"✅ Gelöscht: {deleted_count} A-Record(s)")
    print("\n⏱️  DNS-Propagation: 5-60 Minuten")
    print("✅ CNAME-Einträge sollten jetzt funktionieren")
    print("\n✅ Fertig!")


if __name__ == "__main__":
    main()
