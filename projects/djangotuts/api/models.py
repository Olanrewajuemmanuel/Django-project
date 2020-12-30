from django.db import models

# Create your models here.

class User(models.Model):
    url = models.URLField(max_length=200, null=False)
    username = models.TextField(max_length=100)
    email = models.EmailField(max_length=254)
    groups = models.TextField(max_length=200)

    def __str__(self):
        "Data to be sent when interacting with the django API"
        return self.username   

    class Meta:
        db_table = 'users'


class Group(models.Model):
    group = models.ForeignKey('api.User', on_delete=models.CASCADE)


class Article(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
