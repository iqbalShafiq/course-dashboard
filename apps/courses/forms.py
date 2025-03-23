from django import forms
from apps.courses.models import Course

class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'capacity', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-slate-900 rounded p-2 w-full'}),
            'description': forms.Textarea(attrs={'class': 'border border-slate-900 rounded p-2 w-full', 'rows': 4}),
            'capacity': forms.NumberInput(attrs={'class': 'border border-slate-900 rounded p-2 w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'border border-slate-900 rounded'}),
        }
