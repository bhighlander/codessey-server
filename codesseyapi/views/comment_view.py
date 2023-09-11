from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from codesseyapi.models import Comment, Programmer, Entry

class CommentView(ViewSet):
    def list(self, request):
        try:
            comments = Comment.objects.order_by('-publication_date')

            if "entry" in request.query_params:
                entry_id = self.request.query_params.get('entry')
                comments = Comment.objects.filter(entry=entry_id)

            serializer = CommentSerializer(comments, many=True, context={'request': request})
            return Response(serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        new_comment = Comment()
        new_comment.title = request.data["title"]
        new_comment.content = request.data["content"]
        author = Programmer.objects.get(user=request.auth.user)
        new_comment.author = author
        new_comment.publication_date = datetime.now()
        new_comment.entry = Entry.objects.get(pk=request.data["entry"])
        new_comment.save()

        serializer = CommentSerializer(new_comment, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comment.title = request.data["title"]
        comment.content = request.data["content"]
        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'title', 'content', 'author', 'publication_date', 'entry')
        depth = 1