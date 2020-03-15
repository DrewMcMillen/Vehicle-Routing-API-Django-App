from django import forms
from django.forms import formset_factory

class runFileForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100, required=False)
#add more fields to the webpage here

class saveVRPForm(forms.Form):
    vrpResultsJSON = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'id':'saveFieldVRP','name':'savedataVRP'}))
    solutionName = forms.CharField(label='Solution Save Name', max_length=255, required = False)

class solutionNameSearch(forms.Form):
    nameFilter = forms.CharField(label='Search Solutions', max_length=255)

class manualSolutionRow(forms.Form):
    truck = forms.IntegerField(label=False)
    longitude = forms.DecimalField(max_digits=10, decimal_places=5)
    latitude = forms.DecimalField(max_digits=10, decimal_places=5)

manSolRowFormset = formset_factory(manualSolutionRow,extra=2)

class manSolutionName(forms.Form):
    solutionName = forms.CharField(label='Save Entry', max_length=255, required = True)