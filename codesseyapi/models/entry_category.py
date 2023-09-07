from django.db import models

class EntryCategory(models.Model):
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)