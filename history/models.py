from django.db import models

# Create your models here.
class TwitterUser(models.Model):
    screen_name = models.CharField(max_length=250)
    newest_tweet_id = models.BigIntegerField(null=True, default=None)
    oldest_tweet_id = models.BigIntegerField(null=True, default=None)

    def __str__(self):
        return '{}'.format(self.screen_name)


class TwitterStatus(models.Model):
    twitter_user = models.ForeignKey(TwitterUser)
    status_id = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    created_at = models.DateTimeField()
    text = models.CharField(max_length=300)

    def __str__(self):
        return '({}) - {}'.format(self.status_id, self.text)


