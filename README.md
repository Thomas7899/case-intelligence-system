# Palantir Gotham Clone - Polizei-Ermittlungssystem

Ein Django-basiertes System für Polizei-Ermittlungen, inspiriert von Palantir Gotham. Dieses System ermöglicht die Verwaltung von Personen, Fällen, Beziehungen und Beweismitteln mit erweiterten Analyse-Funktionen.

### Anmeldung
- URL: http://127.0.0.1:8000/
- Admin-Panel: http://127.0.0.1:8000/admin/
- Benutzer: admin
- Passwort: password

## 🚀 Features

### Kern-Funktionen
- **👥 Personen-Management** - Vollständige Verwaltung von Personen mit Risikobewertung
- **📁 Fall-Management** - Strukturierte Fallbearbeitung mit Timeline
- **🔗 Beziehungsanalyse** - Visualisierung von Verbindungen zwischen Personen
- **🔍 Globale Suche** - Durchsuche alle Entitäten gleichzeitig
- **📊 Erweiterte Analysen** - Fall-übergreifende Muster und Verbindungen

### Entitäten
- **Personen** - Mit Risikostufen, Aliasen und Notizen
- **Adressen** - Geografische Daten mit Koordinaten-Unterstützung
- **Fahrzeuge** - Verknüpft mit Besitzern
- **Fälle** - Kategorisiert nach Typ, Status und Priorität
- **Beweismittel** - Verschiedene Typen (physisch, digital, video, etc.)
- **Timeline** - Chronologische Ereignisse pro Fall

### Analyse-Tools
- **🕸️ Netzwerk-Visualisierung** - Interaktive Darstellung von Beziehungen
- **📈 Fall-übergreifende Analyse** - Identifikation von Mehrfach-Beteiligten
- **🎯 Hotspot-Analyse** - Personen mit vielen Verbindungen
- **📊 Statistiken** - Umfassende Datenauswertung

## 🏗️ Technologie-Stack

- **Backend**: Django 5.2
- **Datenbank**: SQLite (einfach auf PostgreSQL umstellbar)
- **Frontend**: Bootstrap 5 mit Django Templates
- **Visualisierung**: Canvas-basierte Netzwerk-Grafiken mit Physik-Simulation
- **Zusätzliche Pakages**: 
  - Django REST Framework (vorbereitet)
  - Django Debug Toolbar
  - Django Extensions
  - Django CORS Headers

## 🔧 Installation & Setup

1. **Repository klonen**
```bash
git clone https://github.com/IhrUsername/palantir-clone.git
cd palantir-clone
```

2. **Virtual Environment erstellen**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# oder
venv\Scripts\activate  # Windows
```

3. **Dependencies installieren**
```bash
pip install -r requirements.txt
```

4. **Datenbank migrieren**
```bash
python manage.py migrate
```

5. **Superuser erstellen**
```bash
python manage.py createsuperuser
```

6. **Beispieldaten laden (optional)**
```bash
python manage.py load_sample_data
```

7. **Server starten**
```bash
python manage.py runserver
```

## 🎯 Verwendung

### 1. Server starten
```bash
python manage.py runserver
```

### 2. Anmeldung
- URL: http://127.0.0.1:8000/
- Admin-Panel: http://127.0.0.1:8000/admin/
- Benutzer: admin
- Passwort: password

### 3. Bereiche im System

#### Dashboard
- Übersicht über aktuelle Fälle
- Statistiken
- Hochrisiko-Personen
- Anstehende Ermittlungsmaßnahmen

#### Fälle
- Fallverwaltung mit Status-Tracking
- Beteiligte Personen
- Beweismittel
- Ermittlungsmaßnahmen
- Zeitachse

#### Personen
- Personenstammdaten
- Risikobewertung
- Adresszuordnungen
- Fahrzeuge
- Beziehungen

#### Beziehungen
- Interaktive Netzwerk-Visualisierung mit Canvas
- Beziehungstypen
- Stärkebewertung
- Fall-übergreifende Analyse
- Physik-Simulation für Netzwerk-Layout

#### Suche
- Globale Suche über alle Entitäten
- Durchsuche Personen, Fälle, Adressen, Fahrzeuge
- Erweiterte Filterfunktionen

#### Cross-Case-Analyse
- Identifikation von Personen in mehreren Fällen
- Netzwerk-Hubs mit vielen Verbindungen
- Fall-Cluster-Analyse
- Risikobewertung über Fälle hinweg
