from django import forms
from apps.teachers.models import Teacher

class TeacherEditForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'specialization']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'border border-slate-900 rounded p-2 w-full',
                'placeholder': 'Enter teacher name'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'border border-slate-900 rounded p-2 w-full',
                'placeholder': 'Enter specialization'
            }),
        }
