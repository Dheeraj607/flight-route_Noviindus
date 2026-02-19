from django import forms
from .models import AirportNode

class AirportRouteForm(forms.ModelForm):
    class Meta:
        model = AirportNode
        fields = ['airport_code', 'parent', 'position', 'duration']
        widgets = {
            'airport_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Airport B'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in minutes'}),
        }

class SearchNthNodeForm(forms.Form):
    start_airport = forms.ModelChoiceField(
        queryset=AirportNode.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    n = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'N (e.g. 2)'})
    )
    direction = forms.ChoiceField(
        choices=[('left', 'Left'), ('right', 'Right')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class ShortestPathForm(forms.Form):
    from_airport = forms.ModelChoiceField(
        queryset=AirportNode.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    to_airport = forms.ModelChoiceField(
        queryset=AirportNode.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
