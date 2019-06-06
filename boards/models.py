from django.db import models
from django.utils import timezone


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True)
    date_published = models.DateTimeField(default=timezone.now)

    def threads(self):
        topics = Topic.objects.filter(board=self)
        return topics

    def thread_count(self):
        topics = Topic.objects.filter(board=self)
        return len(topics)

    def post_count(self):
        posts = Post.objects.filter(topic__board=self)
        return len(posts)

    def __str__(self):
        return self.name


class Topic(models.Model):
    board = models.ForeignKey(Board, default='ETC', on_delete=models.SET_DEFAULT)
    title = models.CharField(max_length=100, unique=True)
    date_published = models.DateTimeField(default=timezone.now)

    def posts(self):
        posts = Post.objects.filter(topic=self)
        return posts

    def post_count(self):
        posts = Post.objects.filter(topic=self)
        return len(posts)

    def __str__(self):
        return self.title


class Post(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=200, default='Unknown', blank=True, null=True)
    date_published = models.DateTimeField(default=timezone.now)
    topic = models.ForeignKey(Topic, default=content, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.content
