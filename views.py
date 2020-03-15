from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import csv
import pandas as pd


# Create your views here.
from .models import solutionName, deliverySite, manDeliverySite, manualSolutionName
from .forms import runFileForm, saveVRPForm, solutionNameSearch, manSolRowFormset, manSolutionName
#First experimental view; all it did was download the results
def runForm(request):

    if request.method == 'POST' and 'run_script' in request.POST:
        form = runFileForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            print(name)

            from .SSH_Client import funcVRP
            #VRP returns results in a DataFrame
            resultsVRP = funcVRP()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(name)
            resultsVRP.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=True,decimal=".")
            df_html = resultsVRP.to_html()
            return render(request, 'runVRP/form.html',{'form':form, 'df_html':df_html})


            #return response
    #blank form for the first time you open the web page in your browser
    form = runFileForm()

    return render(request, 'runVRP/form.html', {'form':form})

def runResults(request):
    if request.method == 'POST' and 'run_script' in request.POST:
        from .SSH_Client import funcVRP
        #funcVRP returns the results as a pandas dataframe
        resultsVRP = funcVRP()
        #we want to display the results in a table;
        #to_html() is a built in dataframe method
        df_html = resultsVRP.to_html()
        #define saveForm so HTML renders for JS save function to work
        saveForm = saveVRPForm()
        return render(request, 'runVRP/form.html',{'df_html':df_html,'saveForm':saveForm})
    #upon initial page visit, render the html page without any results displayed
    elif request.method == 'POST' and 'save_form' in request.POST:
        saveForm = saveVRPForm(request.POST)
        if saveForm.is_valid():
            vrpResultsJSON = saveForm.cleaned_data['vrpResultsJSON']
            solName = saveForm.cleaned_data['solutionName']
            #save solution name first
            solNameModel = solutionName(name=solName)
            solNameModel.save()
            #parse results into a python list
            import json
            arr = json.loads(vrpResultsJSON)
            for i in range(0, len(arr),3):
                truckNum = arr[i]
                longit = arr[i + 1]
                latit = arr[i + 2]
                saveDelivSite = deliverySite(truck=truckNum, latitude=latit, longitude=longit, solution =solNameModel)
                saveDelivSite.save()
            return render(request, 'runVRP/saveSuccess.html',{'vrpResultsJSON':vrpResultsJSON})
    saveForm = saveVRPForm()
    return render(request, 'runVRP/form.html',{'saveForm':saveForm})

def compareResults(request):
    if request.method == 'GET':
        solnQForm = solutionNameSearch(request.GET)
        if solnQForm.is_valid():
            sol_name_q = solnQForm.cleaned_data['nameFilter']
            soln = deliverySite.objects.filter(solution__name=sol_name_q)
            context = {'searchedSoln':soln, 'solnQForm': solnQForm}
            return render(request, 'runVRP/compareResults.html', context)
    solnQForm = solutionNameSearch()
    context = {'solnQForm':solnQForm, 'searchedSoln':[]}
    return render(request, 'runVRP/compareResults.html',context)

def dispatchEntry(request):
    if request.method == 'GET':
        formset = manSolRowFormset(request.GET or None)
        nameForm = manSolutionName(request.GET or None)
    elif request.method == 'POST':
        #manually entered solution rows
        formset = manSolRowFormset(request.POST)
        #name of the solution (should match name of VRP generated soln)
        nameForm = manSolutionName(request.POST)
        if formset.is_valid() and nameForm.is_valid():
            #get solution Name from form
            name = nameForm.cleaned_data.get('solutionName')
            #create manualSolutionName model object
            solName = manualSolutionName(name=name)
            #save solution name into database
            solName.save()
            #loop through rows and save models
            for form in formset:
                truck = form.cleaned_data.get('truck')
                longitude = form.cleaned_data('longitude')
                latitude = form.cleaned_data('latitude')
                #save the row into the database
                manDeliverySite(truck=truck,longitude=longitude,latitude=latitude,solution=solName).save()
            return render(request,'runVRP/saveSuccess.html',{'vrpResultsJSON':[]})
    return render(request, 'runVRP/manualEntry.html',{'nameForm':nameForm, 'formset':formset})













