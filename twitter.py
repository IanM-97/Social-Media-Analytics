import sys
import tweepy
from IPython.lib.deepreload import reload
from tweepy import Stream, API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# Variables that contains the user credentials to access Twitter API
access_token = '1305387432-jtGbbKrNeICsjhDjIooiXrHeI2cWHTDPvwr3AXg'
access_secret = 'Oa9U5vsWG96Im1YLTMmqf7RPhZQF58t6C6S3g62Hg15Bj'
consumer_key = '357Vq4tSRSPOkizPP5bQt6lmi'
consumer_secret = 'WdG1VJV6Q0JgUoJBp8jkSVFiAhJ36WMcGKpgEYxuiNaBhCpDSJ'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

stuff = api.user_timeline(screen_name = 'realdonaldtrump', count = 1000, include_rts = True)


for status in stuff:
    print("ID:" , status.id)
    print("Text:" , status.text)
    print("Favourites:" , status.favorite_count)
    print("Retweets:" , status.retweet_count)
