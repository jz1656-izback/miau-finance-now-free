# Cookie-Richtlinie — Miau Finance

**Stand: Mai 2026**

---

## 1. Einleitung

Diese Cookie-Richtlinie informiert Sie darüber, welche Speichermechanismen die Plattform Miau Finance verwendet und welche Zwecke damit verfolgt werden.

## 2. Was sind Cookies?

Cookies sind kleine Textdateien, die auf Ihrem Endgerät gespeichert werden. Im Gegensatz zu klassischen Cookies verwendet Miau Finance **ausschließlich Local Storage** (eine moderne API des Browsers) — es werden keine klassischen HTTP-Cookies gesetzt.

## 3. Verwendete Speichermechanismen

### 3.1 Local Storage (notwendig)

| Schlüssel | Inhalt | Zweck | Speicherdauer |
|-----------|--------|-------|---------------|
| `miau_token` | JWT (JSON Web Token) | Authentifizierung — speichert Ihren Sitzungstoken nach dem Login | Bis zum Logout oder Token-Ablauf (24h) |
| `miau_refresh` | Refresh Token | Erneuerung des JWT bei Ablauf | Bis zum Logout |

**Rechtsgrundlage:** § 25 Abs. 2 Nr. 2 TTDSG (unbedingt erforderlich)

### 3.2 Server-seitige Sitzungen

Miau Finance verwendet serverseitige Sitzungen zur Analyse der Nutzungsmuster. Diese werden nicht auf Ihrem Endgerät, sondern auf unseren Servern gespeichert.

| Daten | Zweck | Speicherdauer |
|-------|-------|---------------|
| Pseudonyme Session-ID | Nutzungsanalyse | 24 Stunden |
| Aufgerufene Routen | Produktverbesserung | 90 Tage (anonymisiert) |

### 3.3 Drittanbieter

#### Stripe (Zahlungsabwicklung)

Bei Zahlungsvorgängen können Cookies von Stripe gesetzt werden. Stripe benötigt diese Cookies für die Betrugsprävention und zur Authentifizierung. Wir haben keinen Zugriff auf diese Cookies.

- **Anbieter:** Stripe Inc., 510 Townsend Street, San Francisco, CA 94103, USA
- **Cookie-Richtlinie:** https://stripe.com/de/privacy
- **Rechtsgrundlage:** Vertragserfüllung (§ 25 Abs. 2 Nr. 2 TTDSG)

## 4. Keine Tracking-Cookies

Miau Finance verwendet **keine**:
- Tracking-Cookies
- Third-Party-Cookies
- Marketing-Cookies
- Social-Media-Cookies
- Werbe-Cookies
- Cross-Site-Tracking

## 5. Verwaltung Ihres Local Storage

Sie können Local-Storage-Daten jederzeit über die Entwicklerwerkzeuge Ihres Browsers löschen:

| Browser | Anleitung |
|---------|-----------|
| Chrome | F12 → Application → Local Storage → Rechtsklick → Löschen |
| Firefox | F12 → Storage → Local Storage → Rechtsklick → Löschen |
| Safari | Einstellungen → Erweitert → Webentwicklung → Local Storage |
| Edge | F12 → Speicher → Local Storage → Rechtsklick → Löschen |

Alternativ führt eine Abmeldung (Logout) automatisch zur Löschung aller lokalen Speicherdaten.

## 6. Rechtsgrundlage

Die Verwendung von Local Storage für die Authentifizierung ist **unbedingt erforderlich** für den Betrieb der Plattform (§ 25 Abs. 2 Nr. 2 TTDSG). Eine Einwilligung ist daher nicht erforderlich.

---

**Kontakt bei Fragen:** privacy@miau.finance
