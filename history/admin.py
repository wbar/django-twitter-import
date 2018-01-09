from django.contrib import admin
from . import models
from .twitter import API
import logging
from email.utils import parsedate
import time
import datetime

logger =  logging.getLogger(__name__)

def import_newest(modeladmin, request, queryset):
    for twitter_user in queryset:
        num = twitter_user.newest_tweet_id
        for status in API.GetUserTimeline(screen_name=twitter_user.screen_name, since_id=num):
            try:
                models.TwitterStatus.objects.create(
                    twitter_user=twitter_user,
                    status_id=status.id,
                    created_at=datetime.datetime.fromtimestamp(time.mktime(parsedate(status.created_at))),
                    text=status.text
                )
                if num is None or status.id > num:
                    num = status.id
            except Exception as e:
                logger.exception(e)
                pass
        twitter_user.newest_tweet_id = num
        twitter_user.save()

def import_oldest(modeladmin, request, queryset):
    for twitter_user in queryset:
        num = twitter_user.oldest_tweet_id
        for status in API.GetUserTimeline(screen_name=twitter_user.screen_name, max_id=num):
            try:
                models.TwitterStatus.objects.create(
                    twitter_user=twitter_user,
                    status_id=status.id,
                    created_at=datetime.datetime.fromtimestamp((time.mktime(parsedate(status.created_at)))),
                    text=status.text
                )
                if num is None or status.id < num:
                    num = status.id
            except Exception as e:
                logger.exception(e)
                pass
        twitter_user.oldest_tweet_id = num
        twitter_user.save()

import_newest.short_description = 'Import newest'
import_oldest.short_description = 'Import oldest'

# Register your models here.
@admin.register(models.TwitterUser)
class TwitterUserModelAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'newest_tweet_id', 'oldest_tweet_id')
    readonly_fields = ('newest_tweet_id', 'oldest_tweet_id')
    actions = [import_newest, import_oldest]


@admin.register(models.TwitterStatus)
class TwitterStatusModelAdmin(admin.ModelAdmin):
    list_display = ('twitter_user', 'status_id', 'created_at', 'text')
    readonly_fields = list_display
    list_filter = ('twitter_user', 'created_at')
    search_fields = ('text', )
    order_by = ('twitter_user.screen_name', '-created_at')

