# Verzeichnis von Verarbeitungstätigkeiten (Art. 30 DSGVO)

**Stand: Mai 2026**  
**Verantwortlicher:** Jevgeni Ziebart

---

## VVT-001: Nutzerkontenverwaltung

| Feld | Wert |
|------|------|
| **Zweckbestimmung** | Registrierung, Authentifizierung und Verwaltung von Nutzerkonten |
| **Verantwortlicher** | Plattformbetreiber |
| **Kategorien betroffener Personen** | Registrierte Nutzer der Plattform |
| **Kategorien personenbezogener Daten** | Benutzername, E-Mail-Adresse, Passwort-Hash, Rolle, Erstellungs-/Änderungsdatum, Team-Mitgliedschaften, Workspace-Zugehörigkeiten |
| **Empfänger** | PostgreSQL-Datenbank (selbst gehostet) |
| **Drittlandtransfer** | Keiner |
| **Speicherfrist** | Bis zur Account-Löschung; Buchhaltungsdaten 10 Jahre (§ 147 AO) |
| **Technisch-organisatorische Maßnahmen** | TLS 1.3, bcrypt-Passwort-Hashing, JWT-Authentifizierung, rollenbasierte Zugriffskontrolle |
| **Rechtsgrundlage** | Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung), Art. 6 Abs. 1 lit. c DSGVO (rechtliche Verpflichtung) |

---

## VVT-002: Zahlungsabwicklung (Abo-Verwaltung)

| Feld | Wert |
|------|------|
| **Zweckbestimmung** | Abrechnung kostenpflichtiger Abonnements, Rechnungsstellung |
| **Verantwortlicher** | Plattformbetreiber |
| **Kategorien betroffener Personen** | Nutzer mit kostenpflichtigem Abo (Pro, Tiny Catfunds, Enterprise) |
| **Kategorien personenbezogener Daten** | Stripe-Customer-ID, Stripe-Subscription-ID, Abo-Tier, Anzahl Sitze, Rechnungsbeträge, Transaktionsdaten |
| **Empfänger** | Stripe Inc. (Auftragsverarbeiter), PostgreSQL-Datenbank |
| **Drittlandtransfer** | USA — Angemessenheitsbeschluss EU-US Data Privacy Framework |
| **Speicherfrist** | Buchhaltungsdaten: 10 Jahre (§ 147 AO); Übrige Daten: bis Account-Löschung |
| **Technisch-organisatorische Maßnahmen** | Keine Speicherung von Kreditkarten-/IBAN-Daten bei uns; TLS 1.3; PCI-DSS-konformer Zahlungsdienstleister |
| **Rechtsgrundlage** | Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung), Art. 6 Abs. 1 lit. c DSGVO (steuerrechtliche Aufbewahrungspflicht) |

---

## VVT-003: Nutzungsanalyse (Marketing Analytics)

| Feld | Wert |
|------|------|
| **Zweckbestimmung** | Produktverbesserung, Analyse der Nutzungsmuster |
| **Verantwortlicher** | Plattformbetreiber |
| **Kategorien betroffener Personen** | Alle Besucher der Plattform (auch nicht registrierte) |
| **Kategorien personenbezogener Daten** | Pseudonyme Session-ID, aufgerufene URL/Route, User-Agent, Referrer, Zeitstempel |
| **Empfänger** | PostgreSQL-Datenbank |
| **Drittlandtransfer** | Keiner |
| **Speicherfrist** | 90 Tage, danach automatische Löschung |
| **Technisch-organisatorische Maßnahmen** | Keine IP-Speicherung, keine personenidentifizierbaren Daten, Pseudonymisierung |
| **Rechtsgrundlage** | Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an Produktverbesserung) |
| **Widerspruchsrecht** | Art. 21 DSGVO — jederzeit möglich per E-Mail |

---

## VVT-004: API-Nutzungsprotokollierung

