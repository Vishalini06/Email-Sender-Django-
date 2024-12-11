from django import forms

class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    recipients = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter comma-separated emails"}))
    attachment = forms.FileField(required=False)
