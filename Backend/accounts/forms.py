from django import forms

class BulkEmailForm(forms.Form):
    subject = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'size': '40'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=True)
