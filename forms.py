from django import forms

class runFileForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100, required=False)
#add more fields to the webpage here

class saveVRPForm(forms.Form):
    vrpResultsJSON = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'id':'saveFieldVRP','name':'savedataVRP'}))
    solutionName = forms.CharField(label='Solution Save Name', max_length=255, required = False)