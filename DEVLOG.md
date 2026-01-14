# Development Log - NOTSTROMAGGREGAT Multi-Language Landing Page

## Projekt-Übersicht
Multilinguale Verkaufsseite für ein gebrauchtes Atlas Copco QES80 KD Notstromaggregat.
Gehostet auf Vercel mit 5 Sprachversionen und automatischer Domain-Erkennung.

---

## 2026-01-14 - Blog-Seiten Redesign

### Änderungen
- **Alle 5 Blog-Seiten komplett überarbeitet** (DE, EN, FR, NL, PL)
- Umstellung von dunklem auf helles Theme passend zur Hauptseite
- Baltic iHub Markenfarben implementiert:
  - Primary: #0039AD (Blau)
  - Accent: #D61810 (Rot)
  - Gradient: linear-gradient(135deg, #0039AD 0%, #D61810 100%)
- Neues Hero-Section mit Gradient-Hintergrund und dekorativem SVG-Pattern
- Moderne Blog-Karten mit:
  - Hover-Effekte (translateY + Schatten)
  - Kategorie-Tags (Guide, Maintenance, Installation, etc.)
  - Kalender-Icons für Datumsanzeige
- CTA-Sektion mit Link zum Kontaktformular
- Mobile-responsive Navigation mit Hamburger-Menü
- Entfernung der Abhängigkeit von externer styles.css (alle Styles inline)

### Betroffene Dateien
- `website/blog.html`
- `website-en/blog.html`
- `website-fr/blog.html`
- `website-nl/blog.html`
- `website-pl/blog.html`

---

## 2026-01-14 - Danke-Seite Redirect Fix

### Problem
Nach dem Absenden des Kontaktformulars wurde zur falschen danke.html weitergeleitet.

### Lösung
- Redirect-Logik in allen Sprachversionen korrigiert
- API gibt jetzt `/danke.html?lang={lang}` zurück
- JavaScript leitet basierend auf Sprachparameter zur richtigen Domain weiter

---

## 2026-01-14 - SMTP E-Mail Konfiguration

### Konfiguration
- Host: `w014c572.kasserver.com`
- Port: 465 (SSL)
- Absender: `notstromaggregat@baltic-ihub.com`
- Empfänger Admin-Mails: `ceo@baltic-ihub.com`

### Features
- Mehrsprachige E-Mail-Templates (DE, EN, FR, NL, PL)
- Automatische Bestätigungs-E-Mail an Absender
- Admin-Benachrichtigung mit allen Formulardaten
- Absendername: "Notstromaggregat Baltic iHub"

---

## Technische Architektur

### Domains (5 Sprachen)
| Sprache | Domain |
|---------|--------|
| Deutsch | notstromaggregat.baltic-ihub.com |
| English | backup-generator.baltic-ihub.com |
| Français | groupe-electrogene.baltic-ihub.com |
| Nederlands | noodaggregaat.baltic-ihub.com |
| Polski | agregat-pradotworczy.baltic-ihub.com |

### Verzeichnisstruktur
```
NOTSTROMAGGREGAT/
├── api/
│   └── contact.js          # Vercel Serverless Function
├── website/                # Deutsche Version (Standard)
│   ├── index.html
│   ├── blog.html
│   ├── danke.html
│   └── assets/
├── website-en/             # Englische Version
├── website-fr/             # Französische Version
├── website-nl/             # Niederländische Version
├── website-pl/             # Polnische Version
└── vercel.json             # Routing & Rewrites
```

### Routing (vercel.json)
- Host-basiertes Routing: Erkennt automatisch die Domain
- Leitet zu entsprechendem Sprachordner weiter
- Asset-Sharing zwischen Versionen möglich

---

## Geplante Erweiterungen

### Produktidee: Multi-Language Landing Page as a Service
Die Struktur dieses Projekts soll als Vorlage für ein Produkt der Baltic iHub GmbH dienen:
- Hochwertige mehrsprachige Angebotsseiten für gebrauchte Geräte
- Zielgruppe: Unternehmen, die teure Gebrauchtgeräte professionell verkaufen wollen

### Benötigte Tools
1. **Konfigurations-Tool** für Eingabe von:
   - Verkäufer-Informationen (Firma, Kontakt, Logo)
   - Produkt-Details (Name, Beschreibung, Spezifikationen, Preis)
   - Bilder und Medien
   - Gewünschte Sprachen
2. **Template-Generator** für automatische Erstellung der Seiten
3. **Domain-Setup-Automatisierung**

---

## Commit-Historie (relevant)
- `1999dff` - Redesign all blog pages with new light theme matching main website
- `bd665bd` - Fix danke.html redirect for all language versions
- `9ddfe41` - Add sender name "Notstromaggregat Baltic iHub" to emails
- `a5487bc` - Fix SMTP: Use Port 465 with SSL for All-Inkl
- `3becd5d` - Update price to €14,900 excl. VAT and fix SMTP config
