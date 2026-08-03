# Compliance Manual — Miau Finance

**Stand: Mai 2026**  
**Klassifikation:** VERTRAULICH

---

## 1. Einleitung

Dieses Compliance-Manual definiert die Grundsätze, Prozesse und Verantwortlichkeiten zur Sicherstellung der Einhaltung gesetzlicher und regulatorischer Anforderungen auf der Plattform Miau Finance.

## 2. Compliance-Grundsätze

1. **Legalität** — Alle Geschäftsprozesse entsprechen geltendem Recht
2. **Integrität** — Geschäfte werden ehrlich und fair geführt
3. **Transparenz** — Kunden erhalten klare, verständliche Informationen
4. **Vertraulichkeit** — Kundendaten werden streng geschützt
5. **Interessenwahrung** — Kundeninteressen haben Vorrang vor eigenen

## 3. Anwendbare Rechtsvorschriften

| Rechtsgebiet | Vorschrift | Relevanz |
|-------------|------------|----------|
| Datenschutz | DSGVO, BDSG, TTDSG | Datenverarbeitung, Cookies |
| Kapitalmarktrecht | KWG, WpHG, WpIG | (Sofern lizenzierte Tätigkeit) |
| Geldwäsche | GwG | (Sofern lizenzierte Tätigkeit) |
| E-Commerce | TMG, BGB § 312d ff. | AGB, Impressum, Widerruf |
| IT-Sicherheit | BAIT, BSI-Gesetz | IT-Sicherheitsmaßnahmen |
| Urheberrecht | UrhG | Code, Content, Designs |

## 4. Organisatorische Compliance-Struktur

### 4.1 Compliance-Verantwortlicher

| Aufgabe | Verantwortlich | Stellvertretung |
|---------|---------------|-----------------|
| Überwachung der Compliance | Jevgeni Ziebart | Jevgeni Ziebart |
| Meldung an Geschäftsführung | Jevgeni Ziebart | Jevgeni Ziebart |
| Schulungen | Jevgeni Ziebart | Jevgeni Ziebart |
| Dokumentation | Jevgeni Ziebart | Jevgeni Ziebart |

### 4.2 Berichtswege

```
Compliance-Verantwortlicher
    ↓
Geschäftsführung        ← vierteljährlicher Compliance-Bericht
    ↓
Externer Rechtsbeistand  ← bei Bedarf
    ↓
Aufsichtsbehörde         ← bei meldepflichtigen Vorfällen
```

### 4.3 Jährlicher Compliance-Kalender

| Monat | Aufgabe |
|-------|---------|
| Januar | Compliance-Bericht Vorjahr |
| Februar | Datenschutz-Folgenabschätzung (Überprüfung) |
| März | Risikoanalyse (Aktualisierung) |
| April | Mitarbeiter-Schulung Datenschutz |
| Mai | ISMS-Überprüfung |
| Juni | Internes Audit |
| Juli | Vertrags-Überprüfung (AVV, Drittanbieter) |
| August | Schwachstellenanalyse (CVE-Scans) |
| September | Penetrationstest (extern) |
| Oktober | Notfallübung |
| November | Compliance-Bericht laufendes Jahr |
| Dezember | Planung Folgejahr |

## 5. Internes Kontrollsystem (IKS)

### 5.1 Präventive Kontrollen

| Kontrolle | Beschreibung | Rhythmus | Verantwortlich |
|-----------|--------------|----------|---------------|
| **4-Augen-Prinzip** | Keine Admin-Operation ohne Zweiten | Bei jeder Admin-Aktion | Admin-Team |
| **Code-Review** | Kein Merge ohne Review | Jeder Pull-Request | Entwicklung |
| **Berechtigungs-Review** | Prüfung aller Admin-Rechte | Monatlich | Betrieb |
| **Passwort-Policy** | Mindestanforderungen, Rotation | Laufend | System |
| **Log-Monitoring** | Auffällige Muster in API-Logs | Täglich | Betrieb |

### 5.2 Detective Kontrollen

| Kontrolle | Beschreibung | Schwelle | Maßnahme |
|-----------|--------------|----------|----------|
| **Rate-Limiting-Alarm** | Überschreitung von 80% des Limits | Automatisch | Prüfung der Quelle |
| **Failed-Login-Alarm** | >5 fehlgeschlagene Logins in 1 Min | Automatisch | Temporäre IP-Sperre |
| **Fehlerraten-Alarm** | API-Fehlerrate >5% | Automatisch | Incident-Eröffnung |
| **Datenbank-Alarm** | Replikationsverzögerung > 10s | Automatisch | Prüfung DB-Health |

