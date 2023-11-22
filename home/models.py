from django.db import models


class Students(models.Model):
    name = models.CharField(max_length=100,)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, primary_key=True)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=10)

