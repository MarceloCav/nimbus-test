from django import forms

class ReportForm(forms.Form):
    phones = forms.CharField(max_length=200, help_text='Digite um ou mais números de telefone separados por vírgulas')
    report_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    send_email = forms.BooleanField(required=False)
