# entities/services.py
"""
Service-Layer für Entity-bezogene Business Logic.
Trennt Logik von Views für bessere Testbarkeit und Wartbarkeit.
"""
from django.db.models import Count, Q, Prefetch
from .models import Person, PersonRelationship, PersonAddress
from investigations.models import PersonInvolvement, Case


class PersonAnalysisService:
    """
    Service für Personen-Analyse und Netzwerk-Metriken.
    """
    
    @staticmethod
    def get_person_with_related_data(person_id: int) -> Person:
        """
        Lädt Person mit allen relevanten Relationen in einer Query.
        Vermeidet N+1 Queries.
        """
        return Person.objects.select_related('created_by').prefetch_related(
            Prefetch(
                'personaddress_set',
                queryset=PersonAddress.objects.select_related('address')
            ),
            Prefetch(
                'vehicle_set'
            ),
            Prefetch(
                'relationships_from',
                queryset=PersonRelationship.objects.select_related('person2')
            ),
            Prefetch(
                'relationships_to',
                queryset=PersonRelationship.objects.select_related('person1')
            ),
            Prefetch(
                'personinvolvement_set',
                queryset=PersonInvolvement.objects.select_related('case')
            )
        ).get(id=person_id)
    
    @staticmethod
    def calculate_network_degree(person: Person) -> dict:
        """
        Berechnet Netzwerk-Metriken für eine Person.
        
        Returns:
            dict mit degree (Anzahl Verbindungen), 
            in_degree, out_degree, case_count
        """
        out_degree = PersonRelationship.objects.filter(person1=person).count()
        in_degree = PersonRelationship.objects.filter(person2=person).count()
        case_count = PersonInvolvement.objects.filter(person=person).values('case').distinct().count()
        
        return {
            'degree': out_degree + in_degree,
            'out_degree': out_degree,
            'in_degree': in_degree,
            'case_count': case_count,
            'is_hub': (out_degree + in_degree) >= 3,  # Threshold für "Hub"
        }
    
    @staticmethod
    def get_network_hubs(min_connections: int = 3) -> list:
        """
        Identifiziert Netzwerk-Hubs (Personen mit vielen Verbindungen).
        """
        return Person.objects.annotate(
            connection_count=Count('relationships_from', distinct=True) + 
                           Count('relationships_to', distinct=True),
            case_involvement_count=Count('personinvolvement', distinct=True)
        ).filter(
            connection_count__gte=min_connections
        ).order_by('-connection_count')
    
    @staticmethod
    def get_multi_case_persons() -> list:
        """
        Findet Personen, die in mehreren Fällen vorkommen.
        Wichtig für Cross-Case-Analyse.
        """
        return Person.objects.annotate(
            case_count=Count('personinvolvement__case', distinct=True)
        ).filter(case_count__gt=1).order_by('-case_count')
    
    @staticmethod
    def calculate_risk_score(person: Person) -> dict:
        """
        Berechnet erweiterten Risiko-Score basierend auf mehreren Faktoren.
        
        Faktoren:
        - Basis-Risikostufe
        - Anzahl Case-Beteiligungen
        - Rolle in Fällen (Verdächtiger = höher)
        - Netzwerk-Zentralität
        """
        involvements = PersonInvolvement.objects.filter(person=person)
        
        # Basis-Score aus Risikostufe (0-4)
        base_score = person.risk_level * 20  # Max 80
        
        # Case-Involvement-Score
        case_count = involvements.count()
        case_score = min(case_count * 5, 30)  # Max 30
        
        # Rollen-Score (Verdächtiger erhöht Score)
        suspect_count = involvements.filter(involvement_type='suspect').count()
        role_score = suspect_count * 10  # Max unbegrenzt, aber typisch 10-30
        
        # Netzwerk-Score
        network_metrics = PersonAnalysisService.calculate_network_degree(person)
        network_score = min(network_metrics['degree'] * 3, 20)  # Max 20
        
        total_score = min(base_score + case_score + role_score + network_score, 100)
        
        return {
            'total_score': total_score,
            'breakdown': {
                'base_risk': base_score,
                'case_involvement': case_score,
                'role_factor': role_score,
                'network_centrality': network_score,
            },
            'risk_category': (
                'critical' if total_score >= 80 else
                'high' if total_score >= 60 else
                'medium' if total_score >= 40 else
                'low' if total_score >= 20 else
                'minimal'
            )
        }


