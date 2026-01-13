# Bilder für Notstromaggregat-Website

## 📋 Benötigte Bilder

Die folgenden Bilder müssen in den jeweiligen `assets/images` Verzeichnissen platziert werden:

### Für alle Sprachversionen (website, website-en, website-fr, website-nl, website-pl):

#### Hero-Bild:
- `assets/images/hero.jpg` - Hauptbild des Notstromaggregats (für Hero-Section)

#### OG-Image (Social Media):
- `assets/images/og-image.jpg` - Open Graph Bild (1200x630px empfohlen)

#### Galerie-Bilder (8 Bilder):
- `assets/images/gallery-1.jpg` - Atlas Copco QES80 Seitenansicht
- `assets/images/gallery-2.jpg` - Atlas Copco QES80 Rückansicht
- `assets/images/gallery-3.jpg` - Deep Sea Electronics Bedienfeld
- `assets/images/gallery-4.jpg` - Display Betriebsstunden 24h
- `assets/images/gallery-5.jpg` - Cummins Motor Innenansicht
- `assets/images/gallery-6.jpg` - Atlas Copco Typenschild
- `assets/images/gallery-7.jpg` - Generator Alternator
- `assets/images/gallery-8.jpg` - Motor mit Batterie

## 📁 Verzeichnisstruktur

```
Notstromaggregat/
├── website/
│   └── assets/
│       └── images/
│           ├── hero.jpg
│           ├── og-image.jpg
│           ├── gallery-1.jpg
│           ├── gallery-2.jpg
│           ├── gallery-3.jpg
│           ├── gallery-4.jpg
│           ├── gallery-5.jpg
│           ├── gallery-6.jpg
│           ├── gallery-7.jpg
│           └── gallery-8.jpg
├── website-en/
│   └── assets/
│       └── images/
│           └── [gleiche Bilder]
├── website-fr/
│   └── assets/
│       └── images/
│           └── [gleiche Bilder]
├── website-nl/
│   └── assets/
│       └── images/
│           └── [gleiche Bilder]
└── website-pl/
    └── assets/
        └── images/
            └── [gleiche Bilder]
```

## 🔧 Aktueller Status

- ✅ Verzeichnisse erstellt
- ⚠️ Bilder fehlen noch
- ✅ Vercel-Konfiguration korrigiert (Assets werden korrekt geroutet)

## 📝 Nächste Schritte

1. Bilder in die entsprechenden `assets/images` Verzeichnisse kopieren
2. Für alle Sprachversionen (DE, EN, FR, NL, PL) die gleichen Bilder verwenden
3. Nach dem Hinzufügen: `git add` und `git commit`
4. Vercel Deployment wird automatisch aktualisiert

## 🖼️ Bildformate

- **Format:** JPG oder PNG
- **Hero-Bild:** Empfohlen 1200x800px oder größer
- **OG-Image:** 1200x630px (für Social Media)
- **Galerie-Bilder:** Empfohlen mindestens 800x600px

## ⚠️ Wichtig

Die Bilder müssen in **jedem** Sprachverzeichnis vorhanden sein:
- `website/assets/images/`
- `website-en/assets/images/`
- `website-fr/assets/images/`
- `website-nl/assets/images/`
- `website-pl/assets/images/`
