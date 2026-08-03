# IT-Risikobewertung — Miau Finance

**Stand: Mai 2026**  
**Methode:** BSI IT-Grundschutz / ISO 27005

---

## 1. Risikostrategie

Miau Finance verfolgt einen **risikobasierten Ansatz** nach dem BSI-Standard IT-Grundschutz. Risiken werden identifiziert, bewertet und durch geeignete Maßnahmen behandelt.

**Risikoakzeptanzkriterien:**  
- Keine akzeptierten Risiken mit "sehr hoch" oder "hoch" nach Maßnahmenumsetzung  
- Restrisiko muss vom Informationssicherheitsbeauftragten genehmigt werden

## 2. Schutzbedarfsfeststellung

| Geschäftsprozess | Vertraulichkeit | Integrität | Verfügbarkeit |
|-----------------|----------------|------------|---------------|
| Nutzerauthentifizierung | Hoch | Hoch | Mittel |
| Portfolio-Tracking | Mittel | Hoch | Niedrig |
| Abrechnung/Zahlungen | Hoch | Hoch | Mittel |
| Marktdaten-Bereitstellung | Niedrig | Mittel | Mittel |
| Kurs-Plattform | Niedrig | Mittel | Niedrig |

## 3. Asset-Inventar

| Asset | Typ | Standort | Schutzbedarf |
|-------|-----|----------|-------------|
| PostgreSQL-Datenbank | Daten | Docker-Container | Hoch |
| Redis-Cache | Daten | Docker-Container | Niedrig |
| FastAPI Backend | Software | Docker-Container | Mittel |
| React Frontend | Software | Docker/Vite | Niedrig |
| Stripe-Integration | Dienstleistung | Stripe-Cloud | Hoch |
| API-Credentials (31 Anbieter) | Konfiguration | .env-Datei | Hoch |
| JWT-Secret | Konfiguration | .env-Datei | Hoch |
| Docker-Host | Infrastruktur | Server-RZ | Hoch |

## 4. Bedrohungsanalyse

### 4.1 Elementare Bedrohungen (BSI)

| ID | Bedrohung | Betroffene Assets | Eintrittswahrsch. | Schadensausmaß | Risiko |
|----|-----------|-------------------|------------------|----------------|--------|
| G 0.3 | Datenverlust durch Systemausfall | PostgreSQL, Redis | Niedrig | Mittel | Niedrig |
| G 0.5 | Verlust der Vertraulichkeit durch unbefugten Zugriff | PostgreSQL, JWT-Secret | Niedrig | Hoch | Mittel |
| G 0.6 | Datenmanipulation | PostgreSQL | Niedrig | Hoch | Mittel |
| G 0.13 | Personalfehler | Alle | Mittel | Mittel | Mittel |
| G 0.15 | Abhören von Kommunikation | HTTP-Verbindungen | Sehr niedrig | Mittel | Sehr niedrig |
| G 0.18 | Fehlplanung / fehlende Ressourcen | Alle | Mittel | Niedrig | Niedrig |
| G 0.21 | Angriff mit Schadsoftware | Backend, Frontend | Niedrig | Hoch | Mittel |
| G 0.23 | Identitätsdiebstahl | JWT-Token | Niedrig | Hoch | Mittel |
| G 0.30 | Social Engineering | Entwickler, Admins | Mittel | Mittel | Mittel |
| G 0.32 | Missbrauch von Berechtigungen | Admin-Accounts | Niedrig | Hoch | Mittel |
| G 0.37 | Denial of Service | API, Frontend | Mittel | Mittel | Mittel |

### 4.2 Anwendungsspezifische Bedrohungen

| ID | Bedrohung | Betroffene Assets | Eintrittswahrsch. | Schadensausmaß | Risiko |
|----|-----------|-------------------|------------------|----------------|--------|
| A 1 | API-Key-Leak (31 Anbieter in URL-Logs) | .env, Logs | **Hoch** | Hoch | **Hoch** |
| A 2 | Rate-Limiting-Umgehung durch verteilte Angriffe | API | Mittel | Mittel | Mittel |
| A 3 | Stripe-Webhook-Spoofing | Billing | Sehr niedrig | Hoch | Niedrig |
| A 4 | CVE in Python-/Node-Abhängigkeiten | Backend, Frontend | Mittel | Hoch | Mittel |
| A 5 | Ungesicherte .env-Datei in Git-History | Credentials | **Hoch** | **Sehr hoch** | **Hoch** |
| A 6 | Plug-in-Sandbox-Escape (exec()) | Backend | Niedrig | Hoch | Mittel |

## 5. Risikobehandlung

### 5.1 Risikovermeidung

| Maßnahme | Behandelt Bedrohung |
|----------|---------------------|
| .env aus Git-History entfernen, .gitignore ergänzen | A 5 |
| API-Keys in Logs maskieren | A 1 |
| Keine Speicherung von Zahlungsdaten | G 0.5 (Payment) |

### 5.2 Risikominderung

| Maßnahme | Behandelt Bedrohung |
|----------|---------------------|
| bcrypt-Passwort-Hashing | G 0.23 |
| JWT mit 24h-Ablauf | G 0.23, G 0.32 |
| Rate-Limiting (Redis) | G 0.37 |
| CSRF-Middleware | G 0.6 |
| CORS-Whitelist | G 0.15 |
| TLS 1.3 | G 0.15 |
| Tägliche Backups | G 0.3 |
| Input-Validierung (Pydantic) | G 0.6, G 0.21 |
| Stripe-Signatur-Prüfung | A 3 |
| Regelmäßige CVE-Scans | A 4 |

### 5.3 Risikoüberwälzung

| Maßnahme | Behandelt Bedrohung |
|----------|---------------------|
| Stripe für Zahlungen (PCI-DSS) | Zahlungsdaten-Sicherheit |
| Hosting-Provider mit ISO 27001 | Physische Sicherheit |

### 5.4 Risikoakzeptanz

| Restrisiko | Begründung |
|------------|------------|
| Plug-in-Sandbox-Escape (A 6) | Nur Admin-freigegebene Plugins, exec() nicht in Produktion aktiv |
| CVE-Abhängigkeiten (A 4) | Monatlicher Scan, Patches innerhalb von 7 Tagen |

## 6. Risikomatrix (nach Maßnahmen)

```
Sehr hoch │         │         │         │         │
          │         │         │         │         │
Hoch      │  A1 A5  │         │         │         │
          │  → ↓    │         │         │         │
Mittel    │  A2 G13 │ A4 G23  │         │         │
          │  G30    │ G32     │         │         │
Niedrig   │  G3 G18 │         │         │         │
          │  A3     │         │         │         │
S. niedrig│  G15    │         │         │         │
          │         │         │         │         │
          └────────────────────────────────────────
           S.niedr. Niedrig  Mittel    Hoch      S.hoch
                    SCHADENSAUSMASS
```

## 7. Nächste Schritte

| Maßnahme | Fälligkeit | Verantwortlich |
|----------|------------|----------------|
| .env aus Git-History entfernen | Sofort | Betrieb |
| API-Keys in Logging maskieren | Innerhalb 1 Woche | Entwicklung |
| Externen Penetrationstest durchführen | Juni 2026 | Extern |
| CVE-Scan automatisieren | Juni 2026 | Entwicklung |
| Diese Bewertung aktualisieren | Mai 2027 | ISB |

---

**Erstellt von:** Jevgeni Ziebart  
**Freigegeben:** Mai 2026
