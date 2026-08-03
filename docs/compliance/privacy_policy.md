# Datenschutzerklärung — Miau Finance

**Stand: Mai 2026**

---

## 1. Verantwortlicher

**Betreiber:**  
Jevgeni Ziebart  
Zypressenweg 21  
53340 Meckenheim  
Deutschland  
**E-Mail:** privacy@miau.finance

## 2. Datenschutzbeauftragter

Der Datenschutzbeauftragte ist erreichbar unter:  
**E-Mail:** privacy@miau.finance  
**Post:** siehe Verantwortlicher, z. Hd. Datenschutzbeauftragter

## 3. Überblick der Verarbeitungstätigkeiten

Miau Finance betreibt eine webbasierte Finanzterminal- und Bildungsplattform mit folgenden Komponenten:

- **Terminal** — interaktives Finanzterminal mit Marktdaten, Analysen und Portfolio-Tracking (Port 5173)
- **Education Platform** — Online-Kurse und Zertifizierungen (Port 5174)
- **Ecosystem Site** — Marketing- und Produktinformationsseite (Port 5175)

## 4. Verarbeitete Datenkategorien und Zwecke

### 4.1 Account-Daten (Pflichtangaben)

| Daten | Zweck | Rechtsgrundlage | Speicherdauer |
|-------|-------|-----------------|---------------|
| Benutzername | Identifikation, Login | Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung) | Bis zur Löschung des Accounts |
| E-Mail-Adresse | Kommunikation, Password-Reset | Art. 6 Abs. 1 lit. b DSGVO | Bis zur Löschung des Accounts |
| Passwort-Hash (bcrypt) | Authentifizierung | Art. 6 Abs. 1 lit. c DSGVO (Sicherheit) | Bis zur Löschung des Accounts |
| Rolle (admin/user/readonly) | Zugriffssteuerung | Art. 6 Abs. 1 lit. b DSGVO | Bis zur Löschung des Accounts |

### 4.2 Zahlungsdaten (bei kostenpflichtigen Abos)

Die Zahlungsabwicklung erfolgt ausschließlich über **Stripe** (Stripe Inc., USA). Wir speichern selbst keine Zahlungsdaten (Kreditkarten, IBAN etc.), sondern lediglich:

- Stripe-Customer-ID
- Stripe-Subscription-ID
- Gebuchtes Abo-Tier (Pro, Tiny Catfunds, Enterprise)
- Anzahl gebuchter Plätze (Seats)

**Rechtsgrundlage:** Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung)  
**Speicherdauer:** Bis zur Löschung des Accounts, danach Aufbewahrung gemäß § 147 AO (10 Jahre) für buchhalterische Zwecke.  
**Stripe-Datenschutz:** https://stripe.com/de/privacy  
**Drittlandtransfer:** Angemessenheitsbeschluss EU-US Data Privacy Framework

### 4.3 Nutzungsdaten & Analysen

Zur Verbesserung der Plattform erfassen wir anonymisierte Nutzungsdaten:

| Daten | Zweck | Rechtsgrundlage | Speicherdauer |
|-------|-------|-----------------|---------------|
| Seitenaufrufe (PageView) | Produktverbesserung | Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse) | 90 Tage |
| Besuchersitzungen (VisitorSession) | Produktverbesserung | Art. 6 Abs. 1 lit. f DSGVO | 90 Tage |
| Conversions (Conversion) | Marketing-Analyse | Art. 6 Abs. 1 lit. f DSGVO | 90 Tage |

Diese Daten umfassen: aufgerufene URL/Route, User-Agent (Browserkennung), Referrer, Pseudonyme Session-ID (keine IP-Speicherung). Eine Identifikation einzelner Personen ist nicht möglich.

**Widerspruchsrecht:** Sie können der Erfassung jederzeit widersprechen (siehe Abschnitt 9).

### 4.4 API-Nutzungsdaten

Jeder API-Zugriff wird für Rate-Limiting und Abrechnungszwecke protokolliert:

- User-ID (authentifizierte Anfragen)
- API-Endpunkt
- Zeitstempel
- HTTP-Statuscode
- Verbrauchte Rate-Limit-Einheiten

**Rechtsgrundlage:** Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung) i. V. m. Art. 6 Abs. 1 lit. c DSGVO (Sicherheit)  
**Speicherdauer:** 30 Tage, danach anonymisiert

### 4.5 Zusätzliche Funktionen

| Feature | Verarbeitete Daten | Rechtsgrundlage |
|---------|-------------------|-----------------|
| Billing / Abos | Siehe 4.2 | Art. 6 Abs. 1 lit. b DSGVO |
| Bark-System (Feature Requests) | Titel, Beschreibung | Art. 6 Abs. 1 lit. b DSGVO |
| Teams & Workspaces | Team-Mitgliedschaften, Rollen | Art. 6 Abs. 1 lit. b DSGVO |
| Portfolio-Tracking | Vom Benutzer eingegebene Positionen | Art. 6 Abs. 1 lit. b DSGVO |
| MiauBook (Social Feed) | Vom Benutzer erstellte Beiträge | Art. 6 Abs. 1 lit. b DSGVO |

## 5. Empfänger der Daten

| Empfänger | Zweck | Rechtsgrundlage |
|-----------|-------|-----------------|
| Stripe Inc., USA | Zahlungsabwicklung | Art. 28 DSGVO (AVV) + EU-US Data Privacy Framework |
| Hosting-Provider (Hetzner / Jevgeni Ziebart) | Server-Infrastruktur | Art. 28 DSGVO (AVV) |
| Redis, PostgreSQL (selbst gehostet) | Datenbank & Caching | Innerhalb der EU / des EWR |

Eine Weitergabe an Dritte zu Werbezwecken erfolgt nicht.

## 6. Speicherdauer und Löschung

| Datenkategorie | Speicherdauer | Löschung |
|----------------|---------------|----------|
| Account-Daten | Bis zur Account-Löschung | Sofort bei Löschung |
| Buchhaltungsdaten (Abrechnungen) | 10 Jahre (§ 147 AO) | Nach Ablauf der Frist |
| Nutzungsanalysen | 90 Tage | Automatisch nach 90 Tagen |
| API-Logs | 30 Tage | Automatisch nach 30 Tagen |

Accounts können jederzeit per E-Mail an privacy@miau.finance oder über die Terminal-Einstellungen gelöscht werden.

## 7. Rechte der betroffenen Person (Ihre Rechte)

Nach der DSGVO stehen Ihnen folgende Rechte zu:

| Recht | Inhalt | Umsetzung |
|-------|--------|-----------|
| **Auskunft (Art. 15)** | Welche Daten wir über Sie verarbeiten | Anfrage an privacy@miau.finance |
| **Berichtigung (Art. 16)** | Unrichtige Daten korrigieren | Account-Einstellungen oder E-Mail |
| **Löschung (Art. 17)** | "Recht auf Vergessenwerden" | Account-Löschung oder E-Mail |
| **Einschränkung (Art. 18)** | Verarbeitung einschränken | E-Mail an Datenschutzbeauftragten |
| **Datenübertragbarkeit (Art. 20)** | Ihre Daten in maschinenlesbarem Format | Anfrage an privacy@miau.finance |
| **Widerspruch (Art. 21)** | Widerspruch gegen Verarbeitung | E-Mail an Datenschutzbeauftragten |
| **Beschwerde (Art. 77)** | Beschwerde bei Aufsichtsbehörde | Zuständig: Landesdatenschutzbeauftragter [Bundesland] oder BaFin |

## 8. Datensicherheit

Wir treffen folgende technische und organisatorische Maßnahmen:

- **Verschlüsselung in Transit:** TLS 1.3 (HTTPS) für alle Verbindungen
- **Verschlüsselung at Rest:** PostgreSQL-Datenbankverschlüsselung
- **Passwort-Hashing:** bcrypt mit Salt
- **Authentifizierung:** JWT (HS256) mit Token-Ablauf
- **Rate-Limiting:** Redis-gestützt (100 req/min/IP, 1000 req/hr/User)
- **Zugangskontrolle:** Rollenbasiert (admin/user/readonly)
- **CORS-Whitelist:** Nur freigegebene Origins
- **Input-Validierung:** Pydantic-Schemata + Sanitization

## 9. Cookies und lokaler Speicher

Miau Finance verwendet ausschließlich **notwendige lokale Speichermechanismen**:

| Mechanismus | Zweck | Typ | Speicherdauer |
|-------------|-------|-----|---------------|
| `miau_token` (localStorage) | JWT-Authentifizierung | Local Storage | Bis Logout / Ablauf |
| Session-IDs (Server) | Session-Tracking | Server-seitig | 24 Stunden |

Es werden **keine Tracking-Cookies, Third-Party-Cookies oder Marketing-Cookies** eingesetzt. Die Nutzungsanalyse erfolgt pseudonym ohne Cookie-Speicherung.

## 10. Automatisierte Entscheidungsfindung

Eine automatisierte Entscheidungsfindung einschließlich Profiling gemäß Art. 22 DSGVO findet nicht statt. Der KI-Assistent (Miau AI Advisor) gibt lediglich Empfehlungen ab; alle Anlageentscheidungen trifft der Nutzer eigenverantwortlich.

## 11. Änderungen dieser Datenschutzerklärung

Wir behalten uns vor, diese Datenschutzerklärung bei Bedarf anzupassen. Die aktuelle Fassung ist stets unter `/docs/compliance/privacy_policy.md` oder auf der Plattform abrufbar. Bei wesentlichen Änderungen werden Nutzer per E-Mail informiert.

---

**Fragen zum Datenschutz?** Kontaktieren Sie uns unter: privacy@miau.finance
