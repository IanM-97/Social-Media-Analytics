import facebook
import InstagramAPI
token = 'EAADm9nbycx4BAIVJYc45g3L1ly0GSXF3vJ6QMh2jlfqjMq3qmGzoKpWsZCDjYT320JKG0G9HZBHNGasFyv33dIVedETZAE4R6eA9riCdRiWRQ52brwUeKNTLtjZBy88HfFuEQ8jInbAxsrmoQEg4WL8gTD95cKyu36J6SRLOlFT2LFo0Gu48dRxZAvqYFIVzS3Sh8kiaHJgZDZD'
pageToken = "EAADm9nbycx4BANaUIZCK6aaEpA6oom10Kvghu87S86ZBdBDkx4jywGkgz46esJSkcIu8xeBfl0GggRW6OZCMAgGRPp2FqQVUdgQUB8dPjDRSbGROQ03DckiF1jBs7vop8s72yjCbRw6cRHIyHWueMjTBPaj9a57fYizw3M1hHx5TqP2SUAPdyVq8HbX0NatF4FiZCddmZBgZDZD"
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

graph = facebook.GraphAPI(pageToken)
posts = graph.get_connections(mypage, 'posts')

postNumber = 0
total_likes = 0
total_comments = 0
total_shares = 0
total_Value = 0

for post in posts['data']:
    value = 0
    postNumber += 1
    id = post['id']
    likes = graph.get_connections(id, connection_name='reactions', summary='true')
    comments = graph.get_connections(id, connection_name='comments', summary='true')
    print("******************Next Post******************")
    print("\nPost Number: ", postNumber)
    print("Time Posted: ", post['created_time'])
    print("Post: " ,post['message'])
    print("Reations: ", likes['summary']['total_count'])
    print("Comments: ", comments['summary']['total_count'])
    value += (likes['summary']['total_count'] * 0.15) + (comments['summary']['total_count'] * 0.10)
    print("Value: ", round(value),2)

    total_likes += likes['summary']['total_count']
    total_comments += comments['summary']['total_count']
    total_Value += value

print("\n******Total Amounts from all Posts******")
print("Total amount of Likes: ", total_likes)
print("Total amount of Comments: ", total_comments)
print("Total Value: €", round(total_Value),2)

