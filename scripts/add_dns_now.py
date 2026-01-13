#!/usr/bin/env python3
"""
DNS-Einträge bei All-Inkl hinzufügen - Direkter Aufruf
"""

import subprocess
import json
import requests
import sys

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
    """Hole Credentials aus 1Password"""
    try:
        # Versuche Item-Name mit Anführungszeichen
        result = subprocess.run(
            ['op', 'item', 'get', 'All-Inkl KAS (w014c572)', 
             '--vault', 'Automation', 
             '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        item_data = json.loads(result.stdout)
        
        username = None
        password = None
        
        # Suche nach username und password Feldern
        for field in item_data.get('fields', []):
            if field.get('label') == 'username' or field.get('id') == 'username':
                username = field.get('value')
            elif field.get('label') == 'password' or field.get('id') == 'password':
                password = field.get('value')
        
        if username and password:
            return username, password
    except Exception as e:
        print(f"⚠️  Fehler beim Lesen aus 1Password: {e}")
    
    return None, None

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

def add_dns_record(kas_user, kas_password, record_name):
    """Füge DNS-Eintrag hinzu"""
    zone_host = ZONE_HOST + '.'
    
    params = {
        "zone_host": zone_host,
        "record_name": record_name,
        "record_type": "A",
        "record_data": VERCEL_IP,
        "record_aux": "0"
    }
    
    soap = create_soap_request(kas_user, kas_password, "add_dns_settings", params)
    
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "https://kasserver.com/#KasApi"
    }
    
    try:
        response = requests.post(KAS_API_URL, data=soap, headers=headers, timeout=60)
        response.raise_for_status()
        xml_response = response.text
        
        if "TRUE" in xml_response or "<return>TRUE</return>" in xml_response:
            return True, "Erfolgreich"
        elif "faultstring" in xml_response:
            fault_start = xml_response.find("<faultstring>")
            fault_end = xml_response.find("</faultstring>")
            if fault_start != -1 and fault_end != -1:
                fault_msg = xml_response[fault_start+13:fault_end]
                if "already exists" in fault_msg.lower() or "bereits vorhanden" in fault_msg.lower():
                    return True, "Existiert bereits"
                return False, fault_msg
        return False, f"Unerwartete Antwort: {xml_response[:200]}"
    except Exception as e:
        return False, str(e)

def main():
    print("🚀 DNS-Einträge bei All-Inkl hinzufügen\n")
    
    # Credentials holen
    print("🔑 Hole Credentials aus 1Password...")
    kas_user, kas_password = get_credentials()
    
    if not kas_user or not kas_password:
        print("❌ Credentials nicht gefunden!")
        print("\nBitte manuell setzen:")
        print("  export ALL_INKL_KAS_USER=w014c572")
        print("  export ALL_INKL_KAS_PASSWORD=<password>")
        sys.exit(1)
    
    print(f"✅ Credentials gefunden (User: {kas_user})\n")
    
    # DNS-Einträge hinzufügen
    success_count = 0
    failed = []
    
    for record in DNS_RECORDS:
        print(f"🌐 {record['language']}: {record['record_name']}.{ZONE_HOST}")
        success, message = add_dns_record(kas_user, kas_password, record['record_name'])
        
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
