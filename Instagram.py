from InstagramAPI import InstagramAPI

InstagramAPI = InstagramAPI("themanmahon", "Ian_Mahon1")
InstagramAPI.login()

#InstagramAPI.getProfileData()
#result = InstagramAPI.LastJson

#print(result)

import time

myposts = []
has_more_posts = True
max_id = ""

while has_more_posts:
    InstagramAPI.getSelfUserFeed(maxid=max_id)
    if InstagramAPI.LastJson['more_available'] is not True:
        has_more_posts = False  # stop condition
        print
        "stopped"

    max_id = InstagramAPI.LastJson.get('next_max_id', '')
    myposts.extend(InstagramAPI.LastJson['items'])  # merge lists
    time.sleep(2)  # Slows the script down to avoid flooding the servers

for item in myposts:
    print("Poster Name: ", item['user']['username'])
    print("Post ID: ",item['id'])
    print("Comment Count: ", item['comment_count'])
    print("Like count: ", item['like_count'])

