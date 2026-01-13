# DNS-Einträge: A-Record → CNAME

**Datum:** 2026-01-13  
**Status:** ⚠️ A-Records müssen manuell gelöscht werden

## 📋 Vercel-Anweisungen

Gemäß Vercel müssen für alle Subdomains die **A-Records gelöscht** und **CNAME-Einträge verwendet** werden.

### CNAME-Wert (neu):
```
7c6be46a197dc3f0.vercel-dns-017.com.
```

### Alte Werte (funktionieren noch, aber nicht empfohlen):
- `cname.vercel-dns.com`
- `76.76.21.21` (A-Record)

## 🔧 Benötigte Änderungen bei All-Inkl

Für jede Subdomain muss der **A-Record gelöscht** werden:

| Sprache | Subdomain | Aktion |
|---------|-----------|--------|
| DE | `notstromaggregat` | A-Record löschen |
| EN | `backup-generator` | A-Record löschen |
| FR | `groupe-electrogene` | A-Record löschen |
| NL | `noodaggregaat` | A-Record löschen |
| PL | `agregat-pradotworczy` | A-Record löschen |

### ✅ CNAME-Einträge
Die CNAME-Einträge existieren bereits und zeigen auf:
- `7c6be46a197dc3f0.vercel-dns-017.com.`

## 📝 Manuelle Schritte

1. **Login zu All-Inkl KAS:** https://kas.kasserver.com/
2. **Navigiere zu:** Domains → baltic-ihub.com → DNS-Verwaltung
3. **Für jede Subdomain:**
   - Finde den A-Record (Typ: A, Name: subdomain, Wert: 76.76.21.21)
   - Lösche diesen A-Record
   - Der CNAME-Eintrag sollte bereits vorhanden sein

## ⏱️ Nach der Änderung

- DNS-Propagation: 5-60 Minuten
- Vercel wird automatisch die Domains verifizieren
- Status in Vercel Dashboard sollte von "Invalid Configuration" zu "Valid" wechseln

## 🔍 Verifizierung

Nach der Propagation:
```bash
dig notstromaggregat.baltic-ihub.com
dig backup-generator.baltic-ihub.com
# etc.
```

Erwartete Antwort: CNAME auf `7c6be46a197dc3f0.vercel-dns-017.com.`
