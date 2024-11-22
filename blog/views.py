from django.shortcuts import render
from .models.post import Post

def post_list(request):

    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
