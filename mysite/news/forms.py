from django import forms
from news.models import UserData


class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['monthly_income', 'family_number', 'credit_payment', 'apartment_costs', 'education_payment', 'other_expenses', 'food_weight', 'transport_weight', 'fun_weight', 'sport_weight']
        widgets = {
            'monthly_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'family_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'credit_payment': forms.NumberInput(attrs={'class': 'form-control'}),
            'apartment_costs': forms.NumberInput(attrs={'class': 'form-control'}),
            'education_payment': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_expenses': forms.NumberInput(attrs={'class': 'form-control'}),
            'food_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'transport_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'fun_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'sport_weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }