from django import forms
from .models import Students


class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ["name", "age", "email", "address", "contact"]


class UpdateStudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ["name", "age", "email", "address", "contact"]

