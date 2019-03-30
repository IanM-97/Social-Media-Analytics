import facebook

token = 'EAADm9nbycx4BANkZABl8OgEyVDk1AtOL7uwEa81bOossl6VrRhTZAyfZBCF8PrIKQZCYYEhydcy08jZCnjuqbvgWsZCowTcSaRg9UmqZBioXvg6gNwviYciaT3Vo0xnR7ijpL3yv6oxr7ZA5OcvAxyGxGlpQPwZAKWga8QkTlFFOZCZBwZDZD'
FBpageToken = "EAADm9nbycx4BAJ9ZCAOaFZAp07eBWcZAJiR25iYZAzdYO8kZCnUQqZB8JWMeSk33KPBAZAGuyOrpnfipWIrzOTTDmjNjmDQyDqDdrW6zODQbr6wSF77xao0ybZA8ub9wEeKl9cKscxkn5IWPiMAVxiI4cLkbLwl2ATv340oLcDbS4AZDZD"

me = 'https://graph.facebook.com/v3.2/me?access_token=' + token

friends = 'https://graph.facebook.com/v3.2/me/friends?access_token=' + token

mypage = 345279809417210


def check_access_token(token):
    graph = facebook.GraphAPI(token)
    app_id = '253946231943966' # Obtained from https://developers.facebook.com/
    app_secret = '5e71bbac5b669d1de943fb5c3d4f5cdd' # Obtained from https://developers.facebook.com/

    # Extend the expiration time of a valid OAuth access token.
    extended_token = graph.extend_access_token(app_id, app_secret)
    #print(extended_token) #verify that it expires in 60 days

def check_page_token(FBpageToken):
    graph = facebook.GraphAPI(FBpageToken)
    app_id = '253946231943966' # Obtained from https://developers.facebook.com/
    app_secret = '5e71bbac5b669d1de943fb5c3d4f5cdd' # Obtained from https://developers.facebook.com/

    # Extend the expiration time of a valid OAuth access token.
    extended_token = graph.extend_access_token(app_id, app_secret)
    #print(extended_token) #verify that it expires in 60 days

def extract_Facebook_posts(pageToken=FBpageToken, pageID=mypage):
    graph = facebook.GraphAPI(pageToken)
    posts = graph.get_connections(pageID, 'posts')

    postNumber = 0
    total_likes = 0
    total_comments = 0
    total_Value = 0

    for post in posts['data']:
        value = 0
        postNumber += 1
        post_id = post['id']
        likes = graph.get_connections(post_id, connection_name='reactions', summary='true')
        comments = graph.get_connections(post_id, connection_name='comments', summary='true')
        print("******************Next Post******************")
        print("\nPost Number: ", postNumber)
        print("Time Posted: ", post['created_time'])
        print("Post: ", post['message'])
        print("Reations: ", likes['summary']['total_count'])
        print("Comments: ", comments['summary']['total_count'])
        value += (likes['summary']['total_count'] * 0.15) + (comments['summary']['total_count'] * 0.10)
        print("Value: ", round(total_Value, 2))

        total_likes += likes['summary']['total_count']
        total_comments += comments['summary']['total_count']
        total_Value += value

   # print("\n******Total Amounts from all Posts******")
   # print("Total amount of Reactions: ", total_likes)
   # print("Total amount of Comments: ", total_comments)
   # print("Total Value: €", round(total_Value, 2))

    total_posts = postNumber
    finalTotalValue = round(total_Value, 2)

    return total_likes, total_comments, finalTotalValue, total_posts

check_page_token(FBpageToken)
