from django.db import models
from accounts.models import CustomUsers

class Post(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUsers, on_delete=models.CASCADE, related_name='author_post')
    create_date = models.DateTimeField()
    hits = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    area = models.CharField(max_length=200)
    voter = models.ManyToManyField(CustomUsers, related_name='voter_post')
    liked = models.BooleanField(default=False)

    # 조회수 증가
    @property
    def update_hits(self):
        self.hits += 1
        self.save()

class Answer(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUsers, on_delete=models.CASCADE, related_name='author_answer')
    create_date = models.DateTimeField()
    likes = models.IntegerField(default=0)
    content = models.TextField()
    voter = models.ManyToManyField(CustomUsers, related_name='voter_answer')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    content = models.TextField()