# DNS-Konfiguration für Vercel Deployment

**Datum:** 2026-01-11  
**Status:** ⏳ DNS-Einträge müssen bei All-Inkl hinzugefügt werden

## ✅ Vercel Domains hinzugefügt

Die folgenden Domains wurden erfolgreich zu Vercel hinzugefügt:
- `notstromaggregat.baltic-ihub.com`
- `backup-generator.baltic-ihub.com`

## 📋 Benötigte DNS-Einträge bei All-Inkl

Für die Domain `baltic-ihub.com` müssen folgende A-Records bei All-Inkl hinzugefügt werden:

### 1. notstromaggregat.baltic-ihub.com
```
Typ: A
Name: notstromaggregat
Wert: 76.76.21.21
TTL: 3600 (oder Standard)
```

### 2. backup-generator.baltic-ihub.com
```
Typ: A
Name: backup-generator
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
   - https://notstromaggregat.baltic-ihub.com
   - https://backup-generator.baltic-ihub.com

## 🔍 Aktuelle DNS-Einträge prüfen

```bash
# DNS-Einträge prüfen
dig notstromaggregat.baltic-ihub.com
dig backup-generator.baltic-ihub.com
```

## 📚 Weitere Informationen

- Vercel Domain Docs: https://vercel.com/docs/concepts/projects/domains
- All-Inkl KAS API: https://kasapi.kasserver.com/doc/
