# investigations/tests.py
"""
Unit- und Integration-Tests für die investigations App.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Case, PersonInvolvement, Evidence, Timeline
from .services import CaseAnalysisService, TimelineAnalysisService, DashboardService
from entities.models import Person


class CaseModelTest(TestCase):
    """Tests für das Case-Model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.case = Case.objects.create(
            case_number='2024-TEST-001',
            title='Test Case',
            description='Test Description',
            case_type='theft',
            status='open',
            priority='medium',
            created_by=self.user
        )
    
    def test_case_str_representation(self):
        """Testet die String-Darstellung."""
        self.assertEqual(str(self.case), '2024-TEST-001 - Test Case')
    
    def test_case_default_status(self):
        """Testet den Default-Status."""
        case = Case.objects.create(
            case_number='2024-TEST-002',
            title='Another Case',
            description='Description',
            case_type='fraud',
            created_by=self.user
        )
        self.assertEqual(case.status, 'open')
    
    def test_case_number_unique(self):
        """Testet die Einzigartigkeit der Fallnummer."""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Case.objects.create(
                case_number='2024-TEST-001',
                title='Duplicate Case',
                description='Description',
                case_type='fraud',
                created_by=self.user
            )


class PersonInvolvementTest(TestCase):
    """Tests für PersonInvolvement (Through-Model)."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.person = Person.objects.create(
            first_name='Test',
            last_name='Person',
            created_by=self.user
        )
        self.case = Case.objects.create(
            case_number='2024-TEST-001',
            title='Test Case',
            description='Description',
            case_type='theft',
            created_by=self.user
        )
    
    def test_involvement_creation(self):
        """Testet das Erstellen einer Beteiligung."""
        involvement = PersonInvolvement.objects.create(
            person=self.person,
            case=self.case,
            involvement_type='suspect',
            credibility=2,
            created_by=self.user
        )
        self.assertEqual(involvement.involvement_type, 'suspect')
        self.assertEqual(involvement.credibility, 2)
    
    def test_involvement_str(self):
        """Testet die String-Darstellung."""
        involvement = PersonInvolvement.objects.create(
            person=self.person,
            case=self.case,
            involvement_type='witness',
            created_by=self.user
        )
        self.assertIn('Zeuge', str(involvement))


class CaseAnalysisServiceTest(TestCase):
    """Tests für den CaseAnalysisService."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        for i in range(5):
            Case.objects.create(
                case_number=f'2024-TEST-{i:03d}',
                title=f'Test Case {i}',
                description='Description',
                case_type='theft' if i % 2 == 0 else 'fraud',
                status='open' if i < 3 else 'closed',
                priority='urgent' if i == 0 else 'medium',
                created_by=self.user
            )
    
    def test_get_case_statistics_total(self):
        """Testet die Gesamtstatistik."""
        stats = CaseAnalysisService.get_case_statistics()
        self.assertEqual(stats['total'], 5)
    
    def test_get_case_statistics_by_status(self):
        """Testet Statistiken nach Status."""
        stats = CaseAnalysisService.get_case_statistics()
        self.assertEqual(stats['open_count'], 3)
    
    def test_get_case_statistics_urgent(self):
        """Testet Zählung dringender Fälle."""
        stats = CaseAnalysisService.get_case_statistics()
        self.assertEqual(stats['urgent_count'], 1)


class TimelineAnalysisServiceTest(TestCase):
    """Tests für TimelineAnalysisService."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.case = Case.objects.create(
            case_number='2024-TEST-001',
            title='Test Case',
            description='Description',
            case_type='theft',
            created_by=self.user
        )
    
    def test_get_timeline_gaps_no_gaps(self):
        """Testet Timeline ohne Lücken."""
        now = timezone.now()
        for i in range(3):
            Timeline.objects.create(
                case=self.case,
                datetime=now + timedelta(hours=i * 2),
                title=f'Event {i}',
                description='Description',
                created_by=self.user
            )
        
        gaps = TimelineAnalysisService.get_timeline_gaps(self.case)
        self.assertEqual(len(gaps), 0)
    
    def test_get_timeline_gaps_with_gap(self):
        """Testet Timeline mit Lücke."""
        now = timezone.now()
        Timeline.objects.create(
            case=self.case,
            datetime=now,
            title='Event 1',
            description='Description',
            created_by=self.user
        )
        Timeline.objects.create(
            case=self.case,
            datetime=now + timedelta(hours=48),
            title='Event 2',
            description='Description',
            created_by=self.user
        )
        
        gaps = TimelineAnalysisService.get_timeline_gaps(self.case, threshold_hours=24)
        self.assertEqual(len(gaps), 1)
        self.assertGreater(gaps[0]['duration_hours'], 24)


class DashboardServiceTest(TestCase):
    """Tests für DashboardService."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
    
    def test_get_dashboard_data_structure(self):
        """Testet die Struktur der Dashboard-Daten."""
        data = DashboardService.get_dashboard_data()
        
        self.assertIn('stats', data)
        self.assertIn('recent_cases', data)
        self.assertIn('high_risk_persons', data)
        self.assertIn('alerts', data)


class CaseViewTest(TestCase):
    """Integration-Tests für Case Views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.case = Case.objects.create(
            case_number='2024-TEST-001',
            title='Test Case',
            description='Test Description',
            case_type='theft',
            created_by=self.user
        )
    
    def test_dashboard_requires_login(self):
        """Testet, dass Dashboard Login erfordert."""
        response = self.client.get(reverse('investigations:dashboard'))
        self.assertEqual(response.status_code, 302)
    
    def test_dashboard_authenticated(self):
        """Testet Dashboard für authentifizierte User."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('investigations:dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_case_list_authenticated(self):
        """Testet case_list für authentifizierte User."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('investigations:case_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Case')
    
    def test_case_detail_authenticated(self):
        """Testet case_detail für authentifizierte User."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('investigations:case_detail', kwargs={'case_id': self.case.id})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_search_functionality(self):
        """Testet die globale Suchfunktion."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('investigations:search'), {'q': 'Test Case'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Case')
    
    def test_case_filter_by_status(self):
        """Testet Status-Filter."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('investigations:case_list'), {'status': 'open'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Case')
