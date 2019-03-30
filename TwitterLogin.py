'''import re
import time

from bs4 import element, BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()

me_url = u"https://twitter.com/TheManMahon"
#base_url  = u"https://twitter.com/search?q="
#query = u"Trump"
#url = base_url + query

browser.get(me_url)
time.sleep(1)

body = browser.find_element_by_tag_name("body")

for _ in range(2):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)

tweets = browser.find_elements_by_class_name("tweet-text")

for tweet in tweets:
    print(tweet)

Att = browser.find_element_by_xpath('//*[@id="stream-item-tweet-1067180894186819584"]/div[1]/div[2]/div[2]/div[2]')
html = Att.get_attribute('outerHTML')
attributes = BeautifulSoup(html, 'html.parser').a.attrs
print(attributes)'''

from bs4 import BeautifulSoup as bs
from flask import flash
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class wait_for_more_than_n_elements_to_be_present(object):
    def __init__(self, locator, count):
        self.locator = locator
        self.count = count

    def __call__(self, driver):
        try:
            elements = EC._find_elements(driver, self.locator)
            return len(elements) > self.count
        except StaleElementReferenceException:
            return False


def init_driver():
    # initiate the driver:
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("useAutomationExtension")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver = webdriver.PhantomJS()

    # set a default wait time for the browser [5 seconds here]:
    driver.wait = WebDriverWait(driver, 5)

    return driver


def close_driver(driver):
    driver.close()
    return


def login_twitter(driver, username, password):
    # opens the web page in the browser:
    driver.get("https://twitter.com/login")

    # finds the boxes for username and password
    username_field = driver.find_element_by_class_name("js-username-field")
    password_field = driver.find_element_by_class_name("js-password-field")

    # enters username:
    username_field.send_keys(username)
    driver.implicitly_wait(1)

    # enters password:
    password_field.send_keys(password)
    driver.implicitly_wait(1)

    # clicks the "Log In" button:
    driver.find_element_by_class_name("EdgeButtom--medium").click()

    return True


