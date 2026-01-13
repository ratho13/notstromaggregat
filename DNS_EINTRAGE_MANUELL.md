# DNS-Einträge manuell bei All-Inkl hinzufügen

**Datum:** 2026-01-13  
**Status:** ⚠️ API-Aufrufe haben Probleme (kas_login_syntax_incorrect, ip_blocked)

## 📋 Benötigte DNS-Einträge

Für die Domain `baltic-ihub.com` müssen folgende **A-Records** bei All-Inkl hinzugefügt werden:

| Sprache | Subdomain | Typ | Wert | TTL |
|---------|-----------|-----|------|-----|
| DE | `notstromaggregat` | A | `76.76.21.21` | 3600 |
| EN | `backup-generator` | A | `76.76.21.21` | 3600 |
| FR | `groupe-electrogene` | A | `76.76.21.21` | 3600 |
| NL | `noodaggregaat` | A | `76.76.21.21` | 3600 |
| PL | `agregat-pradotworczy` | A | `76.76.21.21` | 3600 |

## 🔧 Schritt-für-Schritt Anleitung

### 1. Login zu All-Inkl KAS
1. Öffne: https://kas.kasserver.com/
2. Login mit deinen All-Inkl KAS Credentials

### 2. Navigiere zur DNS-Verwaltung
1. Klicke auf **"Domains"** im Hauptmenü
2. Wähle **"baltic-ihub.com"** aus der Liste
3. Klicke auf **"DNS-Verwaltung"** oder **"DNS-Einstellungen"**

### 3. DNS-Einträge hinzufügen

Für jeden der 5 Einträge:

1. Klicke auf **"Neuer DNS-Eintrag"** oder **"DNS-Eintrag hinzufügen"**
2. Fülle die Felder aus:
   - **Typ:** `A`
   - **Name:** `notstromaggregat` (ohne `.baltic-ihub.com`)
   - **Wert:** `76.76.21.21`
   - **TTL:** `3600` (oder Standard)
3. Klicke auf **"Speichern"** oder **"Hinzufügen"**
4. Wiederhole für alle 5 Subdomains

### 4. Verifizierung

Nach dem Hinzufügen:
```bash
# DNS-Einträge prüfen
dig notstromaggregat.baltic-ihub.com
dig backup-generator.baltic-ihub.com
dig groupe-electrogene.baltic-ihub.com
dig noodaggregaat.baltic-ihub.com
dig agregat-pradotworczy.baltic-ihub.com
```

Erwartete Antwort: `76.76.21.21`

## ⏱️ Timing

- **DNS-Propagation:** 5-60 Minuten
- **Vercel-Verifizierung:** Automatisch (E-Mail-Benachrichtigung)
- **Live-Status:** Nach Propagation sind alle Domains erreichbar

## ✅ Nach dem Hinzufügen

Vercel sendet automatisch E-Mail-Bestätigungen für jede Domain, sobald die DNS-Einträge propagiert sind.

Die Domains sind dann live unter:
- https://notstromaggregat.baltic-ihub.com (DE)
- https://backup-generator.baltic-ihub.com (EN)
- https://groupe-electrogene.baltic-ihub.com (FR)
- https://noodaggregaat.baltic-ihub.com (NL)
- https://agregat-pradotworczy.baltic-ihub.com (PL)

## 🔍 Troubleshooting

### Problem: DNS-Eintrag wird nicht angezeigt
- Warte 5-10 Minuten auf Propagation
- Prüfe mit `dig` ob der Eintrag existiert

### Problem: Vercel-Verifizierung schlägt fehl
- Prüfe ob der A-Record korrekt auf `76.76.21.21` zeigt
- Warte auf vollständige DNS-Propagation
- Prüfe Vercel Dashboard für Details

## 📚 Weitere Informationen

- All-Inkl KAS: https://kas.kasserver.com/
- Vercel Domain Docs: https://vercel.com/docs/concepts/projects/domains
- DNS Propagation Check: https://www.whatsmydns.net/