### 5.3 Corrective Kontrollen

| Kontrolle | Beschreibung | Ziel |
|-----------|--------------|------|
| **Incident-Response** | Definierte Prozesse (siehe incident_response.md) | Minimierung Schaden |
| **Backup-Restore** | Wiederherstellungsprozess | Minimierung Ausfallzeit |
| **Patch-Management** | Schnelle Behebung von Sicherheitslücken | Minimierung Angriffsfläche |

## 6. Kundenschutz

### 6.1 Beschwerdemanagement

| Schritt | Beschreibung | Frist |
|---------|--------------|-------|
| **1. Eingang** | Erfassung im Beschwerderegister | 1 Werktag |
| **2. Prüfung** | Sachverhaltsklärung | 5 Werktage |
| **3. Stellungnahme** | Antwort an Kunden | 10 Werktage |
| **4. Lösung** | Fehlerbehebung oder Kompensation | 30 Werktage |
| **5. Abschluss** | Dokumentation, ggf. Prozessverbesserung | 5 Werktage |

**Beschwerderegister:** Wird geführt unter docs/compliance/complaints_register.md  
**Kontakt:** complaints@miau.finance

### 6.2 Interessenkonflikte

Mitarbeiter und Verantwortliche sind verpflichtet:
1. Eigene finanzielle Interessen an der Plattform offenlegen
2. Keine Insiderinformationen für Eigengeschäfte nutzen
3. Keine Geschenke oder Zuwendungen von Nutzern anzunehmen
4. Bei Interessenkonflikten die Entscheidung an Vorgesetzten zu delegieren

### 6.3 Mitarbeiter-Finanzgeschäfte

Mitarbeiter mit Zugriff auf nicht-öffentliche Marktdaten oder Kundenportfolios:
- Dürfen keine Positionen in Instrumenten halten, die von internen Analysen betroffen sind
- Müssen Eigengeschäfte offenlegen (falls zutreffend)
- Unterliegen einer Haltefrist von 24h nach Veröffentlichung von Analysen

## 7. Outsourcing-Management

| Auslagerung | Dienstleister | Kritikalität | AVV |
|-------------|---------------|--------------|-----|
| Zahlungsabwicklung | Stripe | Hoch | Ja |
| Server-Hosting | Hetzner Online GmbH | Hoch | Ja |
| E-Mail-Versand | [Anbieter] | Niedrig | Nein |

Grundsatz: Kritische Auslagerungen bedürfen einer schriftlichen Vereinbarung (AVV) mit Regelungen zu:
- Datenschutz und Datensicherheit
- Weisungsbefugnissen
- Kontrollrechten (Audit)
- Kündigungsfristen und Datenrückgabe
- Verbot von Unter-Auslagerungen ohne Zustimmung

## 8. Aufbewahrungsfristen

| Dokument | Frist | Rechtsgrundlage |
|----------|-------|-----------------|
| Geschäftsunterlagen (Rechnungen, Verträge) | 10 Jahre | § 147 AO |
| Personaldaten | 3 Jahre nach Austritt | § 26 BDSG |
| Log-Daten (API, System) | 30 Tage | DSGVO-Datenminimierung |
| Nutzungsanalysen | 90 Tage | Eigene Festlegung |
| Account-Daten | Bis zur Löschung | DSGVO Art. 17 |

## 9. Schulungen

| Thema | Rhythmus | Zielgruppe |
|-------|----------|------------|
| Datenschutz-Grundlagen | Jährlich | Alle Mitarbeiter |
| IT-Sicherheit | Jährlich | Alle Mitarbeiter |
| Phishing-Sensibilisierung | Halbjährlich | Alle Mitarbeiter |
| Compliance für Entwickler | Bei Einstellung + jährlich | Entwickler |
| Incident-Response | Bei Einstellung + jährlich | Betrieb |

## 10. Sanktionen

Verstöße gegen Compliance-Richtlinien werden dokumentiert und je nach Schwere geahndet:
1. **Leichter Verstoß** — Schriftliche Ermahnung
2. **Mittlerer Verstoß** — Abmahnung, ggf. Entzug von Berechtigungen
3. **Schwerer Verstoß** — Kündigung, Strafanzeige

---

**Freigegeben:** Jevgeni Ziebart, [Datum]  
**Nächste Überprüfung:** Mai 2027
