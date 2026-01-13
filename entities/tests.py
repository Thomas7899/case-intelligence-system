# entities/tests.py
"""
Unit- und Integration-Tests für die entities App.
Demonstriert Test-Kompetenz für Bewerbungen.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

from .models import Person, Address, Vehicle, PersonRelationship, PersonAddress
from .services import PersonAnalysisService, RelationshipGraphService


class PersonModelTest(TestCase):
    """Tests für das Person-Model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.person = Person.objects.create(
            first_name='Max',
            last_name='Mustermann',
            birth_date=date(1990, 5, 15),
            risk_level=2,
            created_by=self.user
        )
    
    def test_full_name_property(self):
        """Testet das full_name Property."""
        self.assertEqual(self.person.full_name, 'Max Mustermann')
    
    def test_age_calculation(self):
        """Testet die Altersberechnung."""
        age = self.person.age
        self.assertIsNotNone(age)
        self.assertGreaterEqual(age, 34)
    
    def test_age_none_without_birthdate(self):
        """Testet, dass age None ist ohne Geburtsdatum."""
        person = Person.objects.create(
            first_name='Test',
            last_name='Person',
            created_by=self.user
        )
        self.assertIsNone(person.age)
    
    def test_str_representation(self):
        """Testet die String-Darstellung."""
        self.assertEqual(str(self.person), 'Max Mustermann')
    
    def test_default_risk_level(self):
        """Testet den Default-Wert für risk_level."""
        person = Person.objects.create(
            first_name='Test',
            last_name='User',
            created_by=self.user
        )
        self.assertEqual(person.risk_level, 0)


class PersonRelationshipModelTest(TestCase):
    """Tests für Beziehungen zwischen Personen."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.person1 = Person.objects.create(
            first_name='Max', last_name='Mustermann', created_by=self.user
        )
        self.person2 = Person.objects.create(
            first_name='Anna', last_name='Schmidt', created_by=self.user
        )
    
    def test_relationship_creation(self):
        """Testet das Erstellen einer Beziehung."""
        rel = PersonRelationship.objects.create(
            person1=self.person1,
            person2=self.person2,
            relationship_type='friend',
            strength=3,
            created_by=self.user
        )
        self.assertEqual(rel.strength, 3)
        self.assertEqual(rel.relationship_type, 'friend')
    
    def test_relationship_str(self):
        """Testet die String-Darstellung der Beziehung."""
        rel = PersonRelationship.objects.create(
            person1=self.person1,
            person2=self.person2,
            relationship_type='colleague',
            created_by=self.user
        )
        self.assertIn('Kollege', str(rel))
    
    def test_unique_together_constraint(self):
        """Testet die Unique-Constraint für Beziehungen."""
        PersonRelationship.objects.create(
            person1=self.person1,
            person2=self.person2,
            relationship_type='friend',
            created_by=self.user
        )
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            PersonRelationship.objects.create(
                person1=self.person1,
                person2=self.person2,
                relationship_type='friend',
                created_by=self.user
            )


class PersonAnalysisServiceTest(TestCase):
    """Tests für den PersonAnalysisService."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.person = Person.objects.create(
            first_name='Test',
            last_name='Person',
            risk_level=3,
            created_by=self.user
        )
    
    def test_calculate_network_degree_no_connections(self):
        """Testet Netzwerk-Grad ohne Verbindungen."""
        metrics = PersonAnalysisService.calculate_network_degree(self.person)
        self.assertEqual(metrics['degree'], 0)
        self.assertFalse(metrics['is_hub'])
    
    def test_calculate_network_degree_with_connections(self):
        """Testet Netzwerk-Grad mit Verbindungen."""
        for i in range(4):
            other = Person.objects.create(
                first_name=f'Friend{i}',
                last_name='Test',
                created_by=self.user
            )
            PersonRelationship.objects.create(
                person1=self.person,
                person2=other,
                relationship_type='friend',
                created_by=self.user
            )
        
        metrics = PersonAnalysisService.calculate_network_degree(self.person)
        self.assertEqual(metrics['out_degree'], 4)
        self.assertTrue(metrics['is_hub'])
    
    def test_calculate_risk_score(self):
        """Testet die Risiko-Score-Berechnung."""
        score = PersonAnalysisService.calculate_risk_score(self.person)
        
        self.assertIn('total_score', score)
        self.assertIn('breakdown', score)
        self.assertIn('risk_category', score)
        self.assertEqual(score['breakdown']['base_risk'], 60)


class RelationshipGraphServiceTest(TestCase):
    """Tests für den RelationshipGraphService."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.person1 = Person.objects.create(
            first_name='Max', last_name='Test', created_by=self.user
        )
        self.person2 = Person.objects.create(
            first_name='Anna', last_name='Test', created_by=self.user
        )
        PersonRelationship.objects.create(
            person1=self.person1,
            person2=self.person2,
            relationship_type='friend',
            strength=3,
            created_by=self.user
        )
    
    def test_build_network_data_structure(self):
        """Testet die Struktur der Netzwerk-Daten."""
        data = RelationshipGraphService.build_network_data()
        
        self.assertIn('nodes', data)
        self.assertIn('edges', data)
        self.assertIn('stats', data)
    
    def test_build_network_data_content(self):
        """Testet den Inhalt der Netzwerk-Daten."""
        data = RelationshipGraphService.build_network_data()
        
        self.assertEqual(len(data['nodes']), 2)
        self.assertEqual(len(data['edges']), 1)
        
        node = data['nodes'][0]
        self.assertIn('id', node)
        self.assertIn('label', node)
        self.assertIn('risk_level', node)


class PersonViewTest(TestCase):
    """Integration-Tests für Person Views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.person = Person.objects.create(
            first_name='Max',
            last_name='Mustermann',
            created_by=self.user
        )
    
    def test_person_list_requires_login(self):
        """Testet, dass person_list Login erfordert."""
        response = self.client.get(reverse('entities:person_list'))
        self.assertEqual(response.status_code, 302)
    
    def test_person_list_authenticated(self):
        """Testet person_list für authentifizierte User."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('entities:person_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Max')
    
    def test_person_detail_authenticated(self):
        """Testet person_detail für authentifizierte User."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('entities:person_detail', kwargs={'person_id': self.person.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mustermann')
    
    def test_person_list_search(self):
        """Testet die Suchfunktion in person_list."""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(
            reverse('entities:person_list'), {'search': 'Max'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Max')
    
    def test_person_list_risk_filter(self):
        """Testet den Risikostufen-Filter."""
        self.client.login(username='testuser', password='testpass123')
        
        Person.objects.create(
            first_name='High',
            last_name='Risk',
            risk_level=4,
            created_by=self.user
        )
        
        response = self.client.get(
            reverse('entities:person_list'), {'risk_level': '4'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'High')
