from django import forms


class CreateProjectForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=1024, widget=forms.Textarea)
    visible_to_all = forms.BooleanField(required=False)
