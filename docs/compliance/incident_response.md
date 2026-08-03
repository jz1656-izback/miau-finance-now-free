# Incident Response Plan — Miau Finance

**Stand: Mai 2026**  
**Klassifikation:** INTERN

---

## 1. Zweck

Dieser Plan definiert das Vorgehen bei Sicherheitsvorfällen auf der Plattform Miau Finance. Ziel ist die schnelle Erkennung, Eindämmung, Beseitigung und Dokumentation von Vorfällen sowie die Einhaltung gesetzlicher Meldefristen (72h nach DSGVO Art. 33).

## 2. Incident-Klassifizierung

| Stufe | Bezeichnung | Beispiele | Meldefrist |
|-------|-------------|-----------|------------|
| **🔴 SEV-1** | Kritisch | Datenleak mit PII, RCE, System-Kompromittierung, Ausfall > 4h | 72h (Aufsichtsbehörde + Betroffene) |
| **🟡 SEV-2** | Hoch | API-Key-Leak, DDoS-Angriff, teilweiser Systemausfall | 24h intern |
| **🟢 SEV-3** | Mittel | Fehlerhafte Daten, einzelne Funktionsausfälle | Nächster Werktag |
| **⚪ SEV-4** | Niedrig | Kosmetische Fehler, nicht sicherheitsrelevant | Nächstes Sprint-Planning |

## 3. Incident Response Team

| Rolle | Verantwortung | Stellvertretung |
|-------|---------------|-----------------|
| **Incident Commander** | Gesamtkoordination, Entscheidungen | Betriebsverantwortlicher |
| **Sicherheitsanalyst** | Technische Analyse, Forensik | Entwicklungsverantwortlicher |
| **Kommunikationsverantwortlicher** | Interne/externe Kommunikation, Behörden | Datenschutzbeauftragter |
| **Legal** | Rechtliche Bewertung, Meldepflicht | Externer Rechtsbeistand |

## 4. Incident Response Prozess

### 4.1 Erkennung und Meldung (Discovery)

Jeder Mitarbeiter ist verpflichtet, Sicherheitsvorfälle unverzüglich zu melden.

**Meldewege:**
- **E-Mail:** security@miau.finance (24/7)
- **Intern:** #security-channel (Slack/Teams)
- **Telefon:** 0160/92182557

**Erkennungsquellen:**
- Prometheus-Alarme (Fehlerraten, Latenz)
- BARK-Betriebsalarme (Service-Crashs)
- API-Logs (auffällige Muster)
- Nutzer-Beschwerden
- Externe Meldungen (CVE, Bug Bounty)

### 4.2 Eindämmung (Containment)

| Stufe | Sofortmaßnahme |
|-------|----------------|
| **SEV-1** | System vom Netz trennen, Passwörter rotieren, Logs sichern |
| **SEV-2** | Betroffenen Dienst isolieren, API-Keys rotieren, IP sperren |
| **SEV-3** | Funktion deaktivieren, Fehleranalyse starten |
| **SEV-4** | Ticket anlegen, im nächsten Sprint bearbeiten |

### 4.3 Analyse (Investigation)

1. **Zeitstrahl erstellen** — Wann ist was passiert?
2. **Logs sichern** — PostgreSQL-Logs, API-Logs, Container-Logs
3. **Ursachenanalyse** — Root-Cause-Analyse
4. **Betroffene Daten identifizieren** — Welche Daten, welche Personen?
5. **Schweregrad final bestimmen**

### 4.4 Beseitigung (Eradication)

1. Schwachstelle schließen (Patch, Konfigurationsänderung)
2. Betroffene Systeme säubern (Malware-Scan, Image-Neubau)
3. Zugangsdaten rotieren (Passwörter, API-Keys, JWT-Secret)
4. Backup wiederherstellen (falls erforderlich)

### 4.5 Wiederherstellung (Recovery)

1. System wieder ans Netz nehmen
2. Überwachung intensivieren (24h)
3. Funktionsfähigkeit testen
4. Nutzer informieren (falls erforderlich)

### 4.6 Nachbereitung (Post-Mortem)

1. **Incident-Report erstellen** (Vorlage siehe Abschnitt 7)
2. **Lessons Learned dokumentieren**
3. **Maßnahmen zur Prävention ableiten**
4. **Prozess verbessern**

## 5. Meldepflichten

### 5.1 Datenschutzverletzung (Art. 33 DSGVO)

| Pflicht | Frist | Empfänger |
|---------|-------|-----------|
| Meldung an Aufsichtsbehörde | **72 Stunden** nach Bekanntwerden | Landesdatenschutzbeauftragter |
| Benachrichtigung Betroffener | **Unverzüglich** | Betroffene Personen |
| Dokumentation | Jederzeit nachweisbar | Internes Verzeichnis |

### 5.2 Meldung an BaFin

Bei Vorfällen mit Bezug zu Finanzdienstleistungen (gemäß § 54 KWG / § 30 WpIG):
- Unverzügliche Meldung an BaFin
- Vorlage eines detaillierten Berichts innerhalb von 2 Wochen

## 6. Kommunikationsplan

| Zielgruppe | Kanal | Inhalt | Verantwortlich |
|------------|-------|--------|----------------|
| Internes Team | #security-channel | Technische Details, Aufgaben | Incident Commander |
| Nutzer (allgemein) | E-Mail / Status-Seite | Kurze Zusammenfassung, Entwarnung | Kommunikation |
| Betroffene Nutzer | E-Mail (personalisiert) | Welche Daten, Risiken, Maßnahmen | Kommunikation + Legal |
| Aufsichtsbehörde | Formular + E-Mail | Art. 33-DSGVO-Meldung | Legal |18|
| Presse / Öffentlichkeit | Pressemitteilung (nur SEV-1) | Abgestimmte Stellungnahme | Geschäftsführung |

## 7. Incident-Report-Vorlage

```markdown
# INCIDENT REPORT — [ID]

**Datum:** [Datum]
**Klassifizierung:** [SEV-1/2/3/4]
**Status:** [Open / Containment / Eradication / Recovery / Closed]

## Zusammenfassung
[Kurzbeschreibung des Vorfalls]

## Zeitstrahl
- [Zeit] — Erstmeldung durch [Quelle]
- [Zeit] — Eindämmung eingeleitet
- [Zeit] — Ursache identifiziert
- [Zeit] — Maßnahme umgesetzt
- [Zeit] — Wiederherstellung abgeschlossen
- [Zeit] — Incident geschlossen

## Betroffene Systeme
- [System 1]
- [System 2]

## Betroffene Daten
- [Datenkategorien]
- [Anzahl betroffener Personen]

## Ursache
[Root Cause]

## Maßnahmen
1. [Sofortmaßnahme]
2. [Präventive Maßnahme]

## Lessons Learned
1. [Erkenntnis 1]
2. [Erkenntnis 2]

## Anhänge
- [Log-Auszüge]
- [Screenshots]
- [Korrespondenz]
```

## 8. Übungen und Tests

| Übung | Rhythmus | Beschreibung |
|-------|----------|--------------|
| Tabletop-Exercise | Jährlich | Besprechung fiktiver Incidents |
| Backup-Restore-Test | Quartalsweise | Wiederherstellung aus Backup |
| Penetrationstest | Jährlich | Externer Sicherheitstest |
| Phishing-Simulation | Halbjährlich | Sensibilisierung der Mitarbeiter |

---

**Kontakt Incident Response:** security@miau.finance  
**Nächste Überprüfung:** Mai 2027
