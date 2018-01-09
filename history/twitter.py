import twitter
from django.conf import settings


API = twitter.Api(
    consumer_key=settings.OAUTH_TOKENS_TWITTER_CLIENT_ID, 
    consumer_secret=settings.OAUTH_TOKENS_TWITTER_CLIENT_SECRET, 
    access_token_key=settings.OAUTH_TOKENS_TWITTER_TOKEN, 
    access_token_secret=settings.OAUTH_TOKENS_TWITTER_TOKEN_SECRET
)

