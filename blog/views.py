from .models.post import Post
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from rest_framework.viewsets import ViewSet

	##Render web pages and no serialization needed , just model passed to view
'''def post_list(request):

    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
'''

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Post
from .serializers import PostSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import extend_schema
class PostViewSet(viewsets.ViewSet):
   
    @action(detail=False, methods=['get'], name='List Posts')
    def list_posts(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=PostSerializer,  # Expected request body
        responses=PostSerializer,  # Document the response schema
    )
    @action(detail=False, methods=['post'], name='Create Post')
    def create_post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], name='Retrieve Post')
    def retrieve_post(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @extend_schema(
        request=PostSerializer,  # Expected request body
        responses=PostSerializer,  # Document the response schema
    )
    @action(detail=True, methods=['put'], name='Update Post')
    def update_post(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'], name='Delete Post')
    def delete_post(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
