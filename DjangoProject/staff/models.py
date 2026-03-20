from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Geschlecht(models.TextChoices):
    D = 'D', "Divers"
    W = 'W', "Weiblich"
    M = 'M', "Männlich"


class Gehaltsmodell(models.Model):
    TYP_ARBEIT = 'ARBEIT'
    TYP_FIX = 'FIX'
    TYP_CHOICES = [
        (TYP_ARBEIT, 'Arbeitermodell'),
        (TYP_FIX, 'Fixgehaltmodell'),
    ]

    typ = models.CharField(max_length=10, choices=TYP_CHOICES, default=TYP_ARBEIT)
    stdlohn = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    stdzahl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    gehalt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])

    def get_gehalt(self):
        if self.typ == self.TYP_ARBEIT:
            # Monatsgehalt aus Stunden pro Woche × Stundensatz × 4,33 Wochen/Monat
            return (self.stdlohn or Decimal('0')) * (self.stdzahl or Decimal('0')) * Decimal('4.33')
        return self.gehalt or Decimal('0')

    def __str__(self):
        if self.typ == self.TYP_ARBEIT:
            monats = (self.stdlohn or 0) * (self.stdzahl or 0) * 4.33
            return f"Arbeit - {self.stdlohn or 0}€/h × {self.stdzahl or 0}h/Woche = {monats:.2f}€/Monat"
        return f"Fix - {self.gehalt or 0}€/Monat"   

class Mitarbeiter(models.Model):
    vorname = models.CharField(max_length=30)
    nachname = models.CharField(max_length=30)
    gebdatum = models.DateField()
    einstdatum = models.DateField()
    
    gehaltmodell = models.ForeignKey(Gehaltsmodell, on_delete=models.CASCADE, blank=True, null=True)
    geschlecht = models.CharField(max_length=1, choices=Geschlecht.choices)

    def get_gehalt(self):
        if self.gehaltmodell:
            return self.gehaltmodell.get_gehalt()
        return 0

    def __str__(self):
        return f"{self.vorname} {self.nachname}"