from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models.functions import Lower
from codesseyapi.models import Category, Programmer

class CategoryView(ViewSet):
    def list(self, request):
        entry_id = self.request.query_params.get('entry', None)
        try:
            if entry_id is not None:
                categories = Category.objects.filter(entries=entry_id).order_by(Lower('label'))
            else:
                categories = Category.objects.order_by(Lower('label'))

            serializer = CategorySerializer(categories, many=True, context={'request': request})
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        new_category = Category()
        new_category.label = request.data["label"]
        author = Programmer.objects.get(user=request.auth.user)
        new_category.author = author
        new_category.save()

        serializer = CategorySerializer(new_category, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]
        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')
        depth = 1
