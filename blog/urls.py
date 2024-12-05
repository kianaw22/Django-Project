
from django.urls import path
from .views import PostListCreateAPIView, PostRetrieveUpdateDeleteAPIView

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteAPIView.as_view(), name='post-retrieve-update-delete'),

   
  
    
]