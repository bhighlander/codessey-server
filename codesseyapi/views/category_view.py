from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models.functions import Lower
from codesseyapi.models import Category

class CategoryView(ViewSet):
    def list(self, request):
        try:
            categories = Category.objects.order_by(Lower('label'))
            serializer = CategorySerializer(categories, many=True, context={'request': request})
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    def create(self, request):
        new_category = Category()
        new_category.label = request.data["label"]
        new_category.save()

        serializer = CategorySerializer(new_category, context={'request': request})
        return Response(serializer.data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')
        depth = 1