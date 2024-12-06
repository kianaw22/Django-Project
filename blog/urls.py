
from blog import views
from django.urls import path
from .views import PostListCreateAPIView, PostRetrieveUpdateDeleteAPIView
app_name = 'blog'
urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteAPIView.as_view(), name='post-retrieve-update-delete'),

    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('signup/student/', views.signup_student, name='signup_student'),
    path('signup/teacher/', views.signup_teacher, name='signup_teacher'),
    path('signup/admin/', views.signup_admin, name='signup_admin'),

   
  
    
]