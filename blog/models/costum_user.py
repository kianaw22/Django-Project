from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):

    ADMIN = 'admin'
    STUDENT = 'student'
    TEACHER = 'teacher'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]

   
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
          # Default role is 'student'
    )

    def __str__(self):
        return self.username