/**
 * Contact Form API - Vercel Serverless Function
 * Handles form submissions and sends emails
 */

const nodemailer = require('nodemailer');

// Language configurations
const LANGUAGES = {
  de: {
    subject: 'Neue Anfrage: Atlas Copco QES80 KD Notstromaggregat',
    confirmationSubject: 'Ihre Anfrage wurde erhalten - Baltic iHub',
    thankYou: 'Vielen Dank',
    received: 'Ihre Anfrage wurde erfolgreich übermittelt.',
    greeting: 'Hallo',
    intro: 'vielen Dank für Ihre Anfrage zum Atlas Copco QES80 KD Notstromaggregat.',
    receivedText: 'Wir haben Ihre Nachricht erhalten und werden uns schnellstmöglich bei Ihnen melden.',
    details: 'Ihre Anfrage-Details:',
    nameLabel: 'Name',
    messageLabel: 'Ihre Nachricht',
    footer: 'Mit freundlichen Grüßen,<br>Das Team der Baltic iHub GmbH',
    contact: 'Bei Fragen erreichen Sie uns unter:<br>notstromaggregat@baltic-ihub.com',
  },
  en: {
    subject: 'New Inquiry: Atlas Copco QES80 KD Backup Generator',
    confirmationSubject: 'Your inquiry has been received - Baltic iHub',
    thankYou: 'Thank You',
    received: 'Your inquiry has been successfully submitted.',
    greeting: 'Hello',
    intro: 'thank you for your inquiry about the Atlas Copco QES80 KD Backup Generator.',
    receivedText: 'We have received your message and will get back to you as soon as possible.',
    details: 'Your inquiry details:',
    nameLabel: 'Name',
    messageLabel: 'Your message',
    footer: 'Best regards,<br>The Baltic iHub GmbH Team',
    contact: 'If you have any questions, please contact us at:<br>notstromaggregat@baltic-ihub.com',
  },
  fr: {
    subject: 'Nouvelle demande: Groupe Électrogène Atlas Copco QES80 KD',
    confirmationSubject: 'Votre demande a été reçue - Baltic iHub',
    thankYou: 'Merci',
    received: 'Votre demande a été envoyée avec succès.',
    greeting: 'Bonjour',
    intro: 'merci pour votre demande concernant le Groupe Électrogène Atlas Copco QES80 KD.',
    receivedText: 'Nous avons bien reçu votre message et vous répondrons dans les plus brefs délais.',
    details: 'Détails de votre demande:',
    nameLabel: 'Nom',
    messageLabel: 'Votre message',
    footer: 'Cordialement,<br>L\'équipe de Baltic iHub GmbH',
    contact: 'Pour toute question, contactez-nous à:<br>notstromaggregat@baltic-ihub.com',
  },
  nl: {
    subject: 'Nieuwe aanvraag: Atlas Copco QES80 KD Noodaggregaat',
    confirmationSubject: 'Uw aanvraag is ontvangen - Baltic iHub',
    thankYou: 'Bedankt',
    received: 'Uw aanvraag is succesvol verzonden.',
    greeting: 'Hallo',
    intro: 'bedankt voor uw aanvraag over het Atlas Copco QES80 KD Noodaggregaat.',
    receivedText: 'We hebben uw bericht ontvangen en zullen zo spoedig mogelijk contact met u opnemen.',
    details: 'Uw aanvraagdetails:',
    nameLabel: 'Naam',
    messageLabel: 'Uw bericht',
    footer: 'Met vriendelijke groet,<br>Het Baltic iHub GmbH Team',
    contact: 'Voor vragen kunt u ons bereiken op:<br>notstromaggregat@baltic-ihub.com',
  },
  pl: {
    subject: 'Nowe zapytanie: Agregat Prądotwórczy Atlas Copco QES80 KD',
    confirmationSubject: 'Twoje zapytanie zostało otrzymane - Baltic iHub',
    thankYou: 'Dziękujemy',
    received: 'Twoje zapytanie zostało pomyślnie wysłane.',
    greeting: 'Witam',
    intro: 'dziękujemy za zapytanie dotyczące Agregatu Prądotwórczego Atlas Copco QES80 KD.',
    receivedText: 'Otrzymaliśmy Państwa wiadomość i skontaktujemy się z Państwem tak szybko, jak to możliwe.',
    details: 'Szczegóły Państwa zapytania:',
    nameLabel: 'Imię i nazwisko',
    messageLabel: 'Państwa wiadomość',
    footer: 'Z poważaniem,<br>Zespół Baltic iHub GmbH',
    contact: 'W przypadku pytań prosimy o kontakt:<br>notstromaggregat@baltic-ihub.com',
  },
};

// SMTP Configuration - All-Inkl uses Port 465 with SSL
const getSMTPConfig = () => {
  return {
    host: 'w014c572.kasserver.com',
    port: 465,
    secure: true,
    auth: {
      user: 'notstromaggregat@baltic-ihub.com',
      pass: process.env.ALL_INKL_SMTP_PASSWORD || process.env.ALL_INKL_KAS_PASSWORD,
    },
    tls: {
      rejectUnauthorized: false
    }
  };
};

// Email templates
const getAdminEmailHTML = (data, lang) => {
  const langConfig = LANGUAGES[lang] || LANGUAGES.de;
  
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background: #0039AD; color: white; padding: 20px; text-align: center; }
    .content { background: #f8fafc; padding: 20px; }
    .field { margin: 15px 0; }
    .label { font-weight: bold; color: #0039AD; }
    .value { margin-top: 5px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>${langConfig.subject}</h2>
    </div>
    <div class="content">
      <div class="field">
        <div class="label">Name:</div>
        <div class="value">${data.name}</div>
      </div>
      <div class="field">
        <div class="label">E-Mail:</div>
        <div class="value">${data.email}</div>
      </div>
      ${data.company ? `
      <div class="field">
        <div class="label">Firma:</div>
        <div class="value">${data.company}</div>
      </div>
      ` : ''}
      <div class="field">
        <div class="label">Nachricht:</div>
        <div class="value" style="white-space: pre-wrap;">${data.message}</div>
      </div>
      <div class="field">
        <div class="label">Sprache:</div>
        <div class="value">${lang.toUpperCase()}</div>
      </div>
      <div class="field">
        <div class="label">Zeitstempel:</div>
        <div class="value">${new Date().toLocaleString('de-DE')}</div>
      </div>
    </div>
  </div>
</body>
</html>
  `;
};

const getConfirmationEmailHTML = (data, lang) => {
  const langConfig = LANGUAGES[lang] || LANGUAGES.de;
  const t = langConfig;
  
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: 'Inter', Arial, sans-serif; line-height: 1.6; color: #111827; margin: 0; padding: 0; }
    .container { max-width: 600px; margin: 0 auto; background: #FFFFFF; }
    .header { background: linear-gradient(135deg, #0039AD 0%, #D61810 100%); color: white; padding: 40px 20px; text-align: center; }
    .header h1 { margin: 0; font-size: 28px; }
    .content { padding: 40px 20px; background: #FAF9F6; }
    .message-box { background: white; border-left: 4px solid #0039AD; padding: 20px; margin: 20px 0; }
    .details { background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0; }
    .detail-item { margin: 10px 0; }
    .label { font-weight: 600; color: #0039AD; }
    .footer { background: #1E3A5F; color: white; padding: 30px 20px; text-align: center; }
    .footer a { color: #D61810; text-decoration: none; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>${t.thankYou}!</h1>
    </div>
    <div class="content">
      <p><strong>${t.greeting} ${data.name},</strong></p>
      <p>${t.intro}</p>
      
      <div class="message-box">
        <p style="margin: 0;">${t.receivedText}</p>
      </div>
      
      <div class="details">
        <h3 style="margin-top: 0; color: #0039AD;">${t.details}</h3>
        <div class="detail-item">
          <span class="label">${t.nameLabel}:</span> ${data.name}
        </div>
        <div class="detail-item">
          <span class="label">E-Mail:</span> ${data.email}
        </div>
        ${data.company ? `
        <div class="detail-item">
          <span class="label">Firma:</span> ${data.company}
        </div>
        ` : ''}
        <div class="detail-item">
          <span class="label">${t.messageLabel}:</span>
          <div style="margin-top: 10px; white-space: pre-wrap; color: #475569;">${data.message}</div>
        </div>
      </div>
      
      <p style="margin-top: 30px;">${t.contact}</p>
    </div>
    <div class="footer">
      <p style="margin: 0;">${t.footer}</p>
      <p style="margin: 10px 0 0 0; font-size: 14px; color: #94a3b8;">
        Baltic iHub GmbH | Ein Unternehmen der THOR Holding
      </p>
    </div>
  </div>
</body>
</html>
  `;
};

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { name, email, company, message, language = 'de' } = req.body;

    // Validation
    if (!name || !email || !message) {
      return res.status(400).json({ error: 'Name, E-Mail und Nachricht sind erforderlich' });
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ error: 'Ungültige E-Mail-Adresse' });
    }

    // Create transporter
    const transporter = nodemailer.createTransport(getSMTPConfig());

    const lang = (language || 'de').toLowerCase().substring(0, 2);
    const langConfig = LANGUAGES[lang] || LANGUAGES.de;

    // Send email to admin
    await transporter.sendMail({
      from: '"Notstromaggregat Baltic iHub" <notstromaggregat@baltic-ihub.com>',
      to: 'ceo@baltic-ihub.com',
      replyTo: email,
      subject: langConfig.subject,
      html: getAdminEmailHTML({ name, email, company, message }, lang),
      text: `
Neue Anfrage: ${langConfig.subject}

Name: ${name}
E-Mail: ${email}
${company ? `Firma: ${company}` : ''}

Nachricht:
${message}

Sprache: ${lang.toUpperCase()}
Zeitstempel: ${new Date().toLocaleString('de-DE')}
      `.trim(),
    });

    // Send confirmation email to user
    await transporter.sendMail({
      from: '"Notstromaggregat Baltic iHub" <notstromaggregat@baltic-ihub.com>',
      to: email,
      subject: langConfig.confirmationSubject,
      html: getConfirmationEmailHTML({ name, email, company, message }, lang),
    });

    return res.status(200).json({
      success: true,
      message: langConfig.received,
      redirect: `/danke.html?lang=${lang}`,
    });
  } catch (error) {
    console.error('Contact form error:', error.message, error.stack);
    return res.status(500).json({
      error: 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.',
      debug: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
};
