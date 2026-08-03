# Business Continuity Management (BCM) — Notfallkonzept

**Stand: Mai 2026**  
**Klassifikation:** INTERN

---

## 1. Geltungsbereich

Dieses Notfallkonzept gilt für den Betrieb der Plattform Miau Finance. Es definiert Maßnahmen zur Aufrechterhaltung und Wiederherstellung kritischer Geschäftsprozesse bei Ausfällen.

## 2. Kritische Geschäftsprozesse

| Priorität | Prozess | Max. Ausfallzeit (RTO) | Max. Datenverlust (RPO) |
|-----------|---------|----------------------|------------------------|
| **1** | Nutzerauthentifizierung (Login) | 1 Stunde | 0 (kein Verlust) |
| **2** | API-Bereitstellung (Marktdaten) | 4 Stunden | 1 Stunde |
| **3** | Abrechnung / Billing | 24 Stunden | 24 Stunden |
| **4** | Bildungsplattform | 24 Stunden | 24 Stunden |
| **5** | Marketing-Seite | 48 Stunden | 48 Stunden |

## 3. Notfallszenarien

### SZ-1: Komplettausfall (Docker-Host)

| Aspekt | Beschreibung |
|--------|--------------|
| **Auslöser** | Hardware-Fehler, Stromausfall, OS-Crash |
| **Symptom** | Alle Dienste nicht erreichbar |
| **Sofortmaßnahme** | Host neustarten, Docker-Startup prüfen |
| **Eskalation** | Incident-Commander informieren |
| **Wiederherstellung** | `docker compose up -d` auf Produktions-Host |
| **RTO** | 1 Stunde |
| **Backup-Strategie** | Tägliches PostgreSQL-Dump auf separatem Storage |

### SZ-2: Datenbank-Ausfall

| Aspekt | Beschreibung |
|--------|--------------|
| **Auslöser** | PostgreSQL-Crash, Datenkorruption, Plattenfehler |
| **Symptom** | Backend antwortet mit 500er-Fehlern |
| **Sofortmaßnahme** | PostgreSQL-Container neustarten |
| **Eskalation** | Datenbank-Logs prüfen (`docker logs postgres`) |
| **Wiederherstellung** | Backup einspielen: `psql -U miau miau < backup.sql` |
| **RTO** | 2 Stunden |
| **RPO** | 24 Stunden (tägliches Backup) |

### SZ-3: Redis-Ausfall

| Aspekt | Beschreibung |
|--------|--------------|
| **Auslöser** | Redis-Crash, Speicherüberlauf |
| **Symptom** | Rate-Limiting deaktiviert, erhöhte API-Last |
| **Sofortmaßnahme** | Redis-Container neustarten |
| **Wiederherstellung** | Automatisch (Redis ist zustandslos) |
| **RTO** | 5 Minuten |
| **RPO** | 0 (keine persistenten Daten) |

### SZ-4: DDoS-Angriff

| Aspekt | Beschreibung |
|--------|--------------|
| **Auslöser** | Koordinierte Überlastung der API |
| **Symptom** | Rate-Limiting greift, API-Latenz steigt |
| **Sofortmaßnahme** | IP-Sperre aggressiver Quellen |
| **Eskalation** | Hosting-Provider DDoS-Schutz aktivieren |
| **Wiederherstellung** | Automatisch nach Angriffsende |
| **RTO** | Während des Angriffs — abhängig von Angriffsstärke |

### SZ-5: Datenpanne / Sicherheitsvorfall

| Aspekt | Beschreibung |
|--------|--------------|
| **Auslöser** | Unbefugter Zugriff auf Datenbank |
| **Symptom** | Auffällige API-Muster, unbekannte IPs |
| **Sofortmaßnahme** | Zugangsdaten rotieren, System isolieren |
| **Eskalation** | Incident-Response-Team aktivieren |
| **Wiederherstellung** | Siehe incident_response.md |
| **Meldepflicht** | 72h an Aufsichtsbehörde (Art. 33 DSGVO) |

### SZ-6: Ausfall externer Daten-APIs

| Aspekt | Beschreibung |
|--------|--------------|
| **Auslöser** | Ausfall bei Yahoo, FRED, Alpha Vantage etc. |
| **Symptom** | Marktdaten nicht verfügbar |
| **Sofortmaßnahme** | Automatisches Failover auf Backup-Provider |
| **Wiederherstellung** | Nach Wiederherstellung des Primärproviders |
| **RTO** | 1 Minute (automatisch) |

## 4. Notfallorganisation

| Rolle | Name | Erreichbarkeit |
|-------|------|----------------|
| **BCM-Verantwortlicher** | Jevgeni Ziebart | [Telefon/E-Mail] |
| **Incident-Commander** | Jevgeni Ziebart | [Telefon/E-Mail] |
| **Technischer Betrieb** | Jevgeni Ziebart | [Telefon/E-Mail] |
| **Kommunikation** | Jevgeni Ziebart | [E-Mail] |

## 5. Kommunikation im Notfall

| Zielgruppe | Kanal | Frist |
|------------|-------|-------|
| Internes Team | Slack/Teams #incidents | Sofort |
| Nutzer (SEV-1/2) | E-Mail + Status-Seite | Innerhalb 1 Stunde |
| Aufsichtsbehörde | Formular | 72h (DSGVO) |

## 6. Backup- und Recovery-Plan

| Daten | Backup-Rhythmus | Aufbewahrung | Recovery-Test |
|-------|----------------|--------------|---------------|
| PostgreSQL (Dump) | Täglich 03:00 UTC | 30 Tage (Rolling) | Quartalsweise |
| PostgreSQL (WAL) | Kontinuierlich | 7 Tage | — |
| Konfiguration (.env) | Bei Änderung | Git (verschlüsselt) | — |
| Stripe-Daten | Stripe-seitig | Stripe-seitig | — |

## 7. Wiederherstellungs-Tests

| Test | Rhythmus | Typ |
|------|----------|-----|
| Backup-Restore | Quartalsweise | Technisch |
| Docker-Neustart | Halbjährlich | Technisch |
| Notfallübung | Jährlich | Organisatorisch |
| Kommunikationstest | Jährlich | Organisatorisch |

## 8. Dokumentation

Jeder Notfall wird dokumentiert:
1. **Incident-Report** (Vorlage siehe incident_response.md)
2. **Eintrag ins Fehlerprotokoll** (BARK / Incident-Tracking)
3. **Lessons Learned** innerhalb 1 Woche nach Incident

---

**Nächste Überprüfung:** Mai 2027