| Feld | Wert |
|------|------|
| **Zweckbestimmung** | Rate-Limiting, Abrechnung, Sicherheit und Missbrauchserkennung |
| **Verantwortlicher** | Plattformbetreiber |
| **Kategorien betroffener Personen** | Authentifizierte API-Nutzer |
| **Kategorien personenbezogener Daten** | User-ID, API-Endpunkt, HTTP-Statuscode, Rate-Limit-Verbrauch, Zeitstempel |
| **Empfänger** | Redis (In-Memory-Cache), PostgreSQL |
| **Drittlandtransfer** | Keiner |
| **Speicherfrist** | 30 Tage (Redis), 30 Tage (PostgreSQL), dann Anonymisierung |
| **Technisch-organisatorische Maßnahmen** | Rate-Limiting, Token-basierte Authentifizierung |
| **Rechtsgrundlage** | Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung), Art. 6 Abs. 1 lit. f DSGVO (Sicherheit) |

---

## VVT-005: Bark-System (Feature Requests)

| Feld | Wert |
|------|------|
| **Zweckbestimmung** | Verwaltung von Nutzer-Feature-Requests |
| **Verantwortlicher** | Plattformbetreiber |
| **Kategorien betroffener Personen** | Registrierte Nutzer |
| **Kategorien personenbezogener Daten** | User-ID, Bark-Titel, Bark-Beschreibung, Status, Bark-Jahr |
| **Empfänger** | PostgreSQL-Datenbank |
| **Drittlandtransfer** | Keiner |
| **Speicherfrist** | 3 Jahre nach Einreichung, dann Löschung |
| **Technisch-organisatorische Maßnahmen** | Keine öffentliche Verknüpfung von Barks mit Nutzeridentität |
| **Rechtsgrundlage** | Art. 6 Abs. 1 lit. b DSGVO (vertragsbegleitende Funktion) |

---

## VVT-006: MiauBook (Social Feed)

| Feld | Wert |
|------|------|
| **Zweckbestimmung** | Ermöglichung von nutzergenerierten Inhalten und sozialer Interaktion |
| **Verantwortlicher** | Plattformbetreiber |
| **Kategorien betroffener Personen** | Registrierte Nutzer |
| **Kategorien personenbezogener Daten** | User-ID, Beitragstext, Veröffentlichungsdatum |
| **Empfänger** | PostgreSQL-Datenbank |
| **Drittlandtransfer** | Keiner |
| **Speicherfrist** | Bis zur Account-Löschung oder manuellen Löschung durch den Nutzer |
| **Technisch-organisatorische Maßnahmen** | Beitragserstellung nur nach Authentifizierung |
| **Rechtsgrundlage** | Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung) |

---

## VVT-007: On-Premise-Lizenzverwaltung

| Feld | Wert |
|------|------|
| **Zweckbestimmung** | Ausstellung und Verwaltung von On-Premise-Lizenzen |
| **Verantwortlicher** | Plattformbetreiber |
| **Kategorien betroffener Personen** | Enterprise-Kunden |
| **Kategorien personenbezogener Daten** | Kundenname, Lizenzschlüssel, Aktivierungsdatum |
| **Empfänger** | PostgreSQL-Datenbank |
| **Drittlandtransfer** | Keiner |
| **Speicherfrist** | 10 Jahre nach Vertragsende |
| **Rechtsgrundlage** | Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung) |

---

## VVT-008: Hosting und Infrastruktur

| Feld | Wert |
|------|------|
| **Zweckbestimmung** | Bereitstellung der Server-Infrastruktur, Ausfallsicherheit |
| **Verantwortlicher** | Plattformbetreiber (Auftragsverarbeiter: Hosting-Provider) |
| **Kategorien betroffener Personen** | Alle Nutzer |
| **Kategorien personenbezogener Daten** | Sämtliche vorgenannte Daten (je nach Nutzung) |
| **Empfänger** | Hosting-Provider, PostgreSQL, Redis, Docker-Container |
| **Drittlandtransfer** | Hosting innerhalb der EU / des EWR |
| **Speicherfrist** | Siehe jeweilige VVT |
| **Technisch-organisatorische Maßnahmen** | Verschlüsselung, Firewalls, regelmäßige Backups |
| **Rechtsgrundlage** | Art. 28 DSGVO (Auftragsverarbeitungsvertrag) |

---

## Kontakt Datenschutz

**E-Mail:** privacy@miau.finance  
**Stand:** Mai 2026
