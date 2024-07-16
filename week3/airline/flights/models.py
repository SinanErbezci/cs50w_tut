from django.db import models

# Create your models here.
# Think as a table in db
class Flight(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()

# Migrations. Means the changes you made.
# Then you migrate them which means applying into the database
# python manage.py makemigrations
# python manage.py migrate