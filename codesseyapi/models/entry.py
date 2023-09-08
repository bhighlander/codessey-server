from django.db import models

class Entry(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('Programmer', on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    solved = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category', through='EntryCategory', related_name='entries')