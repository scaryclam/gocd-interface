from django import forms


class ProjectForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=1024, widget=forms.Textarea)
    visible_to_all = forms.BooleanField(required=False)
    gocd_server_host = forms.CharField(max_length=255)
    gocd_server_port = forms.IntegerField()
    gocd_server_username = forms.CharField(max_length=255)
    gocd_server_password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))


class ProjectMembersForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=1024, widget=forms.Textarea)
    visible_to_all = forms.BooleanField(required=False)