def Go_to_self(driver, username):

    driver.get("https://twitter.com/"+"@"+username)
    # initial wait for the search results to load
    wait = WebDriverWait(driver, 10)

    try:
        # wait until the first search result is found.
        # Search results will be tweets, which are html list items and have the class='data-item-id':
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

        # scroll down to the last tweet until there are no more tweets:
        while True:

            # extract all the tweets:
            tweets = driver.find_elements_by_css_selector("li[data-item-id]")

            # find number of visible tweets:
            number_of_tweets = len(tweets)

            # keep scrolling:
            driver.execute_script("arguments[0].scrollIntoView();", tweets[-1])

            try:
                # wait for more tweets to be visible:
                wait.until(wait_for_more_than_n_elements_to_be_present(
                    (By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))

            except TimeoutException:
                # if no more are visible the "wait.until" call will timeout.
                print("No More tweets available")
                # Catch the exception and exit the while loop:
                break

        # extract the html for the whole lot:
        page_source = driver.page_source

    except TimeoutException:
        # if there are no search results then the
        # "wait.until" call in the first "try" statement will never happen and it will time out.
        # So we catch that exception and return no html.
        page_source = None

    return page_source


def Search_HashTag(driver, user, query):
    driver.get("https://twitter.com/search-advanced?lang=en")
    # initial wait for the search results to load
    # wait until the search box has loaded:
    Hashtagbox = driver.wait.until(EC.presence_of_element_located((By.NAME, "tag")))

    # find the search box in the html:
    driver.find_element_by_name("tag").clear()

    # enter your search string in the search box:
    Hashtagbox.send_keys(query)

    # wait until the search box has loaded:
    FromBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "from")))

    # find the search box in the html:
    driver.find_element_by_name("from").clear()

    # enter your search string in the search box:
    FromBox.send_keys(user)

    # Submit
    FromBox.submit()

    # initial wait for the search results to load
    wait = WebDriverWait(driver, 10)

    try:
        # wait until the first search result is found.
        # Search results will be tweets, which are html list items and have the class='data-item-id':
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

        # scroll down to the last tweet until there are no more tweets:
        while True:

            # extract all the tweets:
            tweets = driver.find_elements_by_css_selector("li[data-item-id]")

            # keep scrolling:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # find number of visible tweets:
            number_of_tweets = len(tweets)

            # Wait for more to load
            wait = WebDriverWait(driver, 5)

            try:
                # wait for more tweets to be visible:
                wait.until(wait_for_more_than_n_elements_to_be_present(
                    (By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))

            except TimeoutException:
                # if no more are visible the "wait.until" call will timeout.
                # Catch the exception and exit the while loop:
                break

        # extract the html for the whole lot:
        page_source = driver.page_source

    except TimeoutException:
        # if there are no search results then the
        # "wait.until" call in the first "try" statement will never happen and it will time out.
        # So we catch that exception and return no html.
        page_source = None

    return page_source


def Search_logged_in_User(driver, user, sinceDate='', untilDate='', query=""):
    driver.get("https://twitter.com/search-advanced?lang=en")
    # initial wait for the search results to load
    # wait until the search box has loaded:
    Hashtagbox = driver.wait.until(EC.presence_of_element_located((By.NAME, "tag")))

    # wait until the search box has loaded:
    User = driver.wait.until(EC.presence_of_element_located((By.NAME, "from")))

    # find the search box in the html:
    driver.find_element_by_name("from").clear()

    # enter your search string in the search box:
    User.send_keys(user)

    if (query != ""):
        Hashtagbox.send_keys(query)

    # since
    sinceBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "since")))

    # until
    untilBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "until")))

    # ActionChains(driver).move_to_element(sinceBox).click().send_keys(sinceDate).perform()

    # ActionChains(driver).move_to_element(untilBox).click().send_keys(untilDate).perform()

    driver.execute_script("arguments[0].removeAttribute('readonly')", sinceBox)
    driver.execute_script("arguments[0].removeAttribute('readonly')", untilBox)

    if untilDate == "" and sinceDate != "":
        flash('Both Dates must be picked!')
    elif sinceDate == "" and untilDate != "":
        flash('Both Dates must be picked!')
    elif untilDate != "" and sinceDate != "":
        untilBox.send_keys(untilDate)
        #####For some reason the date pickers dont work if since is inputted before until??
        sinceBox.send_keys(sinceDate)

        # Submit
        sinceBox.submit()

        # initial wait for the search results to load
        wait = WebDriverWait(driver, 10)

        try:
            # wait until the first search result is found.
            # Search results will be tweets, which are html list items and have the class='data-item-id':
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

            # scroll down to the last tweet until there are no more tweets:
            while True:

                # extract all the tweets:
                tweets = driver.find_elements_by_css_selector("li[data-item-id]")

                # keep scrolling:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # find number of visible tweets:
                number_of_tweets = len(tweets)

                # Wait for more to load
                wait = WebDriverWait(driver, 5)

                try:
                    # wait for more tweets to be visible:
                    wait.until(wait_for_more_than_n_elements_to_be_present(
                        (By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))

                except TimeoutException:
                    # if no more are visible the "wait.until" call will timeout.
                    # Catch the exception and exit the while loop:
                    break

            # extract the html for the whole lot:
            page_source = driver.page_source

        except TimeoutException:
            # if there are no search results then the
            # "wait.until" call in the first "try" statement will never happen and it will time out.
            # So we catch that exception and return no html.
            page_source = None

        return page_source



def Search_Specific_User(driver, user, sinceDate, untilDate, query=""):
    driver.get("https://twitter.com/search-advanced?lang=en")
    # initial wait for the search results to load
    # wait until the search box has loaded:
    Hashtagbox = driver.wait.until(EC.presence_of_element_located((By.NAME, "tag")))

    # wait until the search box has loaded:
    User = driver.wait.until(EC.presence_of_element_located((By.NAME, "from")))

    # find the search box in the html:
    driver.find_element_by_name("from").clear()

    if (query != ""):
        Hashtagbox.send_keys(query)

    # enter your search string in the search box:
    User.send_keys(user)

    # since
    sinceBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "since")))

    # until
    untilBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "until")))

    # ActionChains(driver).move_to_element(sinceBox).click().send_keys(sinceDate).perform()

    # ActionChains(driver).move_to_element(untilBox).click().send_keys(untilDate).perform()

    driver.execute_script("arguments[0].removeAttribute('readonly')", sinceBox)
    driver.execute_script("arguments[0].removeAttribute('readonly')", untilBox)

    if untilDate == "" and sinceDate != "":
        flash('Both Dates must be picked!')
    elif sinceDate == "" and untilDate != "":
        flash('Both Dates must be picked!')
    elif untilDate != "" and sinceDate != "":
        untilBox.send_keys(untilDate)
        #####For some reason the date pickers dont work if since is inputted before until??
        sinceBox.send_keys(sinceDate)

        # Submit
        sinceBox.submit()

        # initial wait for the search results to load
        wait = WebDriverWait(driver, 10)

        try:
            # wait until the first search result is found.
            # Search results will be tweets, which are html list items and have the class='data-item-id':
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

            # scroll down to the last tweet until there are no more tweets:
            while True:

                # extract all the tweets:
                tweets = driver.find_elements_by_css_selector("li[data-item-id]")

                # keep scrolling:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # find number of visible tweets:
                number_of_tweets = len(tweets)

                # Wait for more to load
                wait = WebDriverWait(driver, 5)

                try:
                    # wait for more tweets to be visible:
                    wait.until(wait_for_more_than_n_elements_to_be_present(
                        (By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))

                except TimeoutException:
                    # if no more are visible the "wait.until" call will timeout.
                    # Catch the exception and exit the while loop:
                    break

            # extract the html for the whole lot:
            page_source = driver.page_source

        except TimeoutException:
            # if there are no search results then the
            # "wait.until" call in the first "try" statement will never happen and it will time out.
            # So we catch that exception and return no html.
            page_source = None

        return page_source


def search_twitter(driver, query):
    # wait until the search box has loaded:
    box = driver.wait.until(EC.presence_of_element_located((By.NAME, "q")))

    # find the search box in the html:
    driver.find_element_by_name("q").clear()

    # enter your search string in the search box:
    box.send_keys(query)

    # submit the query (like hitting return):
    box.submit()

    # initial wait for the search results to load
    wait = WebDriverWait(driver, 10)

    try:
        # wait until the first search result is found.
        # Search results will be tweets, which are html list items and have the class='data-item-id':
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

        # scroll down to the last tweet until there are no more tweets:
        while True:

            # extract all the tweets:
            tweets = driver.find_elements_by_css_selector("li[data-item-id]")

            # find number of visible tweets:
            number_of_tweets = len(tweets)

            # keep scrolling:
            driver.execute_script("arguments[0].scrollIntoView();", tweets[-1])

            try:
                # wait for more tweets to be visible:
                wait.until(wait_for_more_than_n_elements_to_be_present(
                    (By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))

            except TimeoutException:
                # if no more are visible the "wait.until" call will timeout.
                # Catch the exception and exit the while loop:
                break

        # extract the html for the whole lot:
        page_source = driver.page_source

    except TimeoutException:

        # if there are no search results then the
        # "wait.until" call in the first "try" statement will never happen and it will time out.
        # So we catch that exception and return no html.
        page_source = None

    return page_source


def extract_tweets(page_source):
    soup = bs(page_source, 'lxml')

    i = 0
    impressions = []

    #  for item in page_source:
    # Open analytics of each tweet
    #     driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[4]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li[2]/div[1]/div[2]/div[2]/div[2]/div[4]/button").click()
    #    impressions[i] = driver.find_element_by_css_selector("ep-MetricAnimation").getText()
    #   i+=1
    #  print(impressions[i])

    tweets = []
    for li in soup.find_all("li", class_='js-stream-item'):

        totalValue = 0
        totalRetweets = 0
        totalFavourites = 0
        totalReplies = 0

        # print("\nStart of item \n", li, "\nEnd of Item\n")

        # If our li doesn't have a tweet-id, we skip it as it's not going to be a tweet.
        if 'data-item-id' not in li.attrs:
            continue
        else:
            tweet = {
                'tweet_id': li['data-item-id'],
                'text': None,
                'user_id': None,
                'user_screen_name': None,
                'user_name': None,
                'created_at': None,
                'retweets': 0,
                'likes': 0,
                'replies': 0,
                'impressions': 0,
                'value': 0
            }

            # Tweet Text
            text_p = li.find("p", class_="tweet-text")
            if text_p is not None:
                tweet['text'] = text_p.get_text()

            # Tweet User ID, User Screen Name, User Name
            user_details_div = li.find("div", class_="tweet")
            if user_details_div is not None:
                tweet['user_id'] = user_details_div['data-user-id']
                tweet['user_screen_name'] = user_details_div['data-screen-name']
                tweet['user_name'] = user_details_div['data-name']

            # Tweet date
            date_span = li.find("span", class_="_timestamp")
            if date_span is not None:
                tweet['created_at'] = float(date_span['data-time-ms'])

            # Tweet Retweets
            retweet_span = li.select("span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount")
            if retweet_span is not None and len(retweet_span) > 0:
                tweet['retweets'] = int(retweet_span[0]['data-tweet-stat-count'])

            # Tweet Likes
            like_span = li.select("span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount")
            if like_span is not None and len(like_span) > 0:
                tweet['likes'] = int(like_span[0]['data-tweet-stat-count'])

            # Tweet Replies
            reply_span = li.select("span.ProfileTweet-action--reply > span.ProfileTweet-actionCount")
            if reply_span is not None and len(reply_span) > 0:
                tweet['replies'] = int(reply_span[0]['data-tweet-stat-count'])

            # Tweet impressions
            '''analytics_span = li.select("div.ProfileTweet-action.ProfileTweet-action--analytics")
            if analytics_span is not None and len(analytics_span) > 0:
                analyticsbutton = driver.find_element_by_css_selector(".ProfileTweet-actionButton")
                driver.execute_script("arguments[0].scrollIntoView();", analyticsbutton)
                analyticsbutton.click()
                impressions = driver.find_element_by_css_selector("ep-MetricValue").getText()
                print(impressions)'''

            # driver.find_element_by_css_selector(".ProfileTweet-actionButton.u-textUserColorHover.js-actionButton.js-actionQuickPromote").click()
            # impressions = driver.find_element_by_css_selector("ep-MetricValue").getText()
            # print("\nStart of item \n", li, "\nEnd of Item\n")
            # print("Impressions: ", impressions)
            # driver.find_element_by_css_selector("QuickPromoteDialog modal-container").click()


            # Tweet VALUE ROI
            tweet['value'] += round((tweet['replies'] * 0.10), 2)
            tweet['value'] += round((tweet['likes'] * 0.15), 2)
            tweet['value'] += round((tweet['retweets'] * 0.25), 2)

            tweets.append(tweet)

    for tweet in tweets:
        i += 1
        '''Value = round(tweet['value'],2)
        print("\nTweet Number: ", i)
        print("Username: ", tweet['user_name'])
        print("Text: ", tweet['text'])
        print("Retweets: ", tweet['retweets'])
        print("Likes: ", tweet['likes'])
        print("Replies: ", tweet['replies'])
        print("Impressions: ", tweet['impressions'])
        print("Value: €", Value)'''

        totalValue += round(tweet['value'], 2)
        totalFavourites += tweet['likes']
        totalReplies += tweet['replies']
        totalRetweets += tweet['retweets']

        finalTotalValue = round(totalValue, 2)

        # results = [finalTotalValue, totalRetweets, totalFavourites, totalReplies]

        # return results

    print("\n******Totals of all Values in ths Ad Campaign*****\n")
    print("\nTotal Value of all tweets: €", round(totalValue, 2))
    print("\nTotal number of all replies: ", totalReplies)
    print("\nTotal number of all favourite: ", totalFavourites)
    print("\nTotal number of all retweets: ", totalRetweets)
    print("\nTotal number of all tweets: ", i)

    return (finalTotalValue, totalRetweets, totalFavourites, totalReplies, i)

# start a driver for a web browser:
# driver = init_driver()

# log in to twitter (replace username/password with your own):
# username = "themanmahon"
# password = "Chocolate1"
# login_twitter(driver, username, password)
##### Search Hashtag


####QUERIES FOR SEARCHING A SPECIFIC ACCOUNT FOR A SPECIFIC HASHTAG
# Search_username = "@paddypower"
# query = "#Brexit"

##### search self:
# User_Self = "@themanmahon"
# password ="Chocolate1"
# page_source = search_twitter(driver, query)


#######SINCE
# since = "2015-04-02"

#######TILL
# till = "2018-05-24"

# search twitter:
# page_source = Search_HashTag(driver, Search_username, query)
# page_source = Go_to_self(driver, User_Self, password)
# page_source = Search_Specific_User(driver, User_Self, password, since, till)
# extract info from the search results:
# tweets = extract_tweets(page_source)

# close and quit the driver:
# close_driver(driver)
