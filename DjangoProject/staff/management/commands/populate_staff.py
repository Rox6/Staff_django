from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from staff.models import Mitarbeiter, Gehaltsmodell, Geschlecht
import random

class Command(BaseCommand):
    help = 'Populate database with sample employee data'

    def handle(self, *args, **options):
        # Sample data
        sample_data = [
            {'vorname': 'John', 'nachname': 'Müller', 'gebdatum': date(1985, 5, 15), 'geschlecht': 'M'},
            {'vorname': 'Maria', 'nachname': 'Schmidt', 'gebdatum': date(1990, 8, 22), 'geschlecht': 'W'},
            {'vorname': 'Peter', 'nachname': 'Weber', 'gebdatum': date(1988, 3, 10), 'geschlecht': 'M'},
            {'vorname': 'Anna', 'nachname': 'Becker', 'gebdatum': date(1992, 11, 5), 'geschlecht': 'W'},
            {'vorname': 'Thomas', 'nachname': 'Fischer', 'gebdatum': date(1987, 7, 18), 'geschlecht': 'M'},
            {'vorname': 'Lisa', 'nachname': 'Meyer', 'gebdatum': date(1995, 2, 28), 'geschlecht': 'W'},
        ]
        
        # Create salary models if needed
        modell1, created = Gehaltsmodell.objects.get_or_create(
            typ=Gehaltsmodell.TYP_ARBEIT,
            defaults={'stdlohn': 15.50, 'stdzahl': 40}
        )
        modell2, created = Gehaltsmodell.objects.get_or_create(
            typ=Gehaltsmodell.TYP_FIX,
            defaults={'gehalt': 2500}
        )
        
        # Add employees using for loop
        for data in sample_data:
            # Random employment date within last 3 years
            days_ago = random.randint(30, 1095)
            einstdatum = date.today() - timedelta(days=days_ago)
            
            mitarbeiter, created = Mitarbeiter.objects.get_or_create(
                vorname=data['vorname'],
                nachname=data['nachname'],
                defaults={
                    'gebdatum': data['gebdatum'],
                    'einstdatum': einstdatum,
                    'geschlecht': data['geschlecht'],
                    'gehaltmodell': modell1 if random.choice([True, False]) else modell2,
                }
            )
            
            status = 'Created' if created else 'Already exists'
            self.stdout.write(self.style.SUCCESS(f'{status}: {mitarbeiter}'))
        
        self.stdout.write(self.style.SUCCESS('Sample data populated successfully!'))
