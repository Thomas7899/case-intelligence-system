from django.contrib import admin
from .models import Case, PersonInvolvement, Evidence, Investigation, Timeline


class PersonInvolvementInline(admin.TabularInline):
    model = PersonInvolvement
    extra = 1
    readonly_fields = ['created_at']


class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 0
    readonly_fields = ['created_at']
    fields = ['evidence_number', 'title', 'evidence_type', 'collected_date', 'collected_by']


class TimelineInline(admin.TabularInline):
    model = Timeline
    extra = 0
    readonly_fields = ['created_at']
    fields = ['datetime', 'title', 'related_person', 'related_location']


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['case_number', 'title', 'case_type', 'status', 'priority', 'assigned_to', 'created_at']
    list_filter = ['case_type', 'status', 'priority', 'created_at', 'assigned_to']
    search_fields = ['case_number', 'title', 'description']
    readonly_fields = ['reported_date', 'created_at', 'updated_at']
    
    inlines = [PersonInvolvementInline, EvidenceInline, TimelineInline]
    
    fieldsets = (
        ('Grunddaten', {
            'fields': ('case_number', 'title', 'description', 'case_type', 'status', 'priority')
        }),
        ('Zeitdaten', {
            'fields': ('incident_date', 'reported_date')
        }),
        ('Verknüpfungen', {
            'fields': ('location', 'involved_vehicles')
        }),
        ('Zuständigkeit', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Metadaten', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PersonInvolvement)
class PersonInvolvementAdmin(admin.ModelAdmin):
    list_display = ['person', 'case', 'involvement_type', 'credibility', 'created_at']
    list_filter = ['involvement_type', 'credibility', 'created_at']
    search_fields = ['person__first_name', 'person__last_name', 'case__case_number', 'case__title']
    readonly_fields = ['created_at']


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ['evidence_number', 'title', 'case', 'evidence_type', 'collected_date', 'collected_by']
    list_filter = ['evidence_type', 'collected_date', 'collected_by']
    search_fields = ['evidence_number', 'title', 'description', 'case__case_number']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Grunddaten', {
            'fields': ('case', 'evidence_number', 'title', 'description', 'evidence_type')
        }),
        ('Fundort', {
            'fields': ('location_found', 'file')
        }),
        ('Verwahrung', {
            'fields': ('chain_of_custody', 'collected_date', 'collected_by')
        }),
        ('Metadaten', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    list_display = ['title', 'case', 'investigation_type', 'planned_date', 'completed_date', 'assigned_to']
    list_filter = ['investigation_type', 'planned_date', 'completed_date', 'assigned_to']
    search_fields = ['title', 'description', 'case__case_number', 'case__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Grunddaten', {
            'fields': ('case', 'title', 'description', 'investigation_type')
        }),
        ('Beteiligte', {
            'fields': ('target_persons', 'assigned_to')
        }),
        ('Zeitplanung', {
            'fields': ('planned_date', 'completed_date')
        }),
        ('Ergebnis', {
            'fields': ('result',)
        }),
        ('Metadaten', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        })
    )


@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'title', 'case', 'related_person', 'related_location']
    list_filter = ['datetime', 'case', 'created_at']
    search_fields = ['title', 'description', 'case__case_number']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Grunddaten', {
            'fields': ('case', 'datetime', 'title', 'description')
        }),
        ('Verknüpfungen', {
            'fields': ('related_person', 'related_location')
        }),
        ('Metadaten', {
            'fields': ('created_at', 'created_by'),
            'classes': ('collapse',)
        })
    )
