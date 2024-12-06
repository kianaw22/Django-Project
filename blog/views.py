from http.client import HTTPResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from drf_spectacular.utils import extend_schema
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserSignupForm
from .models import CustomUser

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
    

def signup_student(request):
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = CustomUser.STUDENT  
            user.save() 
            login(request, user)  
            return redirect('blog:student_dashboard')  
    else:
        form = CustomUserSignupForm()

    return render(request, 'blog/signup.html', {'form': form})


def signup_teacher(request):
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = CustomUser.TEACHER 
            user.save()
            login(request, user) 
            return redirect('blog:teacher_dashboard') 
    else:
        form = CustomUserSignupForm()

    return render(request, 'blog/signup.html', {'form': form})


def signup_admin(request):
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = CustomUser.ADMIN  
            user.save()
            login(request, user)  
            return redirect('blog:admin_dashboard')  
    else:
        form = CustomUserSignupForm()

    return render(request, 'blog/signup.html', {'form': form})


def teacher_dashboard(request):
    if request.user.is_authenticated and request.user.role == CustomUser.TEACHER:
        return render(request, 'blog/teacher_dashboard.html')
    else:
        return HttpResponse("You are not authorized to access this page.", status=403)


def admin_dashboard(request):
    if request.user.is_authenticated and request.user.role == CustomUser.ADMIN:
        return render(request, 'blog/admin_dashboard.html')
    else:
        return HttpResponse("You are not authorized to access this page.", status=403)
    

def student_dashboard(request):
    if request.user.is_authenticated and request.user.role == CustomUser.STUDENT:
        return render(request, 'blog/student_dashboard.html')  
    else:
        return HttpResponse("You are not authorized to access this page.", status=403)