
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer,SignupSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import CustomUser

CustomUser = get_user_model()

class PostListCreateAPIView(APIView):
    """
    Handles listing all posts and creating a new post.
    """ 
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(request=PostSerializer)
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveUpdateDeleteAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a single post.
    """
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=PostSerializer)
    def put(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        post.delete()

        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    


class SignupView(APIView):
    """
    API View to handle user signup and return JWT tokens.
    """
    @extend_schema(request=SignupSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "User successfully created",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DashboardAPIView(APIView):
    """
    API for user dashboards based on roles.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == CustomUser.STUDENT:
            return Response({'message': 'Welcome to the Student Dashboard!'}, status=status.HTTP_200_OK)
        elif user.role == CustomUser.TEACHER:
            return Response({'message': 'Welcome to the Teacher Dashboard!'}, status=status.HTTP_200_OK)
        elif user.role == CustomUser.ADMIN:
            return Response({'message': 'Welcome to the Admin Dashboard!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)