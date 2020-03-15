from django.urls import path
from . import views

#Configure URL's here

app_name = 'runVRPApp'

urlpatterns = [
    path('', views.runResults, name='runForm'),
    path('compareResults', views.compareResults, name='comparison'),
    path('dispatchEntry', views.dispatchEntry, name='manualEntry')
]
