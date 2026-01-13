# 🔍 Case Intelligence & Network Analysis System

> **Django-basiertes Analyse-System zur Untersuchung komplexer Beziehungsnetzwerke**  
> Inspiriert von graph-basierten Intelligence-Tools

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Demo-Live-success.svg)](https://palantir-clone.fly.dev)

---

## 📋 Übersicht

Dieses Projekt demonstriert die Entwicklung eines **produktionsreifen Django-Systems** zur Verwaltung und Analyse von vernetzten Daten. Das System ermöglicht:

- **Graph-basierte Beziehungsanalyse** zwischen Entitäten
- **Fall-übergreifende Musterkennung** (Cross-Case-Analysis)
- **Timeline-basierte Rekonstruktion** von Ereignisabläufen
- **Risikobewertung** mit mehrschichtigen Scoring-Algorithmen
- **Interaktive Netzwerk-Visualisierung** mit Physik-Simulation

### 🎯 Zielstellung

Das Projekt dient als **Referenzprojekt für Bewerbungen** und demonstriert:
- Saubere Django-Architektur mit App-Separation
- Durchdachte relationale Datenmodellierung
- Service-Layer-Pattern für Business-Logik
- Query-Optimierung (select_related/prefetch_related)
- Produktions-Deployment mit Fly.io

---

## 🚀 Live Demo

**[➡️ Demo starten](https://palantir-clone.fly.dev)**

Nutzen Sie den **One-Click Demo-Login** auf der Login-Seite, um das System mit Beispieldaten zu erkunden.

> ⚠️ **Disclaimer:** Alle Daten im Demo-System sind **vollständig fiktiv**. Es werden keine echten personenbezogenen Daten gespeichert oder verarbeitet.

---

## 🏗️ Architektur

### App-Struktur

```
palantir_system/          # Django Projekt-Konfiguration
├── settings.py           # Environment-basierte Config
├── urls.py               # URL-Routing
└── wsgi.py               # WSGI Application

entities/                 # Stammdaten-Verwaltung
├── models.py             # Person, Address, Vehicle, Relationships
├── views.py              # CRUD + Analyse-Views
├── services.py           # Business-Logik (Network-Metriken, Risiko-Scoring)
├── tests.py              # Unit & Integration Tests
└── urls.py

investigations/           # Fall-Management
├── models.py             # Case, Evidence, Timeline, PersonInvolvement
├── views.py              # Dashboard, Search, Timeline-Management
├── services.py           # Case-Analysis, Dashboard-Aggregation
├── tests.py
└── management/commands/  # Custom Commands (load_sample_data, setup_demo_user)

templates/                # Django Templates mit Bootstrap 5
```

### Datenmodell

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Person    │────▶│ PersonInvolvement│◀────│    Case     │
│             │     │   (Through)       │     │             │
│ - risk_level│     │ - role           │     │ - status    │
│ - aliases   │     │ - credibility    │     │ - priority  │
└─────────────┘     └──────────────────┘     └─────────────┘
       │                                            │
       │ PersonRelationship                         │
       ▼ (self-referencing M:N)                     ▼
┌─────────────┐                             ┌─────────────┐
│   Address   │                             │  Evidence   │
│   Vehicle   │                             │  Timeline   │
└─────────────┘                             └─────────────┘
```

### Technologie-Stack

| Kategorie | Technologie |
|-----------|-------------|
| **Backend** | Django 5.2, Django REST Framework |
| **Datenbank** | SQLite (dev), PostgreSQL (prod) |
| **Frontend** | Bootstrap 5, Vanilla JS, Canvas API |
| **Deployment** | Fly.io, Whitenoise, Gunicorn |
| **Sicherheit** | CSRF Protection, HTTPS, Secure Headers |

---

## ✨ Features

### Kern-Funktionalität

| Feature | Beschreibung |
|---------|--------------|
| **Netzwerk-Visualisierung** | Interaktive Canvas-basierte Graph-Darstellung mit Physik-Simulation |
| **Cross-Case-Analysis** | Identifikation von Personen in mehreren Fällen |
| **Risiko-Scoring** | Mehrfaktorieller Score (Basis + Netzwerk + Fall-Beteiligung) |
| **Timeline-Analyse** | Lücken-Erkennung und zeitliche Mustererkennung |
| **Globale Suche** | Durchsucht alle Entitätstypen gleichzeitig |

### Service-Layer (Highlights)

```python
# entities/services.py
class PersonAnalysisService:
    @staticmethod
    def calculate_risk_score(person) -> dict:
        """
        Mehrfaktorieller Risiko-Score:
        - Basis-Risikostufe (0-80 Punkte)
        - Fall-Beteiligungen (max. 30 Punkte)
        - Rollen-Gewichtung (Verdächtiger +10)
        - Netzwerk-Zentralität (max. 20 Punkte)
        """
        # ... Implementation
```

---

## 🔧 Installation

### Voraussetzungen

- Python 3.11+
- pip / venv

### Quick Start

```bash
# Repository klonen
git clone https://github.com/Thomas7899/palantir-clone.git
cd palantir-clone

# Virtual Environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Datenbank & Beispieldaten
python manage.py migrate
python manage.py createsuperuser
python manage.py load_sample_data

# Server starten
python manage.py runserver
```

### Tests ausführen

```bash
python manage.py test entities investigations
```

---

## 🔐 Sicherheit

### Demo-Umgebung

Das öffentlich deployete System unter `palantir-clone.fly.dev` ist eine **isolierte Demo-Umgebung**:

- ✅ Alle Daten sind **fiktiv** (keine echten personenbezogenen Daten)
- ✅ Demo-User hat **eingeschränkte Rechte** (kein Admin-Zugang)
- ✅ **HTTPS-only** mit HSTS
- ✅ CSRF-Protection aktiviert
- ✅ Secure Session/Cookie-Flags in Produktion

### Credentials-Handling

```python
# Sichere Konfiguration via Environment Variables
SECRET_KEY = config('SECRET_KEY')  # Nicht im Repository
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASE_URL = config('DATABASE_URL')  # Fly.io Postgres Secret
```

> **Hinweis für Entwickler:** Niemals Credentials committen. Nutze `python-decouple` oder Environment-Variablen.

---

## 📈 Erweiterungsmöglichkeiten

### Geplante Features (Roadmap)

- [ ] REST API mit DRF ViewSets
- [ ] React-Frontend (TypeScript)
- [ ] Erweiterte Graph-Metriken (Betweenness Centrality, Clustering Coefficient)
- [ ] Export-Funktionen (PDF-Reports, CSV)
- [ ] Audit-Log für alle Änderungen

### Integration-Punkte

Das System ist vorbereitet für:
- **REST API** (Django REST Framework bereits konfiguriert)
- **React-Frontend** (CORS-Headers konfiguriert)
- **PostgreSQL** (dj-database-url für einfache Migration)

---

## 🧪 Code-Qualität

### Test-Abdeckung

```bash
python manage.py test --verbosity=2
```

Tests umfassen:
- **Model-Tests:** Validierung von Properties, Constraints, String-Darstellung
- **Service-Tests:** Business-Logik, Berechnungen, Daten-Aggregation
- **View-Tests:** Authentication, Permissions, Response-Codes

### Architektur-Prinzipien

- **Separation of Concerns:** Views → Services → Models
- **Query-Optimierung:** Konsequente Nutzung von `select_related`/`prefetch_related`
- **Type Hints:** Für bessere IDE-Unterstützung und Dokumentation

---

## 📝 Lizenz

MIT License - siehe [LICENSE](LICENSE)

---

## 👤 Autor

**Thomas Osterlehner**

- Portfolio-Projekt für Bewerbungen im Bereich **Fullstack Development**
- Fokus: Django, Python, React, Datenanalyse

---

## 🙏 Danksagung

Inspiriert von graph-basierten Analyse-Tools und Intelligence-Systemen.
Entwickelt als Demonstration moderner Django-Entwicklungspraktiken.
