# CNAME-Einträge manuell hinzufügen

**Datum:** 2026-01-13  
**Status:** ⚠️ Muss manuell über All-Inkl KAS Web-Interface durchgeführt werden

## 📋 Vercel-Anweisungen

Gemäß Vercel müssen für alle Subdomains **CNAME-Einträge** erstellt werden.

### CNAME-Wert:
```
7c6be46a197dc3f0.vercel-dns-017.com.
```

## 🔧 Manuelle Schritte in All-Inkl KAS

### 1. Login
- Gehe zu: https://kas.kasserver.com/
- Login mit deinen All-Inkl Credentials

### 2. Navigiere zu DNS-Verwaltung
- Links im Menü: **Webbaukasten** → **DNS-Einstellungen**
- Oder direkt: Domains → **baltic-ihub.com** → **DNS-Verwaltung**

### 3. Für jede Subdomain: CNAME-Eintrag hinzufügen

Klicke auf **"Hinzufügen"** oder **"Neu"** und erstelle für jede Subdomain einen CNAME-Eintrag:

| Sprache | Name | Typ | Data/Value |
|---------|------|-----|------------|
| DE | `notstromaggregat` | CNAME | `7c6be46a197dc3f0.vercel-dns-017.com.` |
| EN | `backup-generator` | CNAME | `7c6be46a197dc3f0.vercel-dns-017.com.` |
| FR | `groupe-electrogene` | CNAME | `7c6be46a197dc3f0.vercel-dns-017.com.` |
| NL | `noodaggregaat` | CNAME | `7c6be46a197dc3f0.vercel-dns-017.com.` |
| PL | `agregat-pradotworczy` | CNAME | `7c6be46a197dc3f0.vercel-dns-017.com.` |

**Wichtig:**
- **Typ:** CNAME (nicht A!)
- **Name:** Nur der Subdomain-Name (ohne `.baltic-ihub.com`)
- **Data/Value:** `7c6be46a197dc3f0.vercel-dns-017.com.` (mit Punkt am Ende!)

### 4. A-Records löschen

Nachdem die CNAME-Einträge erstellt wurden, müssen die **alten A-Records gelöscht** werden:

Für jede Subdomain:
- Finde den A-Record (Typ: A, Name: subdomain, Wert: `76.76.21.21`)
- Klicke auf das **Löschen-Symbol** (Papierkorb) in der "Aktion"-Spalte
- Bestätige die Löschung

**Wichtig:** Löschen nur die A-Records, nicht andere Einträge (MX, TXT, NS, etc.)!

## ⏱️ Nach der Änderung

- **DNS-Propagation:** 5-60 Minuten
- **Vercel-Verifizierung:** Vercel prüft automatisch die DNS-Einträge
- **Status in Vercel:** Sollte von "Invalid Configuration" auf "Valid" wechseln

## 🔍 Verifizierung

Nach 5-60 Minuten kannst du prüfen:

```bash
dig notstromaggregat.baltic-ihub.com
dig backup-generator.baltic-ihub.com
dig groupe-electrogene.baltic-ihub.com
dig noodaggregaat.baltic-ihub.com
dig agregat-pradotworczy.baltic-ihub.com
```

**Erwartete Antwort:** CNAME auf `7c6be46a197dc3f0.vercel-dns-017.com.`

## 📝 Zusammenfassung

1. ✅ CNAME-Einträge für alle 5 Subdomains hinzufügen
2. ✅ A-Records für alle 5 Subdomains löschen
3. ⏱️ 5-60 Minuten warten (DNS-Propagation)
4. ✅ In Vercel Dashboard prüfen (Status sollte "Valid" sein)
