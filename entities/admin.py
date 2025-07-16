from django.contrib import admin
from .models import Person, Address, Vehicle, PersonAddress, PersonRelationship


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'birth_date', 'age', 'risk_level', 'created_at']
    list_filter = ['risk_level', 'created_at', 'birth_date']
    search_fields = ['first_name', 'last_name', 'known_aliases', 'id_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Grunddaten', {
            'fields': ('first_name', 'last_name', 'birth_date', 'birth_place')
        }),
        ('Identifikation', {
            'fields': ('id_number', 'known_aliases')
        }),
        ('Bewertung', {
            'fields': ('risk_level', 'notes')
        }),
        ('Metadaten', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        })
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'city', 'postal_code', 'country']
    list_filter = ['city', 'country', 'created_at']
    search_fields = ['street', 'city', 'postal_code']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'make', 'model', 'year', 'owner', 'vehicle_type']
    list_filter = ['vehicle_type', 'make', 'year', 'created_at']
    search_fields = ['license_plate', 'make', 'model', 'owner__first_name', 'owner__last_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PersonAddress)
class PersonAddressAdmin(admin.ModelAdmin):
    list_display = ['person', 'address', 'address_type', 'start_date', 'end_date']
    list_filter = ['address_type', 'start_date', 'end_date']
    search_fields = ['person__first_name', 'person__last_name', 'address__street', 'address__city']
    readonly_fields = ['created_at']


@admin.register(PersonRelationship)
class PersonRelationshipAdmin(admin.ModelAdmin):
    list_display = ['person1', 'relationship_type', 'person2', 'strength', 'start_date']
    list_filter = ['relationship_type', 'strength', 'start_date', 'created_at']
    search_fields = ['person1__first_name', 'person1__last_name', 'person2__first_name', 'person2__last_name']
    readonly_fields = ['created_at', 'updated_at']
