import datetime

from Datepicker import SelectDate
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
    # initiate the driver and add options.
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("useAutomationExtension")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=chrome_options)

    # set a wait time:
    driver.wait = WebDriverWait(driver, 5)

    return driver


def close_driver(driver):
    # Close the driver when finished with it.
    driver.close()
    return


def login_twitter(driver, username, password):
    # opens the web page in the browser.
    driver.get("https://twitter.com/login")

    # finds the boxes for username and password.
    username_field = driver.find_element_by_class_name("js-username-field")
    password_field = driver.find_element_by_class_name("js-password-field")

    # enters username.
    username_field.send_keys(username)
    driver.implicitly_wait(1)

    # enters password.
    password_field.send_keys(password)
    driver.implicitly_wait(1)

    # clicks login button.
    driver.find_element_by_class_name("EdgeButtom--medium").click()

    return True


def Go_to_self(driver, username):
    driver.get("https://twitter.com/" + "@" + username)

    # wait for results to load
    wait = WebDriverWait(driver, 10)

    try:
        # wait until the first search result is found.
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

        # scroll until there are no more tweets:
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
                break

        # extract the html
        page_source = driver.page_source

    except TimeoutException:
        # if there are no search results then return no html.
        page_source = None

    # return html
    return page_source


def Search_HashTag(driver, user, query):
    driver.get("https://twitter.com/search-advanced?lang=en")

    # wait until the search box has loaded.
    Hashtagbox = driver.wait.until(EC.presence_of_element_located((By.NAME, "tag")))

    # find the search box.
    driver.find_element_by_name("tag").clear()

    # enter hashtag string.
    Hashtagbox.send_keys(query)

    # wait until the search box has loaded.
    FromBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "from")))

    # find the user box.
    driver.find_element_by_name("from").clear()

    # enter user.
    FromBox.send_keys(user)

    # Submit.
    FromBox.submit()

    # wait for the search results to load.
    wait = WebDriverWait(driver, 10)

    try:
        # wait until the first search result is found.
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

        # scroll until there are no more tweets.
        while True:

            # extract tweets.
            tweets = driver.find_elements_by_css_selector("li[data-item-id]")

            # scrolling.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # find number of visible tweets.
            number_of_tweets = len(tweets)

            # Wait for more to load
            wait = WebDriverWait(driver, 5)

            try:
                # wait for more tweets to be visible.
                wait.until(wait_for_more_than_n_elements_to_be_present(
                    (By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))

            except TimeoutException:
                # if no more tweets "wait.until" call will timeout.
                break

        # extract the html.
        page_source = driver.page_source

    except TimeoutException:
        # if there are no results return None.
        page_source = None

    return page_source


def Search_logged_in_User(driver, user, sinceDate='', untilDate='', hashtag='', phrase=''):
    driver.get("https://twitter.com/search-advanced?lang=en")

    # wait until the search box has loaded.
    Hashtagbox = driver.wait.until(EC.presence_of_element_located((By.NAME, "tag")))

    # wait until the user box has loaded.
    User = driver.wait.until(EC.presence_of_element_located((By.NAME, "from")))

    # find search box for phrase.
    phraseBox = driver.find_element_by_name("phrase")

    # find the search box.
    driver.find_element_by_name("from").clear()

    # enter user.
    User.send_keys(user)

    if hashtag != "":
        Hashtagbox.send_keys(hashtag)
    if phrase != "":
        phraseBox.send_keys(phrase)

    # since box.
    # sinceBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "since")))

    # until box.
    # untilBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "until")))

    # driver.execute_script("arguments[0].removeAttribute('readonly')", sinceBox)
    # driver.execute_script("arguments[0].removeAttribute('readonly')", untilBox)

    if untilDate == "" and sinceDate != "":
        flash('Both Dates must be picked!')
    elif sinceDate == "" and untilDate != "":
        flash('Both Dates must be picked!')
    elif untilDate != "" and sinceDate != "":

        # Getting inputted since date.
        NewSinceDate = datetime.datetime.strptime(sinceDate, "%Y-%m-%d")

        # splitting it into the right format.
        sinceYear = NewSinceDate.strftime("%Y")
        sinceMonth = NewSinceDate.strftime("%b")
        sinceDay = NewSinceDate.strftime("%d").lstrip("0")

        # using dateselector.py to use datepicker.
        SelectDate(driver, "input-since", sinceYear, sinceMonth, sinceDay)

        # getting inputted until date.
        untilDate = datetime.datetime.strptime(untilDate, "%Y-%m-%d")

        untilYear = untilDate.strftime("%Y")
        untilMonth = untilDate.strftime("%b")
        untilDay = untilDate.strftime("%d").lstrip("0")

        # Selecting until date
        SelectDate(driver, "input-until", untilYear, untilMonth, untilDay)

        # Submit
        User.submit()

        # initial wait for the search results to load
        wait = WebDriverWait(driver, 10)

        try:
            # wait until the first search result is found.
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

            # scroll until there are no more tweets.
            while True:

                # extract all the tweets.
                tweets = driver.find_elements_by_css_selector("li[data-item-id]")

                # keep scrolling.
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # find number of visible tweets.
                number_of_tweets = len(tweets)

                # Wait for more to load.
                wait = WebDriverWait(driver, 5)

                try:
                    # wait for more tweets to be visible.
                    wait.until(wait_for_more_than_n_elements_to_be_present(
                        (By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))

                except TimeoutException:
                    break

            # extract the html.
            page_source = driver.page_source

        except TimeoutException:
            # if there are no search results return none.
            page_source = None

        return page_source


def Search_Specific_User(driver, user, sinceDate, untilDate, hashtag="", phrase=''):
    driver.get("https://twitter.com/search-advanced?lang=en")

    # wait until the hashtag box has loaded.
    Hashtagbox = driver.wait.until(EC.presence_of_element_located((By.NAME, "tag")))

    # wait until the user box has loaded.
    User = driver.wait.until(EC.presence_of_element_located((By.NAME, "from")))

    phraseBox = driver.find_element_by_name("phrase")

    # find the search box and clear it.
    driver.find_element_by_name("from").clear()

    if hashtag != "":
        Hashtagbox.send_keys(hashtag)
    if phrase != "":
        phraseBox.send_keys(phrase)

    # enter user.
    User.send_keys(user)

    # since box.
    # sinceBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "since")))

    # until box.
    # untilBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "until")))

    # ActionChains(driver).move_to_element(sinceBox).click().send_keys(sinceDate).perform()

    # ActionChains(driver).move_to_element(untilBox).click().send_keys(untilDate).perform()

    if untilDate == "" and sinceDate != "":
        flash('Both Dates must be picked!')
    elif sinceDate == "" and untilDate != "":
        flash('Both Dates must be picked!')
    elif untilDate != "" and sinceDate != "":

        # getting inputted since date and getting right format.

        NewSinceDate = datetime.datetime.strptime(sinceDate, "%Y-%m-%d")

        # splitting inputted date into the required pieces.

        sinceYear = NewSinceDate.strftime("%Y")
        sinceMonth = NewSinceDate.strftime("%b")
        sinceDay = NewSinceDate.strftime("%d").lstrip("0")

        # using datepicker.py to select date from datepicker.
        SelectDate(driver, "input-since", sinceYear, sinceMonth, sinceDay)

        # getting inputted since date and getting right format.

        untilDate = datetime.datetime.strptime(untilDate, "%Y-%m-%d")

        # splitting inputted date into the required pieces.

        untilYear = untilDate.strftime("%Y")
        untilMonth = untilDate.strftime("%b")
        untilDay = untilDate.strftime("%d").lstrip("0")

        # using datepicker.py to select date from datepicker.
        SelectDate(driver, "input-until", untilYear, untilMonth, untilDay)

        # Submit.
        User.submit()

        # initial wait for the search results to load.
        wait = WebDriverWait(driver, 10)

        try:
            # wait until the first search result is found.
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

            # scroll down to the last tweet until there are no more tweets.
            while True:

                # extract all the tweets.
                tweets = driver.find_elements_by_css_selector("li[data-item-id]")

                # keep scrolling.
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # find number of visible tweets.
                number_of_tweets = len(tweets)

                # Wait for more to load.
                wait = WebDriverWait(driver, 5)

                try:
                    # wait for more tweets to be visible.
                    wait.until(wait_for_more_than_n_elements_to_be_present(
                        (By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))

                except TimeoutException:
                    # if no more are visible the "wait.until" call will timeout.
                    break

            # extract the html.
            page_source = driver.page_source

        except TimeoutException:
            # if there are no tweets then return none.
            page_source = None

        return page_source


# Normal Search IE: The search bar at the top of the page
# this is a very general search type and isn't very accurate.
def search_twitter(driver, query):
    # wait until the search box has loaded.
    box = driver.wait.until(EC.presence_of_element_located((By.NAME, "q")))

    # find the search box.
    driver.find_element_by_name("q").clear()

    # enter search query.
    box.send_keys(query)

    # submit.
    box.submit()

    # wait for the results to load
    wait = WebDriverWait(driver, 10)

    try:
        # wait until the first search result is found.
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))

        # scroll until there are no more tweets.
        while True:

            # extract all the tweets.
            tweets = driver.find_elements_by_css_selector("li[data-item-id]")

            # find number of visible tweets.
            number_of_tweets = len(tweets)

            # keep scrolling.
            driver.execute_script("arguments[0].scrollIntoView();", tweets[-1])

            try:
                # wait for more tweets.
                wait.until(wait_for_more_than_n_elements_to_be_present(
                    (By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))

            except TimeoutException:
                # if no more are visible the "wait.until" call will timeout.
                break

        # extract the html.
        page_source = driver.page_source

    except TimeoutException:

        # if there are no search results then return none.
        page_source = None

    return page_source


def extract_tweets(page_source):
    # get page source
    soup = bs(page_source, 'lxml')

    i = 0
    #  impressions = []
    #  for item in page_source:
    #  Open analytics of each tweet
    #  driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[4]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li[2]/div[1]/div[2]/div[2]/div[2]/div[4]/button").click()
    #  impressions[i] = driver.find_element_by_css_selector("ep-MetricAnimation").getText()
    #  i+=1
    #  print(impressions[i])

    tweets = []

    # For every list item in the page source
    for li in soup.find_all("li", class_='js-stream-item'):

        totalValue = 0
        totalRetweets = 0
        totalFavourites = 0
        totalReplies = 0

        # print("\nStart of item \n", li, "\nEnd of Item\n"

        # If list item doesn't have an item ID then it isn't a tweet
        if 'data-item-id' not in li.attrs:
            continue
        else:
            # Making Tweet item
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

            # Adding details to tweet item from tweet list item

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

            # Attempts to retrieve impressions data

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

    # print("\n******Totals of all Values in ths Ad Campaign*****\n")
    # print("\nTotal Value of all tweets: €", round(totalValue, 2))
    # print("\nTotal number of all replies: ", totalReplies)
    # print("\nTotal number of all favourite: ", totalFavourites)
    # print("\nTotal number of all retweets: ", totalRetweets)
    # print("\nTotal number of all tweets: ", i)

    return (finalTotalValue, totalRetweets, totalFavourites, totalReplies, i)

# Below were used in testing:

# start a driver.
# driver = init_driver()

# Testing log in function.

# username = ""
# password = ""
# login_twitter(driver, username, password)


# Testing Searching a specific username.

# Search_username = "@paddypower"
# query = "#Brexit"

# Testing searching own account.

# User_Self = ""
# password =""
# page_source = search_twitter(driver, query)

# Time frames for testing the specific date queries

# SINCE
# since = "2015-04-02"

# TILL
# till = "2018-05-24"

# Full functions

# page_source = Search_HashTag(driver, Search_username, query)
# page_source = Go_to_self(driver, User_Self, password)
# page_source = Search_Specific_User(driver, User_Self, password, since, till)

# Extraction

# tweets = extract_tweets(page_source)

# close and quit driver.

# close_driver(driver)
