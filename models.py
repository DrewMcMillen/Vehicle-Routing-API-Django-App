from django.db import models

# Create your models here.
class solutionName(models.Model):
    name = models.CharField(max_length=255)

class deliverySite(models.Model):
    truck = models.IntegerField()
    longitude = models.DecimalField(max_digits=10, decimal_places=5)
    latitude = models.DecimalField(max_digits=10, decimal_places=5)
    solution = models.ForeignKey(solutionName, on_delete=models.CASCADE)

class manualSolutionName(models.Model):
    name = models.CharField(max_length=255)

class manDeliverySite(models.Model):
    truck = models.IntegerField()
    longitude = models.DecimalField(max_digits=10, decimal_places=5)
    latitude = models.DecimalField(max_digits=10, decimal_places=5)
    solution = models.ForeignKey(solutionName, on_delete=models.CASCADE)