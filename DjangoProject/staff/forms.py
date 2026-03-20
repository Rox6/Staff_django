from django import forms
from staff.models import Mitarbeiter, Gehaltsmodell

class Gehaltsmodell_form(forms.ModelForm):
    class Meta:
        model = Gehaltsmodell
        fields = ['typ', 'stdlohn', 'stdzahl', 'gehalt']
        labels = {
            'typ': 'Gehalttyp',
            'stdlohn': '€ pro Stunde',
            'stdzahl': 'Stunden pro Woche',
            'gehalt': 'Fixgehalt (€)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class Staff_form(forms.ModelForm):
    gehalt_typ = forms.ChoiceField(
        choices=Gehaltsmodell.TYP_CHOICES,
        label='Gehalttyp',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input', 'onchange': 'updateGehaltFields()'}),
        required=False
    )
    stdlohn = forms.DecimalField(
        label='€ pro Stunde',
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'z.B. 15.50', 'step': '0.01'})
    )
    stdzahl = forms.DecimalField(
        label='Stunden pro Woche',
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'z.B. 40', 'step': '0.5'})
    )
    fixgehalt = forms.DecimalField(
        label='Fixgehalt (€)',
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'z.B. 2500', 'step': '0.01'})
    )

    class Meta:
        model = Mitarbeiter
        fields = ['vorname', 'nachname', 'gebdatum', 'einstdatum', 'geschlecht']
        labels = {
            'vorname': 'Vorname',
            'nachname': 'Nachname',
            'gebdatum': 'Geburtsdatum',
            'einstdatum': 'Einstellungsdatum',
            'geschlecht': 'Geschlecht',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Bootstrap-Styling für Standard-Felder
        for field_name, field in self.fields.items():
            if field_name not in ['gehalt_typ']:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Date picker
        self.fields['gebdatum'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
        self.fields['einstdatum'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
        
        # Wenn es einen existierenden Mitarbeiter gibt, die Gehalt-Daten ausfüllen
        if self.instance.pk and self.instance.gehaltmodell:
            modell = self.instance.gehaltmodell
            self.fields['gehalt_typ'].initial = modell.typ
            if modell.typ == Gehaltsmodell.TYP_ARBEIT:
                self.fields['stdlohn'].initial = modell.stdlohn
                self.fields['stdzahl'].initial = modell.stdzahl
            else:
                self.fields['fixgehalt'].initial = modell.gehalt

    def clean(self):
        cleaned_data = super().clean()
        gehalt_typ = cleaned_data.get('gehalt_typ')
        
        if gehalt_typ == Gehaltsmodell.TYP_ARBEIT:
            if not cleaned_data.get('stdlohn') or not cleaned_data.get('stdzahl'):
                raise forms.ValidationError('Bitte € pro Stunde und Stunden pro Woche eingeben.')
        elif gehalt_typ == Gehaltsmodell.TYP_FIX:
            if not cleaned_data.get('fixgehalt'):
                raise forms.ValidationError('Bitte Fixgehalt eingeben.')
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        gehalt_typ = self.cleaned_data.get('gehalt_typ')
        stdlohn = self.cleaned_data.get('stdlohn')
        stdzahl = self.cleaned_data.get('stdzahl')
        fixgehalt = self.cleaned_data.get('fixgehalt')
        
        if gehalt_typ:
            # Gehaltsmodell erstellen oder aktualisieren
            if instance.gehaltmodell:
                modell = instance.gehaltmodell
            else:
                modell = Gehaltsmodell.objects.create(typ=gehalt_typ)
            
            modell.typ = gehalt_typ
            if gehalt_typ == Gehaltsmodell.TYP_ARBEIT:
                modell.stdlohn = stdlohn
                modell.stdzahl = stdzahl
                modell.gehalt = None
            else:
                modell.gehalt = fixgehalt
                modell.stdlohn = None
                modell.stdzahl = None
            
            modell.save()
            instance.gehaltmodell = modell
        
        if commit:
            instance.save()
        
        return instance