import facebook
import InstagramAPI
token = 'EAADm9nbycx4BANuGpBHQKJtNnye1VmgIJiFZCCLYjYIVZCNcZCsTgzJS3RiLEu8ZCFVLh2EK63LDDejTWn0Tm891F0K1MkqSP5vRm13oUawCbzxX0yBIzT8m5AqLaxpTfHJQp7N0BMWIjDzzXyGwnov5zWl4p5OQTovIK9BvN0aAPOgFlbUZAb8B0TuPUmG4ZD'

import facebook
import os
import jinja2
import requests

me = 'https://graph.facebook.com/v3.2/me?access_token='+token

friends = 'https://graph.facebook.com/v3.2/me/friends?access_token='+token

#me1 = requests.get(me)

#print(me1.text)

'''graph = facebook.GraphAPI(access_token=token, version='2.10')
profile=graph.get_object('me')
posts=graph.get_connections(profile['id'],'posts')
for post in posts['data']:
    message = graph.get_object(id=post['id'])
    print(message['caption'])


#    id+=1

    #print(str(id)+'\t'+ time+'\t'+date+'\t'+year+'\t')# str(num_share)+'\t'+str(num_like))
'''

import os
import json

mypage = 345279809417210

graph = facebook.GraphAPI(token)
posts = graph.get_connections(mypage, 'posts')

for post in posts['data']:
    id = post['id']
    likes = graph.get_connections(id, connection_name='likes', summary='true')
    comments = graph.get_connections(id, connection_name='comments', summary='true')
    print(likes['summary'], comments['summary'])
