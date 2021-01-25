from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    bio = models.TextField(max_length=500, default="My Bio", blank=True)
    name = models.CharField(blank=True, max_length=120)
    projects = models.ForeignKey('Project', on_delete=models.CASCADE,null=True, blank=True)
    contact = models.EmailField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Project(models.Model):
    title = models.CharField(max_length=20,blank=True)
    link = models.URLField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to = 'images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null='True', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title}'

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    @classmethod
    def all_projects(cls):
        return cls.objects.all()

    @classmethod
    def search_project(cls, title):
        return cls.objects.filter(title__icontains=title).all()

    class Meta:
        ordering = ["-date_posted"]

