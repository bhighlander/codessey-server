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

            if "category" in request.query_params:
                category_id = self.request.query_params.get('category')
                if category_id.isnumeric():
                    category_id = int(category_id)
                    entries = entries.filter(categories=category_id)

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

        try:
            entry = Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            return Response({'message': 'Entry does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if "category_add" in request.data:
            categories = Category.objects.get(pk=request.data["category_add"])
            entry.categories.add(categories)
        if "category_remove" in request.data:
            categories = Category.objects.get(pk=request.data["category_remove"])
            entry.categories.remove(categories)
        if "solved" in request.data:
            entry.solved = request.data["solved"]
        if "title" in request.data and "content" in request.data:
            categories = request.data["categories"]
            entry.title = request.data["title"]
            entry.content = request.data["content"]

        entry.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, _, pk=None):
        try:
            entry = Entry.objects.get(pk=pk)
            entry.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Entry.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False)
    def unsolved_entries(self, request):
        try:
            author = Programmer.objects.get(user=request.auth.user)
            entries = Entry.objects.filter(solved=False, author=author)
            serializer = EntrySerializer(entries, many=True)
            return Response(serializer.data)
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
    publication_date = serializers.DateTimeField(format="%m/%d/%Y")
    class Meta:
        model = Entry
        fields = ('id', 'title', 'content', 'author', 'publication_date', 'solved', 'categories')
        depth = 1