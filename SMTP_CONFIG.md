# SMTP Konfiguration für notstromaggregat@baltic-ihub.com

## All-Inkl SMTP Einstellungen

**E-Mail-Adresse:** notstromaggregat@baltic-ihub.com  
**SMTP Server:** w014c572.kasserver.com  
**SMTP Port:** 587 (STARTTLS) oder 465 (SSL/TLS)  
**Benutzername:** notstromaggregat@baltic-ihub.com (vollständige E-Mail-Adresse)  
**Passwort:** [Aus 1Password Vault "Automation" - Item "All-Inkl KAS (w014c572)"]  
**Verschlüsselung:** STARTTLS (Port 587) oder SSL/TLS (Port 465)

## Verwendung in N8N / Automatisierungen

### N8N SMTP Node Konfiguration:
- **Host:** w014c572.kasserver.com
- **Port:** 587
- **Secure:** false (für STARTTLS) oder true (für SSL auf Port 465)
- **User:** notstromaggregat@baltic-ihub.com
- **Password:** [Aus 1Password]
- **From:** notstromaggregat@baltic-ihub.com

### Node.js / TypeScript Beispiel:
```typescript
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  host: 'w014c572.kasserver.com',
  port: 587,
  secure: false, // true für Port 465
  auth: {
    user: 'notstromaggregat@baltic-ihub.com',
    pass: process.env.ALL_INKL_SMTP_PASSWORD
  }
});
```

## Wichtige Hinweise

1. **Benutzername:** Muss die vollständige E-Mail-Adresse sein, nicht nur der lokale Teil
2. **Port 587:** STARTTLS - Verbindung startet unverschlüsselt, wird dann verschlüsselt
3. **Port 465:** SSL/TLS - Verbindung ist von Anfang an verschlüsselt
4. **Passwort:** Nie im Code hardcoden, immer aus Environment Variables oder 1Password

## Troubleshooting

- **Fehler "Authentication failed":** Prüfe ob Benutzername die vollständige E-Mail-Adresse ist
- **Fehler "Connection timeout":** Prüfe Firewall-Einstellungen, Port 587/465 muss offen sein
- **Fehler "STARTTLS not supported":** Verwende Port 465 mit `secure: true`
