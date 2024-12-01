# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import User
from django.db import models

class MainNews(models.Model):
    ranking = models.IntegerField(blank=True, primary_key=True)
    keywords = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    img_link = models.TextField(blank=True, null=True)
    category = models.IntegerField(blank=True)



    class Meta:
        managed = False
        db_table = 'Main_news'


from django.db import models
from django.contrib.auth.models import User

class UserFavoriteKeywords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)  # 기본 값 설정
    keyword = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.keyword

class RecentKeyword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField()
    url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

