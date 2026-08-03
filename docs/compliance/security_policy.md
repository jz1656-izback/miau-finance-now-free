# Informationssicherheitsrichtlinie (ISMS) — Miau Finance

**Stand: Mai 2026**  
**Klassifikation:** INTERN

---

## 1. Geltungsbereich

Diese Richtlinie gilt für die gesamte Informationsverarbeitung auf der Plattform Miau Finance, einschließlich:

- Backend-Systeme (API-Server, Datenbanken, Caches)
- Frontend-Anwendungen (Terminal, Education Platform, Ecosystem Site)
- Entwicklungs- und Betriebsinfrastruktur (Docker, Kubernetes, CI/CD)
- Drittanbieter-Integrationen (Stripe, externe Daten-APIs)
- Mitarbeiter, Administratoren und Auftragsverarbeiter mit Zugriff auf die Systeme

## 2. Sicherheitsleitlinien

1. **Vertraulichkeit** — Daten sind nur für autorisierte Personen zugänglich
2. **Integrität** — Daten sind vollständig, korrekt und vor unbemerkter Manipulation geschützt
3. **Verfügbarkeit** — Systeme sind im vereinbarten Umfang nutzbar
4. **Authentizität** — Identitäten sind eindeutig und überprüfbar
5. **Revisionssicherheit** — Alle relevanten Vorgänge sind nachvollziehbar dokumentiert

## 3. Organisatorische Sicherheit

### 3.1 Rollen und Verantwortlichkeiten

| Rolle | Verantwortlichkeiten |
|-------|---------------------|
| **Informationssicherheitsbeauftragter** | ISMS-Pflege, Sicherheitsvorfälle, Audits |
| **Betriebsverantwortlicher** | Systemadministration, Patch-Management, Backups |
| **Entwicklungsverantwortlicher** | Secure Coding, Code-Reviews |
| **Datenschutzbeauftragter** | Datenschutz-Folgenabschätzung, Betroffenenanfragen |

### 3.2 Zugriffssteuerung

- Zugriffe erfolgen nach dem **Need-to-know-Prinzip**
- Jeder Benutzer hat eine eindeutige ID
- Rollen: admin, user, readonly
- Berechtigungsänderungen werden dokumentiert
- **Vier-Augen-Prinzip** bei administrativen Änderungen

### 3.3 Mitarbeiter-Sicherheit

- Sensibilisierung für Phishing und Social Engineering
- Verpflichtung auf das Datengeheimnis (§ 53 BDSG)
- Verbot der Weitergabe von Zugangsdaten
- Verpflichtende Meldung von Sicherheitsvorfällen

## 4. Technische Sicherheitsmaßnahmen

### 4.1 Netzwerksicherheit

| Maßnahme | Implementierung |
|----------|----------------|
| Firewall | Container-Isolation, Port-Beschränkung |
| TLS | TLS 1.3 für alle öffentlichen Endpunkte |
| CORS | Whitelist-basiert, nur bekannte Origins |
| API-Schutz | Rate-Limiting (Redis), Token-basiert |
| DDoS-Schutz | Rate-Limiting pro IP |

### 4.2 Authentifizierung und Autorisierung

| Maßnahme | Implementierung |
|----------|----------------|
| Passwort-Hashing | bcrypt (Salt, Work-Factor) |
| Token-basierte Authentifizierung | JWT (HS256), 24h Ablauf |
| Passwort-Anforderungen | Min. 8 Zeichen, Großbuchstabe, Zahl |
| Rate-Limiting Login | 10 Versuche/min/IP |
| Session-Management | Keine Session-Cookies (nur Local Storage) |

### 4.3 Verschlüsselung

| Bereich | Verfahren |
|---------|-----------|
| Transport (HTTP) | TLS 1.3 (HTTPS) |
| Datenbank (at Rest) | PostgreSQL-Transparent-Data-Encryption |
| Passwörter | bcrypt |
| API-Keys (extern) | Nur serverseitig, nie im Frontend |

### 4.4 Entwicklungs-Sicherheit

| Maßnahme | Beschreibung |
|----------|-------------|
| **Input-Validierung** | Pydantic-Schemata vor jeder Verarbeitung |
| **SQL-Injection-Schutz** | SQLAlchemy ORM (kein Raw-SQL) |
| **XSS-Schutz** | CSP-Header, Output-Encoding |
| **CSRF-Schutz** | CSRF-Middleware für nicht-GET-Anfragen |
| **Code-Reviews** | Vor jedem Merge in den Hauptzweig |
| **Abhängigkeits-Scans** | Regelmäßige Prüfung auf bekannte CVEs |

## 5. Betriebssicherheit

### 5.1 Patch-Management

| Komponente | Patch-Rhythmus |
|------------|---------------|
| Betriebssystem | Automatische Sicherheitsupdates |
| Docker-Images | Wöchentlicher Scan + Update |
| Python-Abhängigkeiten | Monatliches `pip audit` |
| Node.js-Abhängigkeiten | Monatliches `npm audit` |
| PostgreSQL | Sicherheitspatches innerhalb von 48h |
| Redis | Sicherheitspatches innerhalb von 1 Woche |

### 5.2 Datensicherung

| Daten | Rhythmus | Aufbewahrung |
|-------|----------|--------------|
| PostgreSQL (vollständig) | Täglich | 30 Tage (Rolling) |
| PostgreSQL (WAL) | Kontinuierlich | 7 Tage |
| Konfigurationsdateien | Bei Änderung | Git-Versionierung |
| Stripe-Daten | Nicht bei uns gespeichert | Stripe-seitig |

### 5.3 Monitoring und Erkennung

| System | Zweck |
|--------|-------|
| Prometheus | Metriken (CPU, RAM, Anfragen, Fehlerraten) |
| Grafana | Dashboards, Alerting |
| API-Log | Audit-Trail aller API-Zugriffe |
| BARK-System | Automatisierte Betriebsalarme |

## 6. Vorfallmanagement

Siehe separates Dokument: `incident_response.md`

## 7. Drittanbieter-Management

| Anbieter | Service | Zertifizierung | AVV vorhanden |
|----------|---------|----------------|---------------|
| Stripe Inc. | Zahlungsabwicklung | PCI-DSS Level 1, SOC 2 | Ja |
| Hosting-Provider | Server-Infrastruktur | ISO 27001 | Ja |
| Externe Daten-APIs | Finanzdaten (Yahoo, FRED etc.) | — | Nein (anonyme Nutzung) |

## 8. Compliance und Audits

- Interne Audits: jährlich
- Penetrationstests: jährlich (extern)
- Datenschutz-Folgenabschätzung: bei wesentlichen Änderungen
- Überprüfung dieser Richtlinie: jährlich

## 9. Sanktionen

Verstöße gegen diese Sicherheitsrichtlinie können je nach Schwere führen zu:
1. Verwarnung
2. Entzug von Zugriffsrechten
3. Kündigung des Arbeits-/Dienstverhältnisses
4. Strafrechtlichen Konsequenzen (§ 202a ff. StGB, § 42 BDSG)

## 10. Inkrafttreten

Diese Richtlinie tritt am 1. Juni 2026 in Kraft.

---

**Freigegeben durch:** Jevgeni Ziebart  
**Nächste Überprüfung:** Mai 2027
