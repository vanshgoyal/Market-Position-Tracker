from django import forms

class upload_file_form(forms.Form):
    # Userid = forms.CharField()
    # Password = forms.CharField(widget=forms.PasswordInput)
    trade_file = forms.FileField(
    	label='Select a file ',
    )