class RelationshipGraphService:
    """
    Service für Beziehungs-Graphen und Netzwerk-Visualisierung.
    """
    
    @staticmethod
    def build_network_data(
        case_id: int = None,
        case_type: str = None,
        min_risk_level: int = None,
        analysis_mode: str = 'all'
    ) -> dict:
        """
        Baut Netzwerk-Daten für Visualisierung.
        Optimiert mit prefetch_related.
        
        Args:
            case_id: Optional - Filter nach spezifischem Fall
            case_type: Optional - Filter nach Falltyp
            min_risk_level: Optional - Minimum Risikostufe
            analysis_mode: 'all', 'case', 'cross_case'
            
        Returns:
            dict mit 'nodes', 'edges', 'stats'
        """
        # Basis-Queryset mit Optimierung
        persons = Person.objects.all()
        relationships = PersonRelationship.objects.select_related(
            'person1', 'person2'
        )
        
        # Filter anwenden
        person_ids = None
        
        if case_id:
            person_ids = PersonInvolvement.objects.filter(
                case_id=case_id
            ).values_list('person_id', flat=True)
        elif case_type:
            person_ids = PersonInvolvement.objects.filter(
                case__case_type=case_type
            ).values_list('person_id', flat=True)
        elif analysis_mode == 'cross_case':
            # Multi-Case-Personen
            person_ids = Person.objects.annotate(
                case_count=Count('personinvolvement__case', distinct=True)
            ).filter(case_count__gt=1).values_list('id', flat=True)
        
        if person_ids is not None:
            persons = persons.filter(id__in=person_ids)
            relationships = relationships.filter(
                person1_id__in=person_ids,
                person2_id__in=person_ids
            )
        
        if min_risk_level:
            persons = persons.filter(risk_level__gte=min_risk_level)
            relationships = relationships.filter(
                person1__risk_level__gte=min_risk_level,
                person2__risk_level__gte=min_risk_level
            )
        
        # Prefetch für Performance
        persons = persons.prefetch_related(
            Prefetch(
                'personinvolvement_set',
                queryset=PersonInvolvement.objects.select_related('case')
            )
        )
        
        # Nodes bauen
        nodes = []
        for person in persons:
            involvements = person.personinvolvement_set.all()
            case_count = len(set(inv.case_id for inv in involvements))
            roles = list(set(inv.involvement_type for inv in involvements))
            case_types = list(set(inv.case.case_type for inv in involvements))
            
            nodes.append({
                'id': person.id,
                'label': person.full_name,
                'risk_level': person.risk_level,
                'url': f'/entities/persons/{person.id}/',
                'case_count': case_count,
                'roles': roles,
                'case_types': case_types,
                'size': min(10 + case_count * 2, 30),
            })
        
        # Edges bauen
        edges = []
        person_case_map = {
            p.id: set(inv.case_id for inv in p.personinvolvement_set.all())
            for p in persons
        }
        
        for rel in relationships:
            common_cases = person_case_map.get(rel.person1_id, set()) & \
                          person_case_map.get(rel.person2_id, set())
            
            edges.append({
                'from': rel.person1_id,
                'to': rel.person2_id,
                'label': rel.get_relationship_type_display(),
                'strength': rel.strength,
                'type': rel.relationship_type,
                'common_cases': len(common_cases),
                'width': max(1, rel.strength),
            })
        
        # Statistiken
        stats = {
            'total_persons': len(nodes),
            'total_relationships': len(edges),
            'multi_case_persons': sum(1 for n in nodes if n['case_count'] > 1),
            'high_risk_persons': sum(1 for n in nodes if n['risk_level'] >= 3),
        }
        
        return {
            'nodes': nodes,
            'edges': edges,
            'stats': stats,
        }


class CrossCaseAnalysisService:
    """
    Service für fall-übergreifende Analyse.
    """
    
    @staticmethod
    def find_case_clusters() -> list:
        """
        Findet Cluster von Fällen mit gemeinsamen Beteiligten.
        """
        cases = Case.objects.prefetch_related(
            Prefetch(
                'personinvolvement_set',
                queryset=PersonInvolvement.objects.select_related('person')
            )
        )
        
        clusters = []
        processed = set()
        
        for case in cases:
            if case.id in processed:
                continue
            
            case_persons = {inv.person_id for inv in case.personinvolvement_set.all()}
            related = []
            
            for other in cases:
                if other.id == case.id or other.id in processed:
                    continue
                
                other_persons = {inv.person_id for inv in other.personinvolvement_set.all()}
                common = case_persons & other_persons
                
                if common:
                    related.append({
                        'case': other,
                        'common_persons': len(common),
                        'common_person_ids': list(common),
                    })
            
            if related:
                clusters.append({
                    'main_case': case,
                    'related_cases': related,
                    'total_persons': len(case_persons),
                })
                processed.add(case.id)
                for r in related:
                    processed.add(r['case'].id)
        
        return clusters
    
    @staticmethod
    def get_pattern_analysis() -> dict:
        """
        Identifiziert Muster in den Daten.
        """
        # Zeitliche Muster
        from django.db.models.functions import TruncMonth
        
        monthly_cases = Case.objects.annotate(
            month=TruncMonth('incident_date')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        # Häufigste Falltypen
        case_type_stats = Case.objects.values('case_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Rückfällige Personen (in >2 Fällen als Verdächtige)
        repeat_suspects = PersonInvolvement.objects.filter(
            involvement_type='suspect'
        ).values('person').annotate(
            case_count=Count('case', distinct=True)
        ).filter(case_count__gt=1).count()
        
        return {
            'monthly_trend': list(monthly_cases),
            'case_type_distribution': list(case_type_stats),
            'repeat_suspect_count': repeat_suspects,
        }
