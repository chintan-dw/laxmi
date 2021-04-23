from django.db import models

# Create your models here.
class UploadFile(models.Model):
    cdr = models.FileField()

    