from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from codesseyapi.models import Entry, Programmer, Category

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

    def update(self, request, pk):

        if "category_add" in request.data:
            entry = Entry.objects.get(pk=pk)
            categories = Category.objects.get(pk=request.data["category_add"])
            entry.categories.add(categories) #set resets it, add adds to it, remove removes it. try add_or_remove or something like that? see if you can combine with _or_
        elif "category_remove" in request.data:
            categories = Category.objects.get(pk=request.data["category_remove"])
            entry.categories.remove(categories)
        else:
            categories = request.data["categories"]
            entry = Entry.objects.get(pk=pk)
            entry.title = request.data["title"]
            entry.content = request.data["content"]
            entry.solved = request.data["solved"]

        entry.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, _, pk=None):
        try:
            entry = Entry.objects.get(pk=pk)
            entry.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Entry.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class ProgrammerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programmer
        fields = ('id', 'full_name')
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')

class EntrySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    author = ProgrammerSerializer(many=False)
    class Meta:
        model = Entry
        fields = ('id', 'title', 'content', 'author', 'publication_date', 'solved', 'categories')
        depth = 1