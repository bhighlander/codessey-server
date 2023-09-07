from django.db import models

class Comment(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('Programmer', on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)