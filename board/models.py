from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    hits = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    area = models.CharField(max_length=200)

    # 조회수 증가
    @property
    def update_hits(self):
        self.hits += 1
        self.save()

class Answer(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    likes = models.IntegerField(default=0)
    content = models.TextField()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    content = models.TextField()