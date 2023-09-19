from datetime import datetime
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from codesseyapi.models import Todo, Programmer

class TodoView(ViewSet):
    def list(self, request):
        try:
            todos = Todo.objects.order_by('-created_at')

            serializer = TodoSerializer(todos, many=True, context={'request': request})
            return Response(serializer.data)
        except Todo.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
            serializer = TodoSerializer(todo, context={'request': request})
            return Response(serializer.data)
        except Todo.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        new_todo = Todo()
        author = Programmer.objects.get(user=request.auth.user)
        new_todo.author = author
        new_todo.content = request.data["content"]
        new_todo.created_at = datetime.now()
        new_todo.completed_at = None
        new_todo.done = False
        new_todo.save()

        serializer = TodoSerializer(new_todo, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        todo = Todo.objects.get(pk=pk)
        todo.content = request.data["content"]
        todo.done = request.data["done"]
        todo.completed_at = request.data["completed_at"] if request.data["done"] else None
        todo.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
            todo.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Todo.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'content', 'completed_at', 'created_at', 'done')