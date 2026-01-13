# entities/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import JsonResponse
import json
from .models import Person, Address, Vehicle, PersonAddress, PersonRelationship
from investigations.models import PersonInvolvement, Case


@login_required
def person_list(request):
    """
    Liste aller Personen mit Filterung
    """
    persons = Person.objects.all().order_by('last_name', 'first_name')
    
    # Filter
    risk_level_filter = request.GET.get('risk_level')
    search_query = request.GET.get('search')
    
    if risk_level_filter:
        persons = persons.filter(risk_level=risk_level_filter)
    
    if search_query:
        persons = persons.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(known_aliases__icontains=search_query)
        )
    
    context = {
        'persons': persons,
        'risk_level_choices': Person.RISK_LEVEL_CHOICES,
        'current_risk_level': risk_level_filter,
        'search_query': search_query,
    }
    
    return render(request, 'entities/person_list.html', context)


@login_required
def person_detail(request, person_id):
    """
    Detailansicht einer Person
    """
    person = get_object_or_404(Person, id=person_id)
    
    # Adressen
    addresses = PersonAddress.objects.filter(person=person).select_related('address')
    
    # Fahrzeuge
    vehicles = Vehicle.objects.filter(owner=person)
    
    # Beziehungen
    relationships_from = PersonRelationship.objects.filter(person1=person).select_related('person2')
    relationships_to = PersonRelationship.objects.filter(person2=person).select_related('person1')
    
    # Fallbeteiligungen
    case_involvements = PersonInvolvement.objects.filter(person=person).select_related('case')
    
    context = {
        'person': person,
        'addresses': addresses,
        'vehicles': vehicles,
        'relationships_from': relationships_from,
        'relationships_to': relationships_to,
        'case_involvements': case_involvements,
    }
    
    return render(request, 'entities/person_detail.html', context)


@login_required
def person_create(request):
    """
    Neue Person erstellen
    """
    if request.method == 'POST':
        # Vereinfachte Erstellung - in Realität würde hier ein Form verwendet
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date') or None
        risk_level = request.POST.get('risk_level', 0)
        
        person = Person.objects.create(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            risk_level=risk_level,
            created_by=request.user
        )
        
        return redirect('person_detail', person_id=person.id)
    
    context = {
        'risk_level_choices': Person.RISK_LEVEL_CHOICES,
    }
    
    return render(request, 'entities/person_create.html', context)


@login_required
def address_list(request):
    """
    Liste aller Adressen
    """
    addresses = Address.objects.all().order_by('city', 'street')
    
    # Filter
    city_filter = request.GET.get('city')
    search_query = request.GET.get('search')
    
    if city_filter:
        addresses = addresses.filter(city=city_filter)
    
    if search_query:
        addresses = addresses.filter(
            Q(street__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(postal_code__icontains=search_query)
        )
    
    # Verfügbare Städte für Filter
    cities = Address.objects.values_list('city', flat=True).distinct().order_by('city')
    
    context = {
        'addresses': addresses,
        'cities': cities,
        'current_city': city_filter,
        'search_query': search_query,
    }
    
    return render(request, 'entities/address_list.html', context)


@login_required
def vehicle_list(request):
    """
    Liste aller Fahrzeuge
    """
    vehicles = Vehicle.objects.all().select_related('owner').order_by('license_plate')
    
    # Filter
    vehicle_type_filter = request.GET.get('vehicle_type')
    search_query = request.GET.get('search')
    
    if vehicle_type_filter:
        vehicles = vehicles.filter(vehicle_type=vehicle_type_filter)
    
    if search_query:
        vehicles = vehicles.filter(
            Q(license_plate__icontains=search_query) |
            Q(make__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(owner__first_name__icontains=search_query) |
            Q(owner__last_name__icontains=search_query)
        )
    
    context = {
        'vehicles': vehicles,
        'vehicle_type_choices': Vehicle.VEHICLE_TYPE_CHOICES,
        'current_vehicle_type': vehicle_type_filter,
        'search_query': search_query,
    }
    
    return render(request, 'entities/vehicle_list.html', context)


@login_required
def relationship_graph(request):
    """
    Erweiterte Beziehungsanalyse mit Fall-übergreifenden Funktionen
    """
    # Filter-Parameter
    case_id = request.GET.get('case')
    case_type = request.GET.get('case_type')
    risk_level = request.GET.get('risk_level')
    analysis_mode = request.GET.get('mode', 'all')  # 'all', 'case', 'cross_case'
    
    # Basis-Queries
    relationships = PersonRelationship.objects.all().select_related('person1', 'person2')
    persons = Person.objects.all()
    
    # Fall-spezifische Filterung
    if case_id:
        # Nur Personen aus diesem Fall
        case_persons = PersonInvolvement.objects.filter(case_id=case_id).values_list('person_id', flat=True)
        persons = persons.filter(id__in=case_persons)
        relationships = relationships.filter(
            person1__id__in=case_persons,
            person2__id__in=case_persons
        )
    elif case_type:
        # Personen aus Fällen eines bestimmten Typs
        case_persons = PersonInvolvement.objects.filter(case__case_type=case_type).values_list('person_id', flat=True)
        persons = persons.filter(id__in=case_persons)
        relationships = relationships.filter(
            person1__id__in=case_persons,
            person2__id__in=case_persons
        )
    
    # Risikostufen-Filter
    if risk_level:
        persons = persons.filter(risk_level__gte=risk_level)
        relationships = relationships.filter(
            person1__risk_level__gte=risk_level,
            person2__risk_level__gte=risk_level
        )
    
    # Erweiterte Analyse-Modi
    if analysis_mode == 'cross_case':
        # Personen, die in mehreren Fällen vorkommen
        multi_case_persons = PersonInvolvement.objects.values('person_id').annotate(
            case_count=Count('case_id')
        ).filter(case_count__gt=1).values_list('person_id', flat=True)
        
        persons = persons.filter(id__in=multi_case_persons)
        relationships = relationships.filter(
            person1__id__in=multi_case_persons,
            person2__id__in=multi_case_persons
        )
    
    # Nodes (Personen) mit erweiterten Informationen
    nodes = []
    for person in persons:
        # Fall-Beteiligungen zählen
        case_involvements = PersonInvolvement.objects.filter(person=person)
        case_count = case_involvements.count()
        
        # Rollen sammeln
        roles = list(case_involvements.values_list('involvement_type', flat=True).distinct())
        
        # Fälle nach Typ
        case_types = list(case_involvements.values_list('case__case_type', flat=True).distinct())
        
        node = {
            'id': person.id,
            'label': person.full_name,
            'risk_level': person.risk_level,
            'url': f'/entities/persons/{person.id}/',
            'case_count': case_count,
            'roles': roles,
            'case_types': case_types,
            'size': min(10 + case_count * 2, 30),  # Dynamische Größe
        }
        nodes.append(node)
    
    # Edges (Beziehungen) mit erweiterten Informationen
    edges = []
    for rel in relationships:
        # Gemeinsame Fälle finden
        person1_cases = set(PersonInvolvement.objects.filter(person=rel.person1).values_list('case_id', flat=True))
        person2_cases = set(PersonInvolvement.objects.filter(person=rel.person2).values_list('case_id', flat=True))
        common_cases = person1_cases.intersection(person2_cases)
        
        edge = {
            'from': rel.person1.id,
            'to': rel.person2.id,
            'label': rel.get_relationship_type_display(),
            'strength': rel.strength,
            'type': rel.relationship_type,
            'common_cases': len(common_cases),
            'width': max(1, rel.strength),
        }
        edges.append(edge)
    
    # Verfügbare Fälle für Dropdown
    available_cases = Case.objects.all().order_by('-created_at')
    
    # Fall-übergreifende Statistiken
    cross_case_stats = {
        'total_persons': persons.count(),
        'total_relationships': relationships.count(),
        'multi_case_persons': PersonInvolvement.objects.values('person_id').annotate(
            case_count=Count('case_id')
        ).filter(case_count__gt=1).count(),
        'high_risk_persons': persons.filter(risk_level__gte=3).count(),
    }
    
    # Als JSON für Frontend
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            'nodes': nodes,
            'edges': edges,
            'stats': cross_case_stats
        })
    
    context = {
        'nodes': nodes,
        'edges': edges,
        'persons': persons,
        'relationships': relationships,
        'available_cases': available_cases,
        'case_type_choices': Case.CASE_TYPE_CHOICES,
        'risk_level_choices': Person.RISK_LEVEL_CHOICES,
        'nodes_json': json.dumps(nodes),
        'edges_json': json.dumps(edges),
        'stats': cross_case_stats,
        'current_case': case_id,
        'current_case_type': case_type,
        'current_risk_level': risk_level,
        'analysis_mode': analysis_mode,
    }
    
    return render(request, 'entities/relationship_graph.html', context)


