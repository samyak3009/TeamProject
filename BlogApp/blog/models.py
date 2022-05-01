from statistics import mode
from unicodedata import category
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('category-create')


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    post_image = models.ImageField(blank=True, upload_to='media/profile_pics')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='coding')
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #      return reverse('post-detail', kwargs={'pk': self.pk})