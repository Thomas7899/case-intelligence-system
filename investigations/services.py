# investigations/services.py
"""
Service-Layer für Investigation-bezogene Business Logic.
"""
from django.db.models import Count, Q, Prefetch
from django.utils import timezone
from datetime import timedelta
from .models import Case, PersonInvolvement, Evidence, Investigation, Timeline


class CaseAnalysisService:
    """
    Service für Fall-Analyse.
    """
    
    @staticmethod
    def get_case_with_related_data(case_id: int) -> Case:
        """
        Lädt Fall mit allen Relationen optimiert.
        """
        return Case.objects.select_related(
            'location', 'created_by', 'assigned_to'
        ).prefetch_related(
            Prefetch(
                'personinvolvement_set',
                queryset=PersonInvolvement.objects.select_related('person', 'created_by')
            ),
            Prefetch(
                'evidence',
                queryset=Evidence.objects.select_related('collected_by').order_by('-collected_date')
            ),
            Prefetch(
                'investigations',
                queryset=Investigation.objects.select_related('created_by', 'assigned_to').order_by('-created_at')
            ),
            Prefetch(
                'timeline',
                queryset=Timeline.objects.select_related('related_person', 'related_location').order_by('datetime')
            ),
            'involved_vehicles',
        ).get(id=case_id)
    
    @staticmethod
    def get_case_statistics() -> dict:
        """
        Generiert Dashboard-Statistiken.
        """
        total = Case.objects.count()
        by_status = dict(
            Case.objects.values('status').annotate(
                count=Count('id')
            ).values_list('status', 'count')
        )
        by_priority = dict(
            Case.objects.values('priority').annotate(
                count=Count('id')
            ).values_list('priority', 'count')
        )
        by_type = dict(
            Case.objects.values('case_type').annotate(
                count=Count('id')
            ).values_list('case_type', 'count')
        )
        
        # Trend letzte 30 Tage
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_count = Case.objects.filter(created_at__gte=thirty_days_ago).count()
        
        return {
            'total': total,
            'by_status': by_status,
            'by_priority': by_priority,
            'by_type': by_type,
            'recent_30_days': recent_count,
            'open_count': by_status.get('open', 0),
            'in_progress_count': by_status.get('in_progress', 0),
            'urgent_count': by_priority.get('urgent', 0),
        }
    
    @staticmethod
    def get_related_cases(case: Case) -> list:
        """
        Findet verwandte Fälle basierend auf gemeinsamen Beteiligten.
        """
        case_person_ids = PersonInvolvement.objects.filter(
            case=case
        ).values_list('person_id', flat=True)
        
        related = Case.objects.filter(
            personinvolvement__person_id__in=case_person_ids
        ).exclude(id=case.id).annotate(
            shared_persons=Count('personinvolvement', filter=Q(
                personinvolvement__person_id__in=case_person_ids
            ))
        ).filter(shared_persons__gt=0).distinct().order_by('-shared_persons')[:5]
        
        return list(related)


class TimelineAnalysisService:
    """
    Service für Timeline-basierte Analysen.
    """
    
    @staticmethod
    def get_timeline_gaps(case: Case, threshold_hours: int = 24) -> list:
        """
        Identifiziert Lücken in der Timeline eines Falls.
        Hilfreich für Ermittler.
        """
        entries = Timeline.objects.filter(case=case).order_by('datetime')
        gaps = []
        
        prev_entry = None
        for entry in entries:
            if prev_entry:
                diff = entry.datetime - prev_entry.datetime
                if diff > timedelta(hours=threshold_hours):
                    gaps.append({
                        'start': prev_entry.datetime,
                        'end': entry.datetime,
                        'duration_hours': diff.total_seconds() / 3600,
                        'before_event': prev_entry.title,
                        'after_event': entry.title,
                    })
            prev_entry = entry
        
        return gaps
    
    @staticmethod
    def get_person_timeline_across_cases(person_id: int) -> list:
        """
        Erstellt eine fallübergreifende Timeline für eine Person.
        """
        return Timeline.objects.filter(
            related_person_id=person_id
        ).select_related(
            'case', 'related_location'
        ).order_by('datetime')
    
    @staticmethod
    def detect_temporal_patterns(case_type: str = None) -> dict:
        """
        Erkennt zeitliche Muster (z.B. häufige Tageszeiten).
        """
        from django.db.models.functions import ExtractHour, ExtractWeekDay
        
        base_query = Timeline.objects.all()
        if case_type:
            base_query = base_query.filter(case__case_type=case_type)
        
        by_hour = dict(
            base_query.annotate(
                hour=ExtractHour('datetime')
            ).values('hour').annotate(
                count=Count('id')
            ).values_list('hour', 'count')
        )
        
        by_weekday = dict(
            base_query.annotate(
                weekday=ExtractWeekDay('datetime')
            ).values('weekday').annotate(
                count=Count('id')
            ).values_list('weekday', 'count')
        )
        
        return {
            'by_hour': by_hour,
            'by_weekday': by_weekday,
            'peak_hour': max(by_hour, key=by_hour.get) if by_hour else None,
            'peak_weekday': max(by_weekday, key=by_weekday.get) if by_weekday else None,
        }


class DashboardService:
    """
    Service für Dashboard-Daten.
    """
    
    @staticmethod
    def get_dashboard_data() -> dict:
        """
        Aggregiert alle Dashboard-relevanten Daten.
        """
        from entities.models import Person
        
        # Case-Statistiken
        case_stats = CaseAnalysisService.get_case_statistics()
        
        # Recent Cases (optimiert)
        recent_cases = Case.objects.select_related(
            'assigned_to', 'location'
        ).order_by('-created_at')[:5]
        
        # High-Risk Persons (optimiert)
        high_risk_persons = Person.objects.filter(
            risk_level__gte=3
        ).order_by('-risk_level')[:5]
        
        # Upcoming Investigations (optimiert)
        upcoming_investigations = Investigation.objects.filter(
            planned_date__gte=timezone.now(),
            completed_date__isnull=True
        ).select_related('case', 'assigned_to').order_by('planned_date')[:5]
        
        # Alert-würdige Items
        alerts = []
        
        # Überfällige Maßnahmen
        overdue = Investigation.objects.filter(
            planned_date__lt=timezone.now(),
            completed_date__isnull=True
        ).count()
        if overdue > 0:
            alerts.append({
                'type': 'warning',
                'message': f'{overdue} überfällige Ermittlungsmaßnahmen',
            })
        
        # Dringende offene Fälle
        urgent_open = Case.objects.filter(
            priority='urgent', status='open'
        ).count()
        if urgent_open > 0:
            alerts.append({
                'type': 'danger',
                'message': f'{urgent_open} dringende offene Fälle',
            })
        
        return {
            'stats': case_stats,
            'recent_cases': recent_cases,
            'high_risk_persons': high_risk_persons,
            'upcoming_investigations': upcoming_investigations,
            'alerts': alerts,
        }
