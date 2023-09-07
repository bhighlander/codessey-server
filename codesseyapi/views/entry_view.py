from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from codesseyapi.models import Entry, Programmer

class EntryView(ViewSet):
    def list(self, request):
        try:
            entries = Entry.objects.order_by('-publication_date')
            if "user" in request.query_params:
                author = Programmer.objects.get(user=request.auth.user)
                entries = entries.filter(author=author)

            serializer = EntrySerializer(entries, many=True)
            return Response(serializer.data)
        except Entry.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def retrieve(self, request, pk=None):
        try:
            entry = Entry.objects.get(pk=pk)
            serializer = EntrySerializer(entry)
            return Response(serializer.data)
        except Entry.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
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