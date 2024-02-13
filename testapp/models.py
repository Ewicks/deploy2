from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    word = models.CharField(max_length=200)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.word


class Date(models.Model):
    startdate = models.DateField()
    enddate = models.DateField()

class Scrape(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borough = models.CharField(max_length=255)
    startdate = models.DateField()
    enddate = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    results_number = models.IntegerField()
    worksheet_file = models.FileField(upload_to='worksheet_files/', null=True, blank=True)
    data = models.JSONField(null=True)



    def __str__(self):
        return f"{self.borough} {self.startdate} {self.enddate}"
