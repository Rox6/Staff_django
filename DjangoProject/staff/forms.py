from django import forms
from staff.models import Mitarbeiter, Gehaltsmodell

class Staff_form(forms.ModelForm):
    class Meta:
        model = Mitarbeiter
        fields = ['vorname', 'nachname', 'gebdatum', 'einstdatum', 'gehaltmodell', 'geschlecht']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Alle Felder von Bootstrap-Styling
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Date picker for date fields
        if 'gebdatum' in self.fields:
            self.fields['gebdatum'].widget = forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            )
        if 'einstdatum' in self.fields:
            self.fields['einstdatum'].widget = forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            )
        
        # gehaltmodell queryset
        if 'gehaltmodell' in self.fields:
            self.fields['gehaltmodell'].queryset = Gehaltsmodell.objects.all()
            self.fields['gehaltmodell'].empty_label = "-- Bitte Gehaltsmodell wählen --"