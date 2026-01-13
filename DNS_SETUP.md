# DNS-Konfiguration für Vercel Deployment

**Datum:** 2026-01-11  
**Status:** ⏳ DNS-Einträge müssen bei All-Inkl hinzugefügt werden

## ✅ Vercel Domains hinzugefügt

Die folgenden Domains wurden erfolgreich zu Vercel hinzugefügt:
- `notstromaggregat.baltic-ihub.com` (DE)
- `backup-generator.baltic-ihub.com` (EN)
- `groupe-electrogene.baltic-ihub.com` (FR)
- `noodaggregaat.baltic-ihub.com` (NL)
- `agregat-pradotworczy.baltic-ihub.com` (PL)

## 📋 Benötigte DNS-Einträge bei All-Inkl

Für die Domain `baltic-ihub.com` müssen folgende A-Records bei All-Inkl hinzugefügt werden:

### 1. notstromaggregat.baltic-ihub.com
```
Typ: A
Name: notstromaggregat
Wert: 76.76.21.21
TTL: 3600 (oder Standard)
```

### 2. backup-generator.baltic-ihub.com (EN)
```
Typ: A
Name: backup-generator
Wert: 76.76.21.21
TTL: 3600 (oder Standard)
```

### 3. groupe-electrogene.baltic-ihub.com (FR)
```
Typ: A
Name: groupe-electrogene
Wert: 76.76.21.21
TTL: 3600 (oder Standard)
```

### 4. noodaggregaat.baltic-ihub.com (NL)
```
Typ: A
Name: noodaggregaat
Wert: 76.76.21.21
TTL: 3600 (oder Standard)
```

### 5. agregat-pradotworczy.baltic-ihub.com (PL)
```
Typ: A
Name: agregat-pradotworczy
Wert: 76.76.21.21
TTL: 3600 (oder Standard)
```

## 🔧 All-Inkl KAS API Konfiguration

Die DNS-Einträge können über die All-Inkl KAS API hinzugefügt werden:

### API-Aufruf (über MCP Hub)
```json
{
  "tool": "allinkl.add_dns_record",
  "args": {
    "zone_host": "baltic-ihub.com",
    "record_name": "notstromaggregat",
    "record_type": "A",
    "record_data": "76.76.21.21",
    "record_aux": "0"
  }
}
```

```json
{
  "tool": "allinkl.add_dns_record",
  "args": {
    "zone_host": "baltic-ihub.com",
    "record_name": "backup-generator",
    "record_type": "A",
    "record_data": "76.76.21.21",
    "record_aux": "0"
  }
}
```

```json
{
  "tool": "allinkl.add_dns_record",
  "args": {
    "zone_host": "baltic-ihub.com",
    "record_name": "groupe-electrogene",
    "record_type": "A",
    "record_data": "76.76.21.21",
    "record_aux": "0"
  }
}
```

```json
{
  "tool": "allinkl.add_dns_record",
  "args": {
    "zone_host": "baltic-ihub.com",
    "record_name": "noodaggregaat",
    "record_type": "A",
    "record_data": "76.76.21.21",
    "record_aux": "0"
  }
}
```

```json
{
  "tool": "allinkl.add_dns_record",
  "args": {
    "zone_host": "baltic-ihub.com",
    "record_name": "agregat-pradotworczy",
    "record_type": "A",
    "record_data": "76.76.21.21",
    "record_aux": "0"
  }
}
```

## 📝 Manuelle Konfiguration (All-Inkl KAS)

1. Login zu All-Inkl KAS: https://kas.kasserver.com/
2. Navigiere zu: **Domains** → **baltic-ihub.com** → **DNS-Verwaltung**
3. Füge die beiden A-Records hinzu (siehe oben)

## ⏱️ Propagation

Nach dem Hinzufügen der DNS-Einträge:
- DNS-Propagation: 5-60 Minuten
- Vercel-Verifizierung: Automatisch (E-Mail-Benachrichtigung)

## ✅ Verifizierung

Nach der DNS-Propagation:
1. Vercel sendet automatisch eine E-Mail-Bestätigung
2. Domains sind dann live unter:
   - https://notstromaggregat.baltic-ihub.com (DE)
   - https://backup-generator.baltic-ihub.com (EN)
   - https://groupe-electrogene.baltic-ihub.com (FR)
   - https://noodaggregaat.baltic-ihub.com (NL)
   - https://agregat-pradotworczy.baltic-ihub.com (PL)

## 🔍 Aktuelle DNS-Einträge prüfen

```bash
# DNS-Einträge prüfen
dig notstromaggregat.baltic-ihub.com
dig backup-generator.baltic-ihub.com
dig groupe-electrogene.baltic-ihub.com
dig noodaggregaat.baltic-ihub.com
dig agregat-pradotworczy.baltic-ihub.com
```

## 🔧 Automatisches Hinzufügen via Script

Es gibt zwei Python-Skripte zum automatischen Hinzufügen der DNS-Einträge:

### Option 1: Über MCP Hub (empfohlen)
```bash
export MCP_HUB_TOKEN=$(op read 'op://Automation/MCP Hub Token/credential')
python3 scripts/add_dns_via_mcp_hub.py
```

### Option 2: Direkt über All-Inkl KAS API
```bash
export ALL_INKL_KAS_USER=w014c572
export ALL_INKL_KAS_PASSWORD=$(op read 'op://Automation/All-Inkl KAS (w014c572)/password')
python3 scripts/add_dns_records_allinkl.py
```

## 📚 Weitere Informationen

- Vercel Domain Docs: https://vercel.com/docs/concepts/projects/domains
- All-Inkl KAS API: https://kasapi.kasserver.com/doc/
