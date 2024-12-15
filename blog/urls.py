
from blog import views
from django.urls import path
from .views import PostListCreateAPIView, PostRetrieveUpdateDeleteAPIView,SignupView,ChangeRoleView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
app_name = 'blog'
urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteAPIView.as_view(), name='post-retrieve-update-delete'),


    path('signup/', SignupView.as_view(), name='signup'),
    path('change-role/', ChangeRoleView.as_view(), name='change-role'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   
  
    
]