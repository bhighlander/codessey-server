from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime
from codesseyapi.models import Entry, Programmer

class EntryView(ViewSet):
    def list(self, request):

        entries = Entry.objects.order_by('-publication_date')
        if "user" in request.query_params:
            author = Programmer.objects.get(user=request.auth.user)
            entries = entries.filter(author=author)

        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        new_entry = Entry()
        new_entry.title = request.data["title"]
        new_entry.content = request.data["content"]
        programmer = Programmer.objects.get(user=request.auth.user)
        new_entry.author = programmer
        new_entry.publication_date = datetime.now()
        new_entry.solved = False
        new_entry.save()

        serializer = EntrySerializer(new_entry, context={'request': request})
        return Response(serializer.data)
    

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('id', 'title', 'content', 'author', 'publication_date', 'solved')
        depth = 1