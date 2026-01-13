# entities/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Person(models.Model):
    """
    Zentrale Entität für alle Personen im System
    """
    RISK_LEVEL_CHOICES = [
        (0, 'Kein Risiko'),
        (1, 'Gering'),
        (2, 'Mittel'),
        (3, 'Hoch'),
        (4, 'Sehr hoch'),
    ]
    
    # Grunddaten
    first_name = models.CharField(max_length=100, verbose_name="Vorname")
    last_name = models.CharField(max_length=100, verbose_name="Nachname")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Geburtsdatum")
    birth_place = models.CharField(max_length=200, null=True, blank=True, verbose_name="Geburtsort")
    
    # Identifikation
    id_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="Ausweisnummer")
    known_aliases = models.TextField(blank=True, verbose_name="Bekannte Aliase")
    
    # Bewertung
    risk_level = models.IntegerField(choices=RISK_LEVEL_CHOICES, default=0, verbose_name="Risikostufe")
    notes = models.TextField(blank=True, verbose_name="Notizen")
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Erstellt von")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        if self.birth_date:
            today = now().date()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"
        ordering = ['last_name', 'first_name']


class Address(models.Model):
    """
    Adressdaten und Standorte
    """
    street = models.CharField(max_length=200, verbose_name="Straße")
    house_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Hausnummer")
    postal_code = models.CharField(max_length=20, null=True, blank=True, verbose_name="PLZ")
    city = models.CharField(max_length=100, verbose_name="Stadt")
    country = models.CharField(max_length=100, default="Deutschland", verbose_name="Land")
    
    # Geo-Koordinaten (optional)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True, verbose_name="Breitengrad")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True, verbose_name="Längengrad")
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    
    def __str__(self):
        return f"{self.street} {self.house_number}, {self.postal_code} {self.city}"
    
    class Meta:
        verbose_name = "Adresse"
        verbose_name_plural = "Adressen"
        ordering = ['city', 'street']


class Vehicle(models.Model):
    """
    Fahrzeugdaten
    """
    VEHICLE_TYPE_CHOICES = [
        ('car', 'PKW'),
        ('motorcycle', 'Motorrad'),
        ('truck', 'LKW'),
        ('bus', 'Bus'),
        ('other', 'Sonstiges'),
    ]
    
    license_plate = models.CharField(max_length=20, unique=True, verbose_name="Kennzeichen")
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default='car', verbose_name="Fahrzeugtyp")
    make = models.CharField(max_length=50, null=True, blank=True, verbose_name="Hersteller")
    model = models.CharField(max_length=50, null=True, blank=True, verbose_name="Modell")
    year = models.IntegerField(null=True, blank=True, verbose_name="Baujahr")
    color = models.CharField(max_length=50, null=True, blank=True, verbose_name="Farbe")
    
    # Besitzer
    owner = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Besitzer")
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    
    def __str__(self):
        return f"{self.license_plate} ({self.make} {self.model})"
    
    class Meta:
        verbose_name = "Fahrzeug"
        verbose_name_plural = "Fahrzeuge"
        ordering = ['license_plate']


class PersonAddress(models.Model):
    """
    Verbindung zwischen Person und Adresse mit Zeitraum
    """
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Person")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Adresse")
    
    # Zeitraum
    start_date = models.DateField(null=True, blank=True, verbose_name="Wohnhaft seit")
    end_date = models.DateField(null=True, blank=True, verbose_name="Wohnhaft bis")
    
    # Typ der Verbindung
    ADDRESS_TYPE_CHOICES = [
        ('primary', 'Hauptwohnsitz'),
        ('secondary', 'Nebenwohnsitz'),
        ('temporary', 'Temporär'),
        ('work', 'Arbeitsplatz'),
        ('other', 'Sonstiges'),
    ]
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES, default='primary', verbose_name="Adresstyp")
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    
    def __str__(self):
        return f"{self.person.full_name} - {self.address}"
    
    class Meta:
        verbose_name = "Person-Adresse"
        verbose_name_plural = "Person-Adressen"
        unique_together = ['person', 'address', 'address_type']


class PersonRelationship(models.Model):
    """
    Beziehungen zwischen Personen
    """
    RELATIONSHIP_TYPE_CHOICES = [
        ('family', 'Familie'),
        ('friend', 'Freund'),
        ('colleague', 'Kollege'),
        ('neighbor', 'Nachbar'),
        ('associate', 'Bekannter'),
        ('suspect', 'Verdächtiger'),
        ('victim', 'Opfer'),
        ('witness', 'Zeuge'),
        ('other', 'Sonstiges'),
    ]
    
    person1 = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relationships_from', verbose_name="Person 1")
    person2 = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relationships_to', verbose_name="Person 2")
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPE_CHOICES, verbose_name="Beziehungstyp")
    
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    strength = models.IntegerField(default=1, verbose_name="Stärke (1-5)")
    
    # Zeitraum
    start_date = models.DateField(null=True, blank=True, verbose_name="Bekannt seit")
    end_date = models.DateField(null=True, blank=True, verbose_name="Bekannt bis")
    
    # Metadaten
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Erstellt von")
    
    def __str__(self):
        return f"{self.person1.full_name} - {self.get_relationship_type_display()} - {self.person2.full_name}"
    
    class Meta:
        verbose_name = "Beziehung"
        verbose_name_plural = "Beziehungen"
        unique_together = ['person1', 'person2', 'relationship_type']
