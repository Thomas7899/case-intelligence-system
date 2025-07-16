from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Case, PersonInvolvement, Evidence, Investigation, Timeline
from entities.models import Person, Address, Vehicle


@login_required
def dashboard(request):
    """
    Haupt-Dashboard mit Übersicht
    """
    # Statistiken
    total_cases = Case.objects.count()
    open_cases = Case.objects.filter(status='open').count()
    in_progress_cases = Case.objects.filter(status='in_progress').count()
    
    # Aktuelle Fälle
    recent_cases = Case.objects.order_by('-created_at')[:5]
    
    # Personen mit höchstem Risiko
    high_risk_persons = Person.objects.filter(risk_level__gte=3).order_by('-risk_level')[:5]
    
    # Kommende Ermittlungsmaßnahmen
    upcoming_investigations = Investigation.objects.filter(
        planned_date__gte=timezone.now(),
        completed_date__isnull=True
    ).order_by('planned_date')[:5]
    
    context = {
        'total_cases': total_cases,
        'open_cases': open_cases,
        'in_progress_cases': in_progress_cases,
        'recent_cases': recent_cases,
        'high_risk_persons': high_risk_persons,
        'upcoming_investigations': upcoming_investigations,
    }
    
    return render(request, 'investigations/dashboard.html', context)


@login_required
def case_list(request):
    """
    Liste aller Fälle mit Filterung
    """
    cases = Case.objects.all().order_by('-created_at')
    
    # Filter
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    search_query = request.GET.get('search')
    
    if status_filter:
        cases = cases.filter(status=status_filter)
    
    if priority_filter:
        cases = cases.filter(priority=priority_filter)
    
    if search_query:
        cases = cases.filter(
            Q(case_number__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Statistiken für das Dashboard
    stats = {
        'open_cases': Case.objects.filter(status='open').count(),
        'in_progress_cases': Case.objects.filter(status='in_progress').count(),
        'closed_cases': Case.objects.filter(status='closed').count(),
        'urgent_cases': Case.objects.filter(priority='urgent').count(),
    }
    
    context = {
        'cases': cases,
        'stats': stats,
        'current_status': status_filter,
        'current_priority': priority_filter,
        'search_query': search_query,
    }
    
    return render(request, 'investigations/case_list.html', context)


@login_required
def case_detail(request, case_id):
    """
    Detailansicht eines Falls
    """
    case = get_object_or_404(Case, id=case_id)
    
    # Beteiligte Personen
    involvements = PersonInvolvement.objects.filter(case=case).select_related('person')
    
    # Beweismittel
    evidence = Evidence.objects.filter(case=case).order_by('-collected_date')
    
    # Ermittlungsmaßnahmen
    investigations = Investigation.objects.filter(case=case).order_by('-created_at')
    
    # Zeitachse
    timeline = Timeline.objects.filter(case=case).order_by('datetime')
    
    context = {
        'case': case,
        'involvements': involvements,
        'evidence': evidence,
        'investigations': investigations,
        'timeline': timeline,
    }
    
    return render(request, 'investigations/case_detail.html', context)


@login_required
def case_create(request):
    """
    Neuen Fall erstellen
    """
    if request.method == 'POST':
        # Vereinfachte Erstellung - in Realität würde hier ein Form verwendet
        case_number = request.POST.get('case_number')
        title = request.POST.get('title')
        description = request.POST.get('description')
        case_type = request.POST.get('case_type')
        
        case = Case.objects.create(
            case_number=case_number,
            title=title,
            description=description,
            case_type=case_type,
            created_by=request.user
        )
        
        return redirect('case_detail', case_id=case.id)
    
    context = {
        'case_type_choices': Case.CASE_TYPE_CHOICES,
    }
    
    return render(request, 'investigations/case_create.html', context)


@login_required
def search(request):
    """
    Globale Suche über alle Entitäten
    """
    query = request.GET.get('q', '')
    results = {}
    
    if query:
        # Personen durchsuchen
        persons = Person.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(known_aliases__icontains=query)
        )
        
        # Fälle durchsuchen
        cases = Case.objects.filter(
            Q(case_number__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
        
        # Fahrzeuge durchsuchen
        vehicles = Vehicle.objects.filter(
            Q(license_plate__icontains=query) |
            Q(make__icontains=query) |
            Q(model__icontains=query)
        )
        
        # Adressen durchsuchen
        addresses = Address.objects.filter(
            Q(street__icontains=query) |
            Q(city__icontains=query) |
            Q(postal_code__icontains=query)
        )
        
        results = {
            'persons': persons,
            'cases': cases,
            'vehicles': vehicles,
            'addresses': addresses,
        }
    
    context = {
        'query': query,
        'results': results,
    }
    
    return render(request, 'investigations/search.html', context)


@login_required
def case_edit(request, case_id):
    """
    Fall bearbeiten
    """
    case = get_object_or_404(Case, id=case_id)
    
    if request.method == 'POST':
        # Vereinfachte Bearbeitung
        case.title = request.POST.get('title', case.title)
        case.description = request.POST.get('description', case.description)
        case.status = request.POST.get('status', case.status)
        case.priority = request.POST.get('priority', case.priority)
        case.case_type = request.POST.get('case_type', case.case_type)
        case.save()
        
        messages.success(request, f'Fall {case.case_number} wurde erfolgreich aktualisiert.')
        return redirect('case_detail', case_id=case.id)
    
    context = {
        'case': case,
        'case_type_choices': Case.CASE_TYPE_CHOICES,
    }
    
    return render(request, 'investigations/case_edit.html', context)


@login_required
def case_delete(request, case_id):
    """
    Fall löschen
    """
    case = get_object_or_404(Case, id=case_id)
    
    if request.method == 'POST':
        case_number = case.case_number
        case.delete()
        messages.success(request, f'Fall {case_number} wurde erfolgreich gelöscht.')
        return redirect('case_list')
    
    # Redirect to case list if not POST request
    return redirect('case_list')


@login_required
def timeline_add(request, case_id):
    """
    Zeitachse-Ereignis hinzufügen
    """
    case = get_object_or_404(Case, id=case_id)
    
    if request.method == 'POST':
        datetime_str = request.POST.get('datetime')
        title = request.POST.get('title')
        description = request.POST.get('description')
        related_person_id = request.POST.get('related_person')
        related_location_id = request.POST.get('related_location')
        
        # Parse datetime
        try:
            from django.utils.dateparse import parse_datetime
            datetime_obj = parse_datetime(datetime_str)
            if not datetime_obj:
                # Try parsing without timezone
                import datetime as dt
                datetime_obj = dt.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
                datetime_obj = timezone.make_aware(datetime_obj)
        except (ValueError, TypeError):
            messages.error(request, 'Ungültiges Datum/Zeit-Format.')
            return redirect('case_detail', case_id=case.id)
        
        # Create timeline entry
        timeline_entry = Timeline.objects.create(
            case=case,
            datetime=datetime_obj,
            title=title,
            description=description,
            created_by=request.user
        )
        
        # Add related person if provided
        if related_person_id:
            try:
                person = Person.objects.get(id=related_person_id)
                timeline_entry.related_person = person
                timeline_entry.save()
            except Person.DoesNotExist:
                pass
        
        # Add related location if provided
        if related_location_id:
            try:
                location = Address.objects.get(id=related_location_id)
                timeline_entry.related_location = location
                timeline_entry.save()
            except Address.DoesNotExist:
                pass
        
        messages.success(request, 'Zeitachse-Ereignis wurde erfolgreich hinzugefügt.')
        return redirect('case_detail', case_id=case.id)
    
    # Get available persons and locations for the form
    persons = Person.objects.all().order_by('last_name', 'first_name')
    locations = Address.objects.all().order_by('city', 'street')
    
    context = {
        'case': case,
        'persons': persons,
        'locations': locations,
    }
    
    return render(request, 'investigations/timeline_add.html', context)


@login_required
def timeline_edit(request, timeline_id):
    """
    Zeitachse-Ereignis bearbeiten
    """
    timeline_entry = get_object_or_404(Timeline, id=timeline_id)
    
    if request.method == 'POST':
        datetime_str = request.POST.get('datetime')
        title = request.POST.get('title')
        description = request.POST.get('description')
        related_person_id = request.POST.get('related_person')
        related_location_id = request.POST.get('related_location')
        
        # Parse datetime
        try:
            from django.utils.dateparse import parse_datetime
            datetime_obj = parse_datetime(datetime_str)
            if not datetime_obj:
                # Try parsing without timezone
                import datetime as dt
                datetime_obj = dt.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
                datetime_obj = timezone.make_aware(datetime_obj)
        except (ValueError, TypeError):
            messages.error(request, 'Ungültiges Datum/Zeit-Format.')
            return redirect('case_detail', case_id=timeline_entry.case.id)
        
        # Update timeline entry
        timeline_entry.datetime = datetime_obj
        timeline_entry.title = title
        timeline_entry.description = description
        
        # Update related person
        if related_person_id:
            try:
                person = Person.objects.get(id=related_person_id)
                timeline_entry.related_person = person
            except Person.DoesNotExist:
                timeline_entry.related_person = None
        else:
            timeline_entry.related_person = None
        
        # Update related location
        if related_location_id:
            try:
                location = Address.objects.get(id=related_location_id)
                timeline_entry.related_location = location
            except Address.DoesNotExist:
                timeline_entry.related_location = None
        else:
            timeline_entry.related_location = None
        
        timeline_entry.save()
        
        messages.success(request, 'Zeitachse-Ereignis wurde erfolgreich aktualisiert.')
        return redirect('case_detail', case_id=timeline_entry.case.id)
    
    # Get available persons and locations for the form
    persons = Person.objects.all().order_by('last_name', 'first_name')
    locations = Address.objects.all().order_by('city', 'street')
    
    context = {
        'timeline_entry': timeline_entry,
        'case': timeline_entry.case,
        'persons': persons,
        'locations': locations,
    }
    
    return render(request, 'investigations/timeline_edit.html', context)


@login_required
def timeline_delete(request, timeline_id):
    """
    Zeitachse-Ereignis löschen
    """
    timeline_entry = get_object_or_404(Timeline, id=timeline_id)
    case_id = timeline_entry.case.id
    
    if request.method == 'POST':
        timeline_entry.delete()
        messages.success(request, 'Zeitachse-Ereignis wurde erfolgreich gelöscht.')
    
    return redirect('case_detail', case_id=case_id)