@login_required
def cross_case_analysis(request):
    """
    Spezielle Fall-übergreifende Analyse-View
    """
    # Personen, die in mehreren Fällen vorkommen
    multi_case_persons = PersonInvolvement.objects.values('person').annotate(
        case_count=Count('case_id', distinct=True),
        roles=Count('involvement_type', distinct=True)
    ).filter(case_count__gt=1).order_by('-case_count')
    
    # Detaillierte Informationen zu diesen Personen
    person_analysis = []
    for involvement in multi_case_persons:
        person = Person.objects.get(id=involvement['person'])
        cases = PersonInvolvement.objects.filter(person=person).select_related('case')
        
        # Rollen und Falltypen sammeln
        roles = list(cases.values_list('involvement_type', flat=True).distinct())
        case_types = list(cases.values_list('case__case_type', flat=True).distinct())
        
        # Zeitspanne der Aktivität
        case_dates = cases.values_list('case__incident_date', flat=True)
        date_range = {
            'earliest': min(case_dates) if case_dates else None,
            'latest': max(case_dates) if case_dates else None
        }
        
        person_analysis.append({
            'person': person,
            'case_count': involvement['case_count'],
            'roles': roles,
            'case_types': case_types,
            'cases': cases,
            'date_range': date_range
        })
    
    # Netzwerk-Hotspots (Personen mit vielen Verbindungen)
    network_hubs = Person.objects.annotate(
        relationship_count=Count('relationships_from') + Count('relationships_to')
    ).filter(relationship_count__gt=2).order_by('-relationship_count')
    
    # Fall-Cluster (Fälle mit gemeinsamen Beteiligten)
    case_clusters = []
    processed_cases = set()
    
    for case in Case.objects.all():
        if case.id in processed_cases:
            continue
            
        # Andere Fälle mit gemeinsamen Beteiligten finden
        case_persons = set(PersonInvolvement.objects.filter(case=case).values_list('person_id', flat=True))
        
        related_cases = []
        for other_case in Case.objects.exclude(id=case.id):
            if other_case.id in processed_cases:
                continue
                
            other_persons = set(PersonInvolvement.objects.filter(case=other_case).values_list('person_id', flat=True))
            common_persons = case_persons.intersection(other_persons)
            
            if common_persons:
                related_cases.append({
                    'case': other_case,
                    'common_persons': len(common_persons),
                    'common_person_ids': common_persons
                })
        
        if related_cases:
            case_clusters.append({
                'main_case': case,
                'related_cases': related_cases,
                'total_persons': len(case_persons)
            })
            processed_cases.add(case.id)
            for rc in related_cases:
                processed_cases.add(rc['case'].id)
    
    context = {
        'person_analysis': person_analysis,
        'network_hubs': network_hubs,
        'case_clusters': case_clusters,
        'total_multi_case_persons': len(multi_case_persons),
        'total_network_hubs': network_hubs.count(),
        'total_case_clusters': len(case_clusters),
    }
    
    return render(request, 'entities/cross_case_analysis.html', context)
