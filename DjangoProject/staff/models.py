from django.db import models

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
    stdlohn = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stdzahl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gehalt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def get_gehalt(self):
        if self.typ == self.TYP_ARBEIT:
            return (self.stdlohn or 0) * (self.stdzahl or 0)
        return self.gehalt or 0

    def __str__(self):
        if self.typ == self.TYP_ARBEIT:
            return f"Arbeit - {self.stdlohn or 0}€ x {self.stdzahl or 0}h"
        return f"Fix - {self.gehalt or 0}€"

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