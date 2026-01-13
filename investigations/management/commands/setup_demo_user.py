# investigations/management/commands/setup_demo_user.py
"""
Management-Command zum Erstellen eines sicheren Demo-Users.
Credentials werden aus Environment-Variablen geladen.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config
import secrets


class Command(BaseCommand):
    help = 'Erstellt oder aktualisiert den Demo-User mit sicheren Credentials'

    def add_arguments(self, parser):
        parser.add_argument(
            '--generate-password',
            action='store_true',
            help='Generiert ein neues sicheres Passwort',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Setzt ein bestimmtes Passwort (nur für Entwicklung)',
        )

    def handle(self, *args, **options):
        demo_username = config('DEMO_USERNAME', default='demo_reviewer')
        demo_email = config('DEMO_EMAIL', default='demo@example.com')
        
        # Passwort-Handling
        if options['generate_password']:
            demo_password = secrets.token_urlsafe(16)
            self.stdout.write(
                self.style.WARNING(f'Generiertes Passwort: {demo_password}')
            )
            self.stdout.write(
                self.style.WARNING('Bitte als DEMO_PASSWORD in Fly.io Secrets speichern!')
            )
        elif options['password']:
            demo_password = options['password']
        else:
            demo_password = config('DEMO_PASSWORD', default=None)
        
        if not demo_password:
            self.stdout.write(
                self.style.ERROR(
                    'Kein Passwort angegeben. Nutze --generate-password oder '
                    'setze DEMO_PASSWORD als Environment-Variable.'
                )
            )
            return
        
        # User erstellen oder aktualisieren
        user, created = User.objects.get_or_create(
            username=demo_username,
            defaults={
                'email': demo_email,
                'is_staff': False,  # Kein Admin-Zugang für Demo
                'is_superuser': False,
                'first_name': 'Demo',
                'last_name': 'Reviewer',
            }
        )
        
        user.set_password(demo_password)
        user.save()
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Demo-User "{demo_username}" erstellt.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Demo-User "{demo_username}" aktualisiert.')
            )
        
        self.stdout.write(
            self.style.NOTICE(
                '\nHinweis: Der Demo-User hat READ-ONLY Zugang zum System.\n'
                'Für Produktiv-Nutzung bitte separaten Admin-User verwenden.'
            )
        )
