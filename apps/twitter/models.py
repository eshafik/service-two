from django.db import models


class FeedPost(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey('user.User', on_delete=models.CASCADE,
                               related_name='author_feed')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserPostServingHistory(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE,
                             related_name='user_seen')
    post = models.ForeignKey(FeedPost, on_delete=models.CASCADE, related_name='post_seen')
    created_at = models.DateTimeField(auto_now_add=True)
