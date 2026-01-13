from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from entities.models import Person, Address, Vehicle, PersonAddress, PersonRelationship
from investigations.models import Case, PersonInvolvement, Evidence, Investigation, Timeline
from django.utils import timezone
import random
from datetime import datetime as dt, timedelta


class Command(BaseCommand):
    help = 'Lädt Beispieldaten für das Case Intelligence System'

    def handle(self, *args, **options):
        self.stdout.write('Lade Beispieldaten...')
        
        # Superuser als Ersteller verwenden
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('Kein Superuser gefunden. Bitte erstelle zuerst einen Superuser.'))
            return
        
        # Adressen erstellen
        addresses = []
        address_data = [
            ('Hauptstraße', '15', '12345', 'Berlin'),
            ('Bahnhofstraße', '8', '54321', 'Hamburg'),
            ('Musterweg', '42', '67890', 'München'),
            ('Teststraße', '3', '11111', 'Köln'),
            ('Beispielweg', '99', '22222', 'Frankfurt'),
        ]
        
        for street, number, plz, city in address_data:
            address, created = Address.objects.get_or_create(
                street=street,
                house_number=number,
                postal_code=plz,
                city=city
            )
            addresses.append(address)
            if created:
                self.stdout.write(f'Adresse erstellt: {address}')
        
        # Personen erstellen
        persons = []
        person_data = [
            ('Max', 'Mustermann', '1985-03-15', 2),
            ('Anna', 'Schmidt', '1992-07-22', 1),
            ('Peter', 'Müller', '1978-11-30', 3),
            ('Lisa', 'Weber', '1990-05-10', 0),
            ('Michael', 'Fischer', '1982-09-08', 4),
            ('Sarah', 'Wagner', '1995-12-01', 2),
            ('Thomas', 'Bauer', '1975-04-18', 1),
            ('Julia', 'Richter', '1988-08-25', 0),
        ]
        
        for first_name, last_name, birth_date, risk_level in person_data:
            person, created = Person.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                defaults={
                    'birth_date': dt.strptime(birth_date, '%Y-%m-%d').date(),
                    'risk_level': risk_level,
                    'created_by': admin_user
                }
            )
            persons.append(person)
            if created:
                self.stdout.write(f'Person erstellt: {person}')
        
        # Personen mit Adressen verknüpfen
        for i, person in enumerate(persons):
            address = addresses[i % len(addresses)]
            PersonAddress.objects.get_or_create(
                person=person,
                address=address,
                defaults={
                    'address_type': 'primary',
                    'start_date': timezone.now().date() - timedelta(days=random.randint(30, 1000))
                }
            )
        
        # Fahrzeuge erstellen
        vehicle_data = [
            ('B-AB 123', 'car', 'BMW', '3er', 2020, 'Schwarz', persons[0]),
            ('HH-CD 456', 'car', 'Mercedes', 'C-Klasse', 2019, 'Silber', persons[1]),
            ('M-EF 789', 'motorcycle', 'Yamaha', 'MT-07', 2021, 'Blau', persons[2]),
            ('K-GH 012', 'car', 'Audi', 'A4', 2018, 'Weiß', persons[3]),
            ('F-IJ 345', 'truck', 'MAN', 'TGX', 2017, 'Rot', persons[4]),
        ]
        
        for plate, v_type, make, model, year, color, owner in vehicle_data:
            vehicle, created = Vehicle.objects.get_or_create(
                license_plate=plate,
                defaults={
                    'vehicle_type': v_type,
                    'make': make,
                    'model': model,
                    'year': year,
                    'color': color,
                    'owner': owner
                }
            )
            if created:
                self.stdout.write(f'Fahrzeug erstellt: {vehicle}')
        
        # Beziehungen erstellen
        relationships = [
            (persons[0], persons[1], 'friend', 'Bekannt aus der Schule'),
            (persons[1], persons[2], 'colleague', 'Arbeiten im gleichen Unternehmen'),
            (persons[2], persons[3], 'family', 'Geschwister'),
            (persons[3], persons[4], 'neighbor', 'Wohnen nebeneinander'),
            (persons[4], persons[5], 'associate', 'Geschäftspartner'),
            (persons[0], persons[2], 'suspect', 'Verdächtige Verbindung'),
        ]
        
        for person1, person2, rel_type, description in relationships:
            relationship, created = PersonRelationship.objects.get_or_create(
                person1=person1,
                person2=person2,
                relationship_type=rel_type,
                defaults={
                    'description': description,
                    'strength': random.randint(1, 5),
                    'created_by': admin_user
                }
            )
            if created:
                self.stdout.write(f'Beziehung erstellt: {relationship}')
        
        # Fälle erstellen (erweitert für realistisches Erlebnis)
        cases = []
        case_data = [
            # Diebstahl-Fälle
            ('2024-001', 'Einbruch Hauptstraße', 'Einbruch in Wohnhaus mit Diebesgut im Wert von 15.000€', 'theft', 'open', 'high', addresses[0]),
            ('2024-005', 'Ladendiebstahl Kaufhof', 'Diebstahl von Elektronikartikeln', 'theft', 'closed', 'low', addresses[1]),
            ('2024-012', 'Fahrraddiebstahl Bahnhof', 'Hochwertiges E-Bike gestohlen', 'theft', 'in_progress', 'medium', addresses[2]),
            ('2024-018', 'Einbruch Juwelier', 'Schwerer Einbruch mit Sachschaden', 'theft', 'open', 'urgent', addresses[3]),
            ('2024-023', 'Autodiebstahl Parkhaus', 'BMW gestohlen aus Tiefgarage', 'theft', 'in_progress', 'high', addresses[4]),
            ('2024-029', 'Taschendiebstahl Marktplatz', 'Handtasche während Einkauf gestohlen', 'theft', 'closed', 'low', addresses[0]),
            ('2024-034', 'Kellereinbruch Wohnhaus', 'Mehrere Keller aufgebrochen', 'theft', 'open', 'medium', addresses[1]),
            ('2024-041', 'Diebstahl Baustelle', 'Werkzeuge und Maschinen gestohlen', 'theft', 'in_progress', 'high', addresses[2]),
            
            # Betrugs-Fälle
            ('2024-002', 'Betrugsfall Weber', 'Onlinebetrug über gefälschte Kleinanzeigen', 'fraud', 'in_progress', 'medium', addresses[1]),
            ('2024-008', 'Kreditkartenbetrug', 'Missbrauch von Kreditkartendaten', 'fraud', 'open', 'high', addresses[2]),
            ('2024-015', 'Enkeltrick Senioren', 'Telefonbetrug an älteren Menschen', 'fraud', 'closed', 'medium', addresses[3]),
            ('2024-021', 'Internetbetrug PayPal', 'Fake-Verkäufer auf Online-Plattform', 'fraud', 'in_progress', 'low', addresses[4]),
            ('2024-027', 'Versicherungsbetrug', 'Vorgetäuschter Autounfall', 'fraud', 'open', 'high', addresses[0]),
            ('2024-032', 'Anlagebetrug', 'Schneeballsystem mit hohen Verlusten', 'fraud', 'in_progress', 'urgent', addresses[1]),
            ('2024-038', 'Phishing-Angriff Bank', 'Gefälschte Banking-Website', 'fraud', 'closed', 'medium', addresses[2]),
            ('2024-044', 'Romance Scam', 'Liebesbetrug über Dating-Apps', 'fraud', 'open', 'low', addresses[3]),
            
            # Körperverletzung
            ('2024-003', 'Körperverletzung Bahnhof', 'Schlägerei am Bahnhof mit Verletzten', 'assault', 'closed', 'high', addresses[2]),
            ('2024-009', 'Prügelei Kneipe', 'Auseinandersetzung in Gaststätte', 'assault', 'in_progress', 'medium', addresses[3]),
            ('2024-016', 'Straßenraub', 'Raubüberfall auf Fußgänger', 'assault', 'open', 'urgent', addresses[4]),
            ('2024-024', 'Mobbing Arbeitsplatz', 'Systematische Belästigung am Arbeitsplatz', 'assault', 'in_progress', 'low', addresses[0]),
            ('2024-030', 'Vandalismus Schule', 'Sachbeschädigung und Bedrohung', 'assault', 'closed', 'medium', addresses[1]),
            ('2024-036', 'Nachbarschaftsstreit', 'Körperliche Auseinandersetzung', 'assault', 'open', 'low', addresses[2]),
            ('2024-042', 'Überfall Tankstelle', 'Bewaffneter Raubüberfall', 'assault', 'in_progress', 'urgent', addresses[3]),
            
            # Drogen-Fälle
            ('2024-004', 'Drogenhandel Musterweg', 'Verdacht auf Verkauf von Betäubungsmitteln', 'drug', 'open', 'high', addresses[3]),
            ('2024-010', 'Cannabis-Plantage', 'Illegaler Anbau in Wohnung', 'drug', 'closed', 'medium', addresses[4]),
            ('2024-017', 'Drogenlabor Industriegebiet', 'Herstellung synthetischer Drogen', 'drug', 'in_progress', 'urgent', addresses[0]),
            ('2024-025', 'Dealer Schulhof', 'Drogenverkauf an Minderjährige', 'drug', 'open', 'urgent', addresses[1]),
            ('2024-031', 'Kokain-Schmuggel', 'Einfuhr größerer Mengen', 'drug', 'in_progress', 'high', addresses[2]),
            ('2024-037', 'Drogen-Razzia Club', 'Verkauf in Diskothek', 'drug', 'closed', 'medium', addresses[3]),
            ('2024-043', 'Methamphetamin-Ring', 'Organisierter Drogenhandel', 'drug', 'open', 'urgent', addresses[4]),
            
            # Verkehrs-Fälle
            ('2024-006', 'Unfallflucht Autobahn', 'Fahrerflucht nach schwerem Unfall', 'traffic', 'open', 'high', addresses[0]),
            ('2024-013', 'Alkohol am Steuer', 'Trunkenheit im Verkehr', 'traffic', 'closed', 'medium', addresses[1]),
            ('2024-019', 'Raser Innenstadt', 'Illegale Straßenrennen', 'traffic', 'in_progress', 'high', addresses[2]),
            ('2024-026', 'Führerschein-Betrug', 'Fahren ohne gültige Fahrerlaubnis', 'traffic', 'open', 'low', addresses[3]),
            ('2024-033', 'LKW-Überladung', 'Verstoß gegen Ladungsvorschriften', 'traffic', 'closed', 'low', addresses[4]),
            ('2024-039', 'Gefährlicher Eingriff', 'Manipulation an Verkehrszeichen', 'traffic', 'in_progress', 'medium', addresses[0]),
            ('2024-045', 'Hit-and-Run', 'Unfallflucht mit Personenschaden', 'traffic', 'open', 'urgent', addresses[1]),
            
            # Häusliche Gewalt
            ('2024-007', 'Häusliche Gewalt Müllerstraße', 'Wiederholte Gewalt in Beziehung', 'domestic', 'in_progress', 'urgent', addresses[2]),
            ('2024-014', 'Stalking Ex-Partner', 'Beharrliche Verfolgung', 'domestic', 'open', 'high', addresses[3]),
            ('2024-020', 'Kindesmisshandlung', 'Verdacht auf Gewalt gegen Minderjährige', 'domestic', 'in_progress', 'urgent', addresses[4]),
            ('2024-028', 'Bedrohung Familie', 'Wiederholte Drohungen', 'domestic', 'closed', 'medium', addresses[0]),
            ('2024-035', 'Zwangsehe', 'Verdacht auf Nötigung zur Ehe', 'domestic', 'open', 'high', addresses[1]),
            ('2024-040', 'Gewalt gegen Senioren', 'Misshandlung pflegebedürftiger Person', 'domestic', 'in_progress', 'urgent', addresses[2]),
            
            # Sonstige Fälle
            ('2024-011', 'Sachbeschädigung Park', 'Vandalismus an öffentlichen Einrichtungen', 'other', 'closed', 'low', addresses[3]),
            ('2024-022', 'Urkundenfälschung', 'Gefälschte Dokumente', 'other', 'in_progress', 'medium', addresses[4]),
            ('2024-046', 'Cybercrime Hacking', 'Angriff auf Computersystem', 'other', 'open', 'high', addresses[0]),
            ('2024-047', 'Geldwäsche', 'Verdacht auf Geldwäsche', 'other', 'in_progress', 'high', addresses[1]),
            ('2024-048', 'Menschenhandel', 'Verdacht auf Zwangsprostitution', 'other', 'open', 'urgent', addresses[2]),
            ('2024-049', 'Umweltdelikt', 'Illegale Entsorgung von Chemikalien', 'other', 'closed', 'medium', addresses[3]),
            ('2024-050', 'Korruption Behörde', 'Bestechung von Amtsträgern', 'other', 'in_progress', 'urgent', addresses[4]),
        ]
        
        for case_number, title, description, case_type, status, priority, location in case_data:
            case, created = Case.objects.get_or_create(
                case_number=case_number,
                defaults={
                    'title': title,
                    'description': description,
                    'case_type': case_type,
                    'status': status,
                    'priority': priority,
                    'location': location,
                    'incident_date': timezone.now() - timedelta(days=random.randint(1, 90)),
                    'created_by': admin_user,
                    'assigned_to': admin_user if random.choice([True, False]) else None
                }
            )
            cases.append(case)
            if created:
                self.stdout.write(f'Fall erstellt: {case}')
        
        # Zusätzliche automatisch generierte Fälle
        case_types = ['theft', 'fraud', 'assault', 'drug', 'traffic', 'domestic', 'other']
        priorities = ['low', 'medium', 'high', 'urgent']
        statuses = ['open', 'in_progress', 'closed', 'suspended']
        
        for i in range(51, 151):  # 100 zusätzliche Fälle
            case_type = random.choice(case_types)
            priority = random.choice(priorities)
            status = random.choice(statuses)
            location = random.choice(addresses)
            
            case_titles = {
                'theft': ['Diebstahl', 'Einbruch', 'Raub', 'Autodiebstahl', 'Ladendiebstahl'],
                'fraud': ['Betrug', 'Internetbetrug', 'Kreditkartenbetrug', 'Anlagebetrug', 'Versicherungsbetrug'],
                'assault': ['Körperverletzung', 'Schlägerei', 'Bedrohung', 'Überfall', 'Gewalt'],
                'drug': ['Drogenhandel', 'Drogenlabor', 'Dealer', 'Schmuggel', 'Plantage'],
                'traffic': ['Unfallflucht', 'Verkehrsdelikt', 'Raser', 'Alkohol', 'Führerschein'],
                'domestic': ['Häusliche Gewalt', 'Stalking', 'Bedrohung', 'Misshandlung', 'Nötigung'],
                'other': ['Sachbeschädigung', 'Urkundenfälschung', 'Cybercrime', 'Umweltdelikt', 'Korruption']
            }
            
            title_base = random.choice(case_titles[case_type])
            location_name = location.street if location.street else location.city
            
            case, created = Case.objects.get_or_create(
                case_number=f'2024-{i:03d}',
                defaults={
                    'title': f'{title_base} {location_name}',
                    'description': f'Automatisch generierter Fall: {title_base} in {location.city}',
                    'case_type': case_type,
                    'status': status,
                    'priority': priority,
                    'location': location,
                    'incident_date': timezone.now() - timedelta(days=random.randint(1, 365)),
                    'created_by': admin_user,
                    'assigned_to': admin_user if random.choice([True, False, False]) else None
                }
            )
            cases.append(case)
            if created:
                self.stdout.write(f'Fall erstellt: {case}')
        
        # Weitere historische Fälle aus 2023
        for i in range(1, 81):  # 80 Fälle aus 2023
            case_type = random.choice(case_types)
            priority = random.choice(priorities)
            status = random.choice(['closed', 'closed', 'closed', 'suspended'])  # Meist abgeschlossen
            location = random.choice(addresses)
            
            title_base = random.choice(case_titles[case_type])
            location_name = location.street if location.street else location.city
            
            case, created = Case.objects.get_or_create(
                case_number=f'2023-{i:03d}',
                defaults={
                    'title': f'{title_base} {location_name}',
                    'description': f'Historischer Fall aus 2023: {title_base} in {location.city}',
                    'case_type': case_type,
                    'status': status,
                    'priority': priority,
                    'location': location,
                    'incident_date': timezone.now() - timedelta(days=random.randint(365, 730)),
                    'created_by': admin_user,
                    'assigned_to': admin_user if random.choice([True, False]) else None
                }
            )
            cases.append(case)
            if created:
                self.stdout.write(f'Historischer Fall erstellt: {case}')
        
        # Personen mit Fällen verknüpfen (erweitert)
        involvements = [
            # Spezifische Verknüpfungen für die ersten Fälle
            (persons[0], cases[0], 'suspect'),
            (persons[1], cases[0], 'witness'),
            (persons[2], cases[1], 'victim'),
            (persons[3], cases[1], 'suspect'),
            (persons[4], cases[2], 'suspect'),
            (persons[5], cases[3], 'informant'),
            (persons[6], cases[4], 'witness'),
            (persons[7], cases[5], 'victim'),
            (persons[0], cases[6], 'suspect'),
            (persons[1], cases[7], 'witness'),
            (persons[2], cases[8], 'victim'),
            (persons[3], cases[9], 'suspect'),
            (persons[4], cases[10], 'informant'),
            (persons[5], cases[11], 'witness'),
            (persons[6], cases[12], 'victim'),
            (persons[7], cases[13], 'suspect'),
        ]
        
        # Zufällige Verknüpfungen für alle anderen Fälle
        involvement_types = ['suspect', 'victim', 'witness', 'informant', 'other']
        
        for case in cases[14:]:  # Für alle Fälle ab Index 14
            # Jeder Fall hat 1-4 beteiligte Personen
            num_involvements = random.randint(1, 4)
            selected_persons = random.sample(persons, min(num_involvements, len(persons)))
            
            for i, person in enumerate(selected_persons):
                # Erste Person ist oft Verdächtiger oder Opfer
                if i == 0:
                    involvement_type = random.choice(['suspect', 'victim'])
                else:
                    involvement_type = random.choice(involvement_types)
                
                involvements.append((person, case, involvement_type))
        
        for person, case, involvement_type in involvements:
            involvement, created = PersonInvolvement.objects.get_or_create(
                person=person,
                case=case,
                involvement_type=involvement_type,
                defaults={
                    'description': f'{person.full_name} als {involvement_type} in Fall {case.case_number}',
                    'credibility': random.randint(2, 5),
                    'created_by': admin_user
                }
            )
            if created:
                self.stdout.write(f'Fallbeteiligung erstellt: {involvement}')
        
        # Beweismittel erstellen (erweitert)
        evidence_data = [
            # Spezifische Beweismittel für die ersten Fälle
            (cases[0], 'BW-001', 'Fingerabdrücke', 'Fingerabdrücke am Fenster', 'physical'),
            (cases[1], 'BW-002', 'E-Mail-Verkehr', 'Betrügerische E-Mails', 'digital'),
            (cases[2], 'BW-003', 'Überwachungsvideos', 'Videoaufnahmen der Tat', 'video'),
            (cases[3], 'BW-004', 'Beschlagnahmte Substanzen', 'Verdächtige Pulver', 'physical'),
            (cases[4], 'BW-005', 'Handschrift-Analyse', 'Gefälschte Unterschriften', 'document'),
            (cases[5], 'BW-006', 'Audio-Aufnahme', 'Bedrohungsanruf', 'audio'),
            (cases[6], 'BW-007', 'DNA-Spuren', 'Biologische Spuren am Tatort', 'physical'),
            (cases[7], 'BW-008', 'Smartphone-Daten', 'Gelöschte Nachrichten', 'digital'),
            (cases[8], 'BW-009', 'Überwachungskamera', 'Aufnahmen vom Parkplatz', 'video'),
            (cases[9], 'BW-010', 'Werkzeuge', 'Einbruchswerkzeuge', 'physical'),
        ]
        
        # Automatische Beweismittel für alle anderen Fälle
        evidence_types = ['physical', 'digital', 'video', 'audio', 'document', 'photo']
        evidence_titles = {
            'physical': ['Fingerabdrücke', 'DNA-Spuren', 'Werkzeuge', 'Waffen', 'Kleidung', 'Substanzen'],
            'digital': ['E-Mail-Verkehr', 'Smartphone-Daten', 'Computer-Festplatte', 'USB-Stick', 'Chat-Protokolle'],
            'video': ['Überwachungsvideos', 'Dashcam-Aufnahmen', 'Handy-Videos', 'Sicherheitskamera'],
            'audio': ['Telefon-Mitschnitte', 'Bedrohungsanrufe', 'Zeugen-Interviews', 'Abhör-Aufnahmen'],
            'document': ['Gefälschte Dokumente', 'Handschrift-Analyse', 'Verträge', 'Rechnungen'],
            'photo': ['Tatort-Fotos', 'Beweisfotos', 'Überwachungsfotos', 'Verletzungsfotos']
        }
        
        evidence_counter = 11
        for case in cases[10:]:  # Für alle Fälle ab Index 10
            # Jeder Fall hat 1-3 Beweismittel
            num_evidence = random.randint(1, 3)
            
            for i in range(num_evidence):
                evidence_type = random.choice(evidence_types)
                title = random.choice(evidence_titles[evidence_type])
                
                evidence_data.append((
                    case,
                    f'BW-{evidence_counter:03d}',
                    title,
                    f'{title} zu Fall {case.case_number}',
                    evidence_type
                ))
                evidence_counter += 1
        
        for case, evidence_number, title, description, evidence_type in evidence_data:
            evidence, created = Evidence.objects.get_or_create(
                case=case,
                evidence_number=evidence_number,
                defaults={
                    'title': title,
                    'description': description,
                    'evidence_type': evidence_type,
                    'collected_date': timezone.now() - timedelta(days=random.randint(1, 60)),
                    'collected_by': admin_user
                }
            )
            if created:
                self.stdout.write(f'Beweismittel erstellt: {evidence}')
        
        # Timeline-Einträge erstellen (erweitert)
        timeline_data = [
            # Spezifische Timeline für die ersten Fälle
            (cases[0], timezone.now() - timedelta(days=5, hours=2), 'Einbruch gemeldet', 'Anruf bei der Polizei um 14:30 Uhr', persons[1], addresses[0]),
            (cases[0], timezone.now() - timedelta(days=4, hours=10), 'Tatort besichtigt', 'Spurensicherung vor Ort durchgeführt', None, addresses[0]),
            (cases[0], timezone.now() - timedelta(days=3, hours=16), 'Zeuge befragt', 'Ausführliches Gespräch mit Nachbarn', persons[1], None),
            (cases[0], timezone.now() - timedelta(days=2, hours=8), 'Verdächtiger identifiziert', 'Fingerabdrücke führen zu Verdächtigem', persons[0], None),
            
            (cases[1], timezone.now() - timedelta(days=7, hours=12), 'Betrugsanzeige eingegangen', 'Online-Betrug über E-Mail gemeldet', persons[2], None),
            (cases[1], timezone.now() - timedelta(days=6, hours=9), 'E-Mail-Verkehr analysiert', 'Digitale Spuren untersucht', None, None),
            (cases[1], timezone.now() - timedelta(days=5, hours=15), 'Verdächtiger ermittelt', 'IP-Adresse zurückverfolgt', persons[3], None),
            (cases[1], timezone.now() - timedelta(days=4, hours=11), 'Hausdurchsuchung', 'Computer und Dokumente sichergestellt', None, addresses[1]),
            
            (cases[2], timezone.now() - timedelta(days=3, hours=22), 'Schlägerei gemeldet', 'Notruf von Passanten erhalten', None, addresses[2]),
            (cases[2], timezone.now() - timedelta(days=3, hours=21), 'Polizei am Tatort', 'Erste Hilfe und Festnahme', persons[4], addresses[2]),
            (cases[2], timezone.now() - timedelta(days=2, hours=14), 'Vernehmung durchgeführt', 'Täter und Opfer befragt', persons[4], None),
            (cases[2], timezone.now() - timedelta(days=1, hours=10), 'Fall abgeschlossen', 'Anklage erhoben', None, None),
        ]
        
        # Automatische Timeline-Einträge für alle anderen aktiven Fälle
        timeline_events = [
            'Anzeige erstattet', 'Tatort besichtigt', 'Zeuge befragt', 'Verdächtiger vernommen',
            'Beweismittel sichergestellt', 'Hausdurchsuchung durchgeführt', 'Festnahme erfolgt',
            'Anklage erhoben', 'Verhandlung angesetzt', 'Fall abgeschlossen', 'Ermittlungen eingestellt',
            'Neue Spur verfolgt', 'Experte hinzugezogen', 'Gutachten erstellt', 'Phantombild erstellt',
            'Öffentlichkeitsfahndung', 'Belohnung ausgesetzt', 'Hinweise ausgewertet', 'Razzia durchgeführt',
            'Observierung begonnen', 'Abhörmaßnahmen', 'Datenauswertung', 'Spurensicherung'
        ]
        
        for case in cases[3:]:  # Für alle Fälle ab Index 3
            # Jeder Fall hat 2-6 Timeline-Einträge
            num_events = random.randint(2, 6)
            
            # Sortiere Events chronologisch
            event_times = sorted([
                timezone.now() - timedelta(days=random.randint(1, 180), hours=random.randint(0, 23))
                for _ in range(num_events)
            ])
            
            for i, event_time in enumerate(event_times):
                event_title = random.choice(timeline_events)
                related_person = random.choice(persons) if random.choice([True, False]) else None
                related_location = random.choice(addresses) if random.choice([True, False]) else None
                
                timeline_data.append((
                    case,
                    event_time,
                    event_title,
                    f'{event_title} zu Fall {case.case_number}',
                    related_person,
                    related_location
                ))
        
        for case, event_datetime, title, description, person, location in timeline_data:
            timeline, created = Timeline.objects.get_or_create(
                case=case,
                datetime=event_datetime,
                title=title,
                defaults={
                    'description': description,
                    'related_person': person,
                    'related_location': location,
                    'created_by': admin_user
                }
            )
            if created:
                self.stdout.write(f'Timeline-Eintrag erstellt: {timeline}')
        
        self.stdout.write(self.style.SUCCESS('Beispieldaten erfolgreich geladen!'))
