# Anti-Money Laundering (AML) Policy — Miau Finance

**Stand: Mai 2026**  
**Klassifikation:** VERTRAULICH

---

## 1. Geltungsbereich

Diese Richtlinie definiert die Grundsätze zur Verhinderung von Geldwäsche und Terrorismusfinanzierung auf der Plattform Miau Finance.

**Hinweis:** Miau Finance ist ein reines Informations- und Bildungsangebot. Es werden keine Finanztransaktionen, Zahlungsdienste oder Wertpapiergeschäfte durchgeführt oder vermittelt. Das GwG (Geldwäschegesetz) ist daher im vollen Umfang nicht anwendbar. Dennoch befolgen wir die Grundsätze des risikobasierten Ansatzes.

## 2. Risikobewertung

### 2.1 Plattform-spezifische Risiken

| Risiko | Eintrittswahrsch. | Begründung | Maßnahme |
|--------|-------------------|------------|----------|
| Missbrauch der API für Marktmanipulation | Niedrig | API ist read-only (keine Order-Übermittlung) | Keine |
| Nutzung der Plattform zur Koordination illegaler Transaktionen | Sehr niedrig | Keine Kommunikationsplattform | Logging von Aktivitäten |
| Identitätsbetrug bei Account-Erstellung | Mittel | E-Mail-basierte Registrierung | E-Mail-Verifikation |
| Zahlungsbetrug (Stripe) | Niedrig | Stripe-Betrugsprüfung (Radar) | Stripe-eigene Mechanismen |

### 2.2 Risikoklassifizierung

Da Miau Finance keine Finanztransaktionen ermöglicht, entfällt eine KYC-Pflicht nach GwG. Dennoch empfehlen wir für Enterprise-Kunden (On-Premise, individuelle Verträge):

- **Niedriges Risiko:** Free- und Pro-Nutzer — keine zusätzliche Prüfung
- **Mittleres Risiko:** Tiny-Catfunds-Nutzer — E-Mail-Verifikation, Zahlung über Stripe
- **Erhöhtes Risiko:** Enterprise-Kunden — individuelle Prüfung, ggf. Know-Your-Customer (KYC)

## 3. KYC-Verfahren (freiwillig, für Enterprise)

Für Enterprise-Kunden mit individuellem Vertrag und On-Premise-Lizenz kann eine freiwillige Identitätsprüfung durchgeführt werden:

| Schritt | Beschreibung |
|---------|--------------|
| 1 | Vorlage eines gültigen Ausweisdokuments (Personalausweis, Reisepass) |
| 2 | Nachweis der Geschäftsadresse (Handelsregisterauszug) |
| 3 | Prüfung auf PEP-Status (politisch exponierte Person) |
| 4 | Dokumentation und Aufbewahrung (5 Jahre nach Vertragsende) |

## 4. Transaktionsmonitoring

Da keine Finanztransaktionen auf der Plattform stattfinden, beschränkt sich das Monitoring auf:

| Überwachung | Zweck |
|-------------|-------|
| **Auffällige Login-Muster** | Erkennung von Account-Übernahmen |
| **Ungewöhnliche API-Nutzung** | Erkennung von Scraping / Missbrauch |
| **Zahlungsausfälle** | Erkennung von Betrugsversuchen (gestohlene Kreditkarten) |

## 5. Verdachtsmeldung

Sollten dennoch Anhaltspunkte für Geldwäsche oder Terrorismusfinanzierung vorliegen:

1. **Interne Meldung** an Compliance-Verantwortlichen (compliance@miau.finance)
2. **Prüfung** des Sachverhalts innerhalb von 48 Stunden
3. **Ggf. Meldung an FIU** (Financial Intelligence Unit) gemäß § 43 GwG
4. **Dokumentation** des Vorgangs

## 6. Aufbewahrung von Unterlagen

- KYC-Dokumente: 5 Jahre nach Vertragsende (§ 8 Abs. 1 GwG)
- Verdachtsmeldungen: 5 Jahre nach Meldung
- Sonstige AML-relevante Dokumente: 5 Jahre

## 7. Schulungen

Der Compliance-Verantwortliche nimmt jährlich an einer AML-Schulung teil.

## 8. Verantwortlichkeiten

| Funktion | Verantwortung |
|----------|---------------|
| **Compliance-Verantwortlicher** | Überwachung der AML-Richtlinien, Meldungen |
| **Geschäftsführung** | Freigabe der Richtlinie, Sanktionen |

---

**Kontakt:** compliance@miau.finance  
**Nächste Überprüfung:** Mai 2027
