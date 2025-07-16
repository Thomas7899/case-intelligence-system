from django.db import models
from django.contrib.auth.models import User
from entities.models import Person, Address, Vehicle


class Case(models.Model):
    """
    Ermittlungsfall
    """
    CASE_STATUS_CHOICES = [
        ('open', 'Offen'),
        ('in_progress', 'In Bearbeitung'),
        ('closed', 'Abgeschlossen'),
        ('suspended', 'Ausgesetzt'),
    ]
    
    CASE_TYPE_CHOICES = [
        ('theft', 'Diebstahl'),
        ('fraud', 'Betrug'),
        ('assault', 'Körperverletzung'),
        ('drug', 'Drogen'),
        ('traffic', 'Verkehr'),
        ('domestic', 'Häusliche Gewalt'),
        ('other', 'Sonstiges'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Niedrig'),
        ('medium', 'Mittel'),
        ('high', 'Hoch'),
        ('urgent', 'Dringend'),
    ]
    
    case_number = models.CharField(max_length=50, unique=True, verbose_name="Aktenzeichen")
    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    
    case_type = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES, verbose_name="Falltyp")
    status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES, default='open', verbose_name="Status")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Priorität")
    
    # Zeitdaten
    incident_date = models.DateTimeField(null=True, blank=True, verbose_name="Tatzeitpunkt")
    reported_date = models.DateTimeField(auto_now_add=True, verbose_name="Gemeldet am")
    
    # Verknüpfungen
    involved_persons = models.ManyToManyField(Person, through='PersonInvolvement', verbose_name="Beteiligte Personen")
    location = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tatort")
    involved_vehicles = models.ManyToManyField(Vehicle, blank=True, verbose_name="Beteiligte Fahrzeuge")
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Erstellt von")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='assigned_cases', verbose_name="Zugewiesen an")
    
    def __str__(self):
        return f"{self.case_number} - {self.title}"
    
    class Meta:
        verbose_name = "Fall"
        verbose_name_plural = "Fälle"
        ordering = ['-created_at']


class PersonInvolvement(models.Model):
    """
    Verknüpfung zwischen Person und Fall mit Rolle
    """
    INVOLVEMENT_TYPE_CHOICES = [
        ('suspect', 'Verdächtiger'),
        ('victim', 'Opfer'),
        ('witness', 'Zeuge'),
        ('informant', 'Informant'),
        ('other', 'Sonstiges'),
    ]
    
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Person")
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name="Fall")
    involvement_type = models.CharField(max_length=20, choices=INVOLVEMENT_TYPE_CHOICES, verbose_name="Rolle")
    
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    credibility = models.IntegerField(default=3, verbose_name="Glaubwürdigkeit (1-5)")
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Erstellt von")
    
    def __str__(self):
        return f"{self.person.full_name} - {self.get_involvement_type_display()} in {self.case.case_number}"
    
    class Meta:
        verbose_name = "Person-Fall-Beteiligung"
        verbose_name_plural = "Person-Fall-Beteiligungen"
        unique_together = ['person', 'case', 'involvement_type']


class Evidence(models.Model):
    """
    Beweismittel
    """
    EVIDENCE_TYPE_CHOICES = [
        ('document', 'Dokument'),
        ('photo', 'Foto'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('physical', 'Physisches Objekt'),
        ('digital', 'Digitale Spur'),
        ('other', 'Sonstiges'),
    ]
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='evidence', verbose_name="Fall")
    evidence_number = models.CharField(max_length=50, verbose_name="Beweis-Nr.")
    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    
    evidence_type = models.CharField(max_length=20, choices=EVIDENCE_TYPE_CHOICES, verbose_name="Beweistyp")
    location_found = models.CharField(max_length=200, null=True, blank=True, verbose_name="Fundort")
    
    # Datei-Upload (optional)
    file = models.FileField(upload_to='evidence/', null=True, blank=True, verbose_name="Datei")
    
    # Kette der Verwahrung
    chain_of_custody = models.TextField(blank=True, verbose_name="Verwahrungskette")
    
    # Metadaten
    collected_date = models.DateTimeField(null=True, blank=True, verbose_name="Sichergestellt am")
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Sichergestellt von")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    
    def __str__(self):
        return f"{self.evidence_number} - {self.title}"
    
    class Meta:
        verbose_name = "Beweismittel"
        verbose_name_plural = "Beweismittel"
        ordering = ['-collected_date']


class Investigation(models.Model):
    """
    Ermittlungsmaßnahme
    """
    INVESTIGATION_TYPE_CHOICES = [
        ('interview', 'Vernehmung'),
        ('search', 'Durchsuchung'),
        ('surveillance', 'Überwachung'),
        ('analysis', 'Analyse'),
        ('forensic', 'Forensische Untersuchung'),
        ('other', 'Sonstiges'),
    ]
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='investigations', verbose_name="Fall")
    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    
    investigation_type = models.CharField(max_length=20, choices=INVESTIGATION_TYPE_CHOICES, verbose_name="Maßnahmentyp")
    
    # Beteiligte Personen
    target_persons = models.ManyToManyField(Person, blank=True, verbose_name="Zielpersonen")
    
    # Zeitdaten
    planned_date = models.DateTimeField(null=True, blank=True, verbose_name="Geplant für")
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name="Durchgeführt am")
    
    # Ergebnis
    result = models.TextField(blank=True, verbose_name="Ergebnis")
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Erstellt von")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='assigned_investigations', verbose_name="Zugewiesen an")
    
    def __str__(self):
        return f"{self.title} - {self.case.case_number}"
    
    class Meta:
        verbose_name = "Ermittlungsmaßnahme"
        verbose_name_plural = "Ermittlungsmaßnahmen"
        ordering = ['-created_at']


class Timeline(models.Model):
    """
    Zeitachse für Fälle
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='timeline', verbose_name="Fall")
    datetime = models.DateTimeField(verbose_name="Datum/Zeit")
    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    
    # Verknüpfungen
    related_person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Beteiligte Person")
    related_location = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ort")
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Erstellt von")
    
    def __str__(self):
        return f"{self.datetime.strftime('%d.%m.%Y %H:%M')} - {self.title}"
    
    class Meta:
        verbose_name = "Zeitachsen-Eintrag"
        verbose_name_plural = "Zeitachsen-Einträge"
        ordering = ['datetime']
