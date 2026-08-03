# Data Protection Impact Assessment (DPIA) — Miau Finance

**Stand: Mai 2026**  
**Durchgeführt von:** Jevgeni Ziebart

---

## 1. Einleitung

Diese Datenschutz-Folgenabschätzung gemäß Art. 35 DSGVO bewertet die Risiken der Datenverarbeitung auf der Plattform Miau Finance und dokumentiert die ergriffenen Maßnahmen zur Risikominimierung.

## 2. Beschreibung der Verarbeitungstätigkeit

### 2.1 Systemübersicht

Miau Finance ist eine webbasierte Finanzterminal- und Bildungsplattform mit folgenden Komponenten:

- **Backend:** FastAPI (Python) — API-Server, Authentifizierung, Datenverarbeitung
- **Frontend:** React/Vite — Terminal, Dashboard, Bildungsplattform
- **Datenbank:** PostgreSQL — Speicherung aller Nutzer- und Anwendungsdaten
- **Cache:** Redis — Rate-Limiting, Session-Management
- **Zahlungen:** Stripe — Abrechnung von Abonnements
- **Infrastruktur:** Docker-Container, selbst gehostet

### 2.2 Datenkategorien

Siehe VVT-001 bis VVT-008 im Verzeichnis der Verarbeitungstätigkeiten.

### 2.3 Betroffene Personen

- Registrierte Nutzer der Plattform (ca. 100)
- Besucher der Marketing-Seite (nicht registriert)
- Enterprise-Kunden (On-Premise)

## 3. Notwendigkeitsprüfung

### 3.1 Zweckbindung

| Verarbeitung | Notwendig für Vertragserfüllung? | Berechtigtes Interesse? |
|-------------|--------------------------------|------------------------|
| Account-Erstellung | Ja (Authentifizierung) | — |
| Zahlungsabwicklung | Ja (Abo-Bezahlung) | — |
| Nutzungsanalyse | Nein | Ja (Produktverbesserung) |
| API-Protokollierung | Ja (Rate-Limiting) | Ja (Sicherheit) |

### 3.2 Datenminimierung

Es werden nur die für den jeweiligen Zweck erforderlichen Daten erhoben:
- Keine IP-Speicherung in der Nutzungsanalyse
- Keine Zahlungsdaten bei uns (nur bei Stripe)
- Keine Cookies (nur Local Storage)
- Keine Standortdaten
- Keine biometrischen Daten
- Keine besonderen Kategorien (Art. 9 DSGVO)

## 4. Risikobewertung

### 4.1 Risikomatrix

| Risiko | Eintrittswahrscheinlichkeit | Schwere | Risikostufe | Maßnahme |
|--------|---------------------------|---------|-------------|----------|
| **Datenleak durch unbefugten Zugriff** | Niedrig (2/5) | Hoch (4/5) | Mittel | TLS, Verschlüsselung, Authentifizierung, Firewall |
| **Passwort-Diebstahl** | Niedrig (2/5) | Hoch (4/5) | Mittel | bcrypt-Hashing, Rate-Limiting bei Login |
| **Verlust von Buchhaltungsdaten** | Niedrig (1/5) | Mittel (3/5) | Niedrig | Tägliche Backups, 10-jährige Aufbewahrung |
| **Missbrauch durch API-Scraping** | Mittel (3/5) | Niedrig (2/5) | Niedrig | Rate-Limiting, Token-basierte Auth |
| **Datenpanne durch Stripe** | Sehr niedrig (1/5) | Hoch (4/5) | Niedrig | Stripe ist PCI-DSS Level 1 zertifiziert |
| **Phishing / Social Engineering** | Mittel (3/5) | Mittel (3/5) | Mittel | Keine Speicherung von Zahlungsdaten, 2FA-fähig |

### 4.2 Schutzbedarfsfeststellung

| Schutzziel | Schutzbedarf | Begründung |
|------------|-------------|------------|
| **Vertraulichkeit** | Hoch | Zugangsdaten zu Finanzplattform |
| **Integrität** | Hoch | Marktdaten und Portfoliodaten müssen korrekt sein |
| **Verfügbarkeit** | Mittel | Keine Echtzeit-Handelspflicht |
| **Belastbarkeit** | Mittel | Keine systemrelevanten Finanzdienstleistungen |

## 5. Technisch-organisatorische Maßnahmen (TOMs)

### 5.1 Vertraulichkeit

| Maßnahme | Beschreibung |
|----------|-------------|
| **Verschlüsselung in Transit** | TLS 1.3 für alle HTTP-Verbindungen |
| **Verschlüsselung at Rest** | PostgreSQL-Datenbankverschlüsselung |
| **Passwort-Hashing** | bcrypt (Salt, Work-Factor) |
| **Authentifizierung** | JWT (HS256), Token-Ablauf nach 24h |
| **Zugriffskontrolle** | Rollenbasiert (admin/user/readonly) |
| **CORS-Whitelist** | Nur freigegebene Origins |
| **Input-Validierung** | Pydantic-Schemata, Sanitization |

### 5.2 Integrität

| Maßnahme | Beschreibung |
|----------|-------------|
| **CSRF-Schutz** | CSRF-Middleware für nicht-GET-Anfragen |
| **Rate-Limiting** | Redis-gestützt: 100 req/min/IP, 1000 req/hr/User |
| **Audit-Log** | Protokollierung von API-Zugriffen |
| **Versionskontrolle** | Git, alle Änderungen nachvollziehbar |

### 5.3 Verfügbarkeit und Belastbarkeit

| Maßnahme | Beschreibung |
|----------|-------------|
| **Docker-Orchestrierung** | Automatische Neustarts bei Absturz |
| **Datenbank-Backups** | Täglich (konsistent) |
| **Monitoring** | Prometheus + Grafana |
| **Ressourcenlimits** | Container-Limits, HPA in K8s |
| **Incident Response** | Definierter Prozess (siehe incident_response.md) |

### 5.4 Verfahren zur regelmäßigen Überprüfung

| Maßnahme | Rhythmus | Verantwortlich |
|----------|----------|----------------|
| **Log-Review** | Wöchentlich | Betrieb |
| **Penetrationstest** | Jährlich | Externer Dienstleister |
| **Notfallübung** | Jährlich | Betrieb |
| **Datenschutz-Folgenabschätzung** | Bei wesentlichen Änderungen | Datenschutzbeauftragter |

## 6. Risikobewertung nach Maßnahmenumsetzung

| Risiko | Risikostufe vor Maßnahmen | Risikostufe nach Maßnahmen |
|--------|--------------------------|---------------------------|
| Datenleak | Hoch | **Niedrig** |
| Passwort-Diebstahl | Hoch | **Niedrig** |
| Datenverlust | Mittel | **Sehr niedrig** |
| API-Missbrauch | Mittel | **Niedrig** |
| Stripe-Datenpanne | Mittel | **Sehr niedrig** |
| Phishing | Mittel | **Niedrig** |

## 7. Fazit

Nach Umsetzung der beschriebenen technisch-organisatorischen Maßnahmen verbleiben keine als "hoch" eingestuften Restrisiken. Eine Vorab-Konsultation der Aufsichtsbehörde gemäß Art. 36 DSGVO ist nicht erforderlich.

**Risikobewertung:** 🟢 **Akzeptabel**  
**Nächste Überprüfung:** Mai 2027 oder bei wesentlichen Änderungen der Verarbeitungstätigkeit.

---

**Durchgeführt von:** Jevgeni Ziebart  
**Datum:** Mai 2026  
**Unterschrift:** _________________
