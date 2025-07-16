# Palantir Gotham Clone - Polizei-Ermittlungssystem

Ein Django-basiertes System für Polizei-Ermittlungen, inspiriert von Palantir Gotham. Dieses System ermöglicht die Verwaltung von Personen, Fällen, Beziehungen und Beweismitteln mit erweiterten Analyse-Funktionen.

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
- Benutzer: Ihr erstellter Superuser

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

## 📊 Beispieldaten

Das System wurde mit umfangreichen Beispieldaten befüllt:

### Fälle (230+ Fälle)
- **50 detaillierte Hauptfälle** mit verschiedenen Delikttypen
- **100 auto-generierte 2024-Fälle** für aktuelle Ermittlungen
- **80 historische 2023-Fälle** für Vergleichsanalysen
- Verschiedene Kategorien: Betrug, Diebstahl, Körperverletzung, Drogenhandel, etc.

### Personen (1000+ Personen)
- Realistische Namen und Daten
- Verschiedene Risikostufen
- Umfassende Beziehungsstrukturen
- Mehrfach-Beteiligungen in verschiedenen Fällen

### Fahrzeuge & Adressen
- Realistische Fahrzeugdaten mit Kennzeichen
- Adressdaten mit Geodaten-Unterstützung
- Verknüpfungen zu Personen und Fällen

### Beweismittel & Timeline
- Verschiedene Beweismitteltypen
- Chronologische Timeline-Einträge
- Verknüpfungen zwischen Beweisen und Fällen

### Laden der Beispieldaten
```bash
python manage.py load_sample_data
```

**Hinweis**: Das Laden der Beispieldaten kann einige Minuten dauern aufgrund der umfangreichen Datenstruktur.

## � Ähnlichkeit zu Palantir Gotham

**Ähnlichkeitsgrad: ~70-75%**

### ✅ Vollständig implementiert
- **Entitäten-Management**: Personen, Adressen, Fahrzeuge, Fälle
- **Beziehungsanalyse**: Netzwerk-Visualisierung mit interaktiver Canvas
- **Fallmanagement**: Strukturierte Fallbearbeitung mit Timeline
- **Suchfunktionen**: Globale Suche über alle Entitäten
- **Cross-Case-Analyse**: Fall-übergreifende Verbindungen
- **Basis-Visualisierung**: Interaktive Netzwerk-Darstellung

### 🔶 Teilweise implementiert
- **Erweiterte Visualisierung**: Canvas-basiert (nicht 3D)
- **Datenintegration**: Über Django Models (nicht Big Data)
- **Analytics**: Basis-Statistiken und Hotspot-Analyse
- **Timeline-Features**: Chronologische Darstellung implementiert

### ❌ Noch nicht implementiert
- **Machine Learning/AI**: Automatische Mustererkennung
- **Big Data Processing**: Verarbeitung großer Datenmengen
- **3D-Visualisierung**: Räumliche Darstellung
- **Externe Datenquellen**: Integration verschiedener Systeme
- **Enterprise-Features**: SSO, erweiterte Rechteverwaltung
- **Geospatial Analysis**: Erweiterte Karten-Integration

## � Datenschutz & Sicherheit

⚠️ **Wichtiger Hinweis**: Dies ist ein Prototyp für Demonstrationszwecke. Für den produktiven Einsatz müssen folgende Sicherheitsmaßnahmen implementiert werden:

- Verschlüsselung sensibler Daten
- Audit-Logging aller Zugriffe
- Rollenbasierte Zugriffskontrolle
- Sichere Authentifizierung (2FA)
- Backup & Recovery-Prozesse
- Compliance mit DSGVO/GDPR

## 🤝 Weiterentwicklung

Das System ist modular aufgebaut und kann einfach erweitert werden:

1. **Neue Entitäten**: Weitere Modelle in `entities/models.py`
2. **Neue Views**: Erweiterte Ansichten in `*/views.py`
3. **API-Endpunkte**: REST API mit Django REST Framework
4. **Frontend**: React/Vue.js für interaktive Komponenten
5. **Datenbank**: PostgreSQL mit PostGIS für Geodaten

## 📚 Projektstruktur

```
palantir-clone/
├── entities/                    # Entitäten-Management
│   ├── models.py               # Datenmodelle für Personen, Adressen, Fahrzeuge
│   ├── views.py                # Views für Beziehungsanalyse
│   └── urls.py                 # URL-Routing
├── investigations/             # Ermittlungen und Fälle
│   ├── models.py               # Datenmodelle für Fälle, Beweise, Timeline
│   ├── views.py                # Views für Fallmanagement
│   ├── urls.py                 # URL-Routing
│   └── management/commands/    # Management-Commands
│       └── load_sample_data.py # Beispieldaten-Generator
├── palantir_system/           # Django-Hauptkonfiguration
│   ├── settings.py            # Projekteinstellungen
│   └── urls.py                # Haupt-URL-Routing
├── templates/                 # HTML-Templates
│   ├── base.html              # Basis-Template
│   ├── entities/              # Templates für Entitäten
│   └── investigations/        # Templates für Ermittlungen
├── requirements.txt           # Python-Abhängigkeiten
├── manage.py                  # Django-Management-Skript
└── README.md                  # Diese Datei
```

## � Datenmodell

### Kern-Entitäten
```
Person ←→ PersonRelationship ←→ Person
Person ←→ PersonInvolvement ←→ Case
Person ←→ PersonAddress ←→ Address
Person ←→ Vehicle
Case ←→ Evidence
Case ←→ Timeline
Case ←→ Investigation
```

### Beziehungstypen
- **Familie**: Verwandtschaftsbeziehungen
- **Geschäft**: Geschäftliche Verbindungen
- **Freundschaft**: Persönliche Beziehungen
- **Kriminalität**: Tatbezogene Verbindungen
- **Bekannte**: Allgemeine Bekanntschaften

## 🔧 Konfiguration

### Umgebungsvariablen
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Erweiterte Konfiguration
- **Django Admin Interface**: `/admin/` - Vollständige Datenverwaltung
- **Debug Toolbar**: Aktiviert im Development-Modus
- **URL Namespaces**: Saubere URL-Struktur mit App-Namespaces
- **Static Files**: Bootstrap 5 und eigene CSS/JS-Dateien

## 🔮 Roadmap

### Version 2.0 - Erweiterte Visualisierung
- [ ] **Karten-Integration** (Leaflet/OpenStreetMap)
- [ ] **Graph-Datenbank** (Neo4j) für komplexe Beziehungen
- [ ] **Erweiterte Suche** (Elasticsearch)
- [ ] **REST API** Vollausbau
- [ ] **CSV-Import/Export** für Datenintegration
- [ ] **PDF-Berichte** für Fallakten

### Version 3.0 - Intelligence Features
- [ ] **Machine Learning** für Risikovorhersagen
- [ ] **NLP** für automatische Textanalyse
- [ ] **Real-time Updates** mit WebSockets
- [ ] **Mobile App** für Außendienstmitarbeiter
- [ ] **Audit-Trail** für alle Systemzugriffe

### Version 4.0 - Enterprise
- [ ] **React/Vue.js Frontend** für bessere UX
- [ ] **PostGIS** für geografische Analysen
- [ ] **Kubernetes** Deployment
- [ ] **SSO Integration** (Active Directory)
- [ ] **Multi-Tenant** Architektur
- [ ] **Big Data Processing** mit Apache Spark

## 🔒 Datenschutz & Sicherheit

⚠️ **Wichtiger Hinweis**: Dies ist ein Prototyp für Demonstrationszwecke. Für den produktiven Einsatz müssen folgende Sicherheitsmaßnahmen implementiert werden:

### Erforderliche Sicherheitsmaßnahmen
- **🔐 Verschlüsselung**: Sensitive Daten End-to-End verschlüsseln
- **📝 Audit-Logging**: Vollständige Protokollierung aller Systemzugriffe
- **🛡️ Rollenbasierte Zugriffskontrolle**: Granulare Berechtigungen
- **🔑 Sichere Authentifizierung**: 2FA, SSO-Integration
- **💾 Backup & Recovery**: Automatische Datensicherung
- **⚖️ DSGVO-Compliance**: Datenschutzkonform implementieren

### Produktive Umgebung
- **PostgreSQL**: Für bessere Performance und Skalierbarkeit
- **Redis**: Für Session-Management und Caching
- **Nginx**: Als Reverse Proxy mit SSL/TLS
- **Docker**: Für konsistente Deployments
- **Monitoring**: Logging und Alerting-System

## 🤝 Beitragen

Wir freuen uns über Beiträge zur Weiterentwicklung des Systems!

### Entwicklung
1. **Fork** das Repository
2. **Clone** deinen Fork: `git clone https://github.com/dein-username/palantir-clone.git`
3. **Branch** erstellen: `git checkout -b feature/amazing-feature`
4. **Änderungen** committen: `git commit -m 'Add amazing feature'`
5. **Push** zum Branch: `git push origin feature/amazing-feature`
6. **Pull Request** öffnen

### Coding Standards
- **PEP 8**: Python-Coding-Standards befolgen
- **Django Best Practices**: Django-Konventionen einhalten
- **Tests**: Unit Tests für neue Features
- **Dokumentation**: Code-Kommentare und Docstrings

## 🎉 Erste Schritte

1. **Installation** durchführen (siehe oben)
2. **Server starten**: `python manage.py runserver`
3. **Dashboard erkunden**: http://127.0.0.1:8000/
4. **Beispieldaten laden**: `python manage.py load_sample_data`
5. **Suchfunktion testen**: Namen oder Aktenzeichen eingeben
6. **Beziehungsanalyse**: Netzwerk-Visualisierung erkunden
7. **Eigene Fälle erstellen**: Über das Admin-Interface

## 📞 Support & Community

- **🐛 Bug Reports**: GitHub Issues
- **💡 Feature Requests**: GitHub Discussions
- **📚 Dokumentation**: Wiki (geplant)
- **💬 Community**: Discussions Tab

## 🏆 Inspiration

Dieses Projekt ist inspiriert von **Palantir Gotham**, dem führenden System für Ermittlungsanalysen und Intelligence-Auswertung. Ziel ist es, die Kern-Konzepte und Funktionalitäten in einer Open-Source-Django-Anwendung zu demonstrieren und für Bildungszwecke sowie kleinere Strafverfolgungsbehörden zugänglich zu machen.

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe `LICENSE` für Details.

## ⚠️ Disclaimer

Diese Software ist für **Bildungs- und Demonstrationszwecke** entwickelt. Sie ist nicht für den produktiven Einsatz in echten Polizei-Ermittlungen gedacht, ohne entsprechende Sicherheitsüberprüfungen, Datenschutzmaßnahmen und Anpassungen an lokale Gesetze und Vorschriften.

---

**Entwickelt mit ❤️ für die Strafverfolgung und Bildung**

*Palantir Gotham Clone - Bringing Intelligence Analysis to Open Source*
