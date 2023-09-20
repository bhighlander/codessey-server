from django.db import models

class Todo(models.Model):
    content = models.CharField(max_length=100)
    author = models.ForeignKey('Programmer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(default=None, null=True, blank=True)