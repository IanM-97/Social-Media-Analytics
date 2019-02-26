import facebook
import InstagramAPI
token = 'EAADm9nbycx4BACbP0Jjrr0itWWH7wjg9RcCmOg5GpmHsFa91burnYRLfUsQfqcxcHpv85t3E4LwZCZCkQ9cJ2j5M1ocmBs5RS9idOGcurN3Lgrm1qXydBvS7TpX9kUZAx0QswBZApd4csAdRZCUOvFZAW3ZB4EKeCdgTzxwsWCh7wZDZD'

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

graph = facebook.GraphAPI(token)
posts = graph.get_connections('me', 'posts')

for post in posts['data']:
    print(post)
