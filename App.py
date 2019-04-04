import os
import socket
import threading
import webbrowser
from pathlib import Path

import win32api
import win32com.client
import pythoncom

import easygui
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, session
from selenium.common.exceptions import NoSuchElementException

from Instagram import extract_insta_posts
from TwitterLogin import init_driver, login_twitter, extract_tweets, Search_logged_in_User, Search_Specific_User, \
    close_driver
from facebookTest import extract_Facebook_posts

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

driver = init_driver()

# Secret Key for session variables #
app.secret_key = 'secretkey123456'

# for Facebook API #
facebook_user_token = 'EAADm9nbycx4BANkZABl8OgEyVDk1AtOL7uwEa81bOossl6VrRhTZAyfZBCF8PrIKQZCYYEhydcy08jZCnjuqbvgWs' \
                      'ZCowTcSaRg9UmqZBioXvg6gNwviYciaT3Vo0xnR7ijpL3yv6oxr7ZA5OcvAxyGxGlpQPwZAKWga8QkTlFFOZCZBwZDZD'
facebook_pageToken = "EAADm9nbycx4BAJ9ZCAOaFZAp07eBWcZAJiR25iYZAzdYO8kZCnUQqZB8JWMeSk33KPBAZAGuyOrpnfipWIrzOTTDmj" \
                     "NjmDQyDqDdrW6zODQbr6wSF77xao0ybZA8ub9wEeKl9cKscxkn5IWPiMAVxiI4cLkbLwl2ATv340oLcDbS4AZDZD"

page_ID = 345279809417210


@app.route('/shutdown', methods=['GET'])
def shutdown():
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    close_driver(driver)

    shutdown_server()
    return render_template("Shutdown.html")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def homePage():
    if request.method == 'POST':
        if request.form['bsubmit'] == 'Twitter':
            return redirect('/LoginChoice', code=303)
        if request.form['bsubmit'] == 'Facebook':
            return redirect('/FacebookResults', code=303)
        if request.form['bsubmit'] == 'Instagram':
            return redirect('/InstagramResults', code=303)


@app.route('/LoginChoice')
def TwitterChoiceRender():
    return render_template('twitterChoice.html')


@app.route('/LoginChoice', methods=['POST'])
def TwitterChoice():
    if request.method == 'POST':
        if request.form['bsubmit'] == 'Login and Search':
            return redirect('/LoginTwitter', code=303)
        if request.form['bsubmit'] == 'Search User':
            return redirect('/SearchTwitter', code=303)


@app.route('/SearchTwitter')
def SearchTwitterRender():
    return render_template("SearchTwitter.html")


@app.route("/SearchTwitter", methods=['POST'])
def SearchTwitterResult():
    twitter_results = []

    if request.method == "POST":
        if request.form['bsubmit'] == "Search":
            fromDate = request.form['FromDate']
            toDate = request.form['ToDate']
            username = request.form['username']
            hashtag = request.form['Hashtag']

            print(fromDate)
            print(toDate)

            page_source = Search_Specific_User(driver, username, fromDate, toDate, hashtag)

            if page_source != None:
                for item in extract_tweets(page_source):
                    twitter_results.append(item)
            elif page_source == None:
                win32api.MessageBox(0, "No tweets were found.", "Search Unsuccessful", 0x00001000)
                return render_template("SearchTwitter.html")

    # Twitter results
    session['totalTweetValues'] = twitter_results[0]
    session['totalTweetRetweets'] = twitter_results[1]
    session['totalTweetFavourites'] = twitter_results[2]
    session['totalTweetReplies'] = twitter_results[3]
    session['totalNumofTweets'] = twitter_results[4]

    return redirect("/SearchTwitterResults")


@app.route("/SearchTwitterResults", methods=['POST'])
def SearchTwitterROIResult():
    totalTweetValues = session['totalTweetValues']
    totalTweetRetweets = session['totalTweetRetweets']
    totalTweetFavourites = session['totalTweetFavourites']
    totalTweetReplies = session['totalTweetReplies']
    totalNumofTweets = session['totalNumofTweets']

    def DeletePrevChart():
        os.remove('static/SearchTwitterROIplot.png')

    def create_Chart():
        ys = [session['totalTweetRetweets'], session['totalTweetFavourites'], session['totalTweetReplies']]
        xs = ["Retweets", "Favourites", "Replies"]
        colors = ['red', 'lightblue', 'green']
        plt.pie(ys, startangle=90, autopct='%.1f%%', shadow=True, colors=colors,
                wedgeprops={"edgecolor": "black", 'linewidth': 1, 'linestyle': 'solid', 'antialiased': True},
                pctdistance=0.9, )
        plt.title('Metrics')
        plt.legend(loc='center left', labels=xs)
        # plt.tight_layout()
        plt.savefig('static/SearchTwitterROIplot.png')

    my_file = Path('static/SearchTwitterROIplot.png')

    # Check if Plot already exists or not to prevent overlap of PNG files
    if my_file.is_file():
        # Delete the Plot
        DeletePrevChart()
    else:
        create_Chart()

    if request.method == "POST":
        if request.form['bsubmit'] == "Calculate ROI":
            return render_template("TwitterROI.html",
                                   totalTweetValues=totalTweetValues,
                                   totalTweetRetweets=totalTweetRetweets,
                                   totalTweetFavourites=totalTweetFavourites,
                                   totalTweetReplies=totalTweetReplies,
                                   totalNumofTweets=totalNumofTweets)


@app.route('/LoginTwitter')
def loginTwitterRender():
    return render_template("loginTwitter.html")


@app.route('/LoginTwitter', methods=['POST'])
def loginTwitter():
    session['username'] = request.form['username']
    session['password'] = request.form['password']

    if request.method == 'POST':
        if request.form['bsubmit'] == "Log in":
            error = None
            login_twitter(driver, session['username'], session['password'])
            FailedLoginMessage = "//span[contains(.,'The username and password you entered did not match our " \
                                 "records. Please double-check and try again.')]"
            SuccessfulLogin = "//div[contains(@aria-labelledby,'tweet-box-home-timeline-label')]"
            try:
                driver.find_element_by_xpath(FailedLoginMessage)
            except NoSuchElementException:
                return redirect("LoginTwitterSuccess", code=303)
            win32api.MessageBox(0, "Login was unsuccessful, please try again", "Login Unsuccessful", 0x00001000)
            return render_template("loginTwitter.html")


@app.route("/LoginTwitterSuccess")
def twitter_success():
    return render_template('loginSuccessTwitter.html')


@app.route("/LoginTwitterSuccess", methods=["POST"])
def twitter_login_success():
    # Twitter Data
    twitter_results = []

    if request.method == "POST":
        if request.form['bsubmit'] == "Search":
            fromDate = request.form['FromDate']
            toDate = request.form['ToDate']

            page_source = Search_logged_in_User(driver, "@" + session['username'], fromDate, toDate)

            if page_source != None:
                for item in extract_tweets(page_source):
                    twitter_results.append(item)

                # find and click drop down containing log out
                LogoutBox = '//*[@id="user-dropdown-toggle"]'
                driver.find_element_by_xpath(LogoutBox).click()

                # finding and clicking log out
                Logout = "/html/body/div[2]/div[1]/div[2]/div/div/div[3]/ul/li[1]/div/ul/li[13]/button"
                driver.find_element_by_xpath(Logout).click()

            elif page_source == None:
                win32api.MessageBox(0, "No tweets were found.", "Search Unsuccessful", 0x00001000)
                return render_template("loginSuccessTwitter.html")

        session['totalTweetValues'] = twitter_results[0]
        session['totalTweetRetweets'] = twitter_results[1]
        session['totalTweetFavourites'] = twitter_results[2]
        session['totalTweetReplies'] = twitter_results[3]
        session['totalNumofTweets'] = twitter_results[4]

        return redirect('/TwitterResults')


@app.route("/TwitterResults")
def TwitterResult():
    # Twitter results
    totalTweetRetweets = session['totalTweetRetweets']
    totalTweetFavourites = session['totalTweetFavourites']
    totalTweetReplies = session['totalTweetReplies']
    totalNumofTweets = session['totalNumofTweets']

    return render_template("resultsTwitter.html",
                           totalTweetRetweets=totalTweetRetweets,
                           totalTweetFavourites=totalTweetFavourites,
                           totalTweetReplies=totalTweetReplies,
                           totalNumofTweets=totalNumofTweets)


@app.route("/TwitterResults", methods=['POST'])
def TwitterROIResult():
    totalTweetValues = session['totalTweetValues']
    totalTweetRetweets = session['totalTweetRetweets']
    totalTweetFavourites = session['totalTweetFavourites']
    totalTweetReplies = session['totalTweetReplies']
    totalNumofTweets = session['totalNumofTweets']

    def DeletePrevChart():
        os.remove('static/TwitterROIplot.png')

    def create_Chart():
        ys = [session['totalTweetRetweets'], session['totalTweetFavourites'], session['totalTweetReplies']]
        xs = ["Retweets", "Favourites", "Replies"]
        colors = ['red', 'lightblue', 'green']
        plt.pie(ys, startangle=90, autopct='%.1f%%', shadow=True, colors=colors,
                wedgeprops={"edgecolor": "black", 'linewidth': 1, 'linestyle': 'solid', 'antialiased': True},
                pctdistance=0.9, )
        plt.title('Metrics')
        plt.legend(loc='center left', labels=xs)
        # plt.tight_layout()
        plt.savefig('static/TwitterROIplot.png')

    my_file = Path('static/TwitterROIplot.png')

    # Check if Plot already exists or not to prevent overlap of PNG files
    if my_file.is_file():
        # Delete the Plot
        DeletePrevChart()
    else:
        create_Chart()

    if request.method == "POST":
        if request.form['bsubmit'] == "Calculate ROI":
            return render_template("TwitterROI.html",
                                   totalTweetValues=totalTweetValues,
                                   totalTweetRetweets=totalTweetRetweets,
                                   totalTweetFavourites=totalTweetFavourites,
                                   totalTweetReplies=totalTweetReplies,
                                   totalNumofTweets=totalNumofTweets)


@app.route("/FacebookResults")
def FacebookResult():
    # Facebook Data

    facebookResults = []

    for item in extract_Facebook_posts():
        facebookResults.append(item)

    session['totalFacebookValue'] = facebookResults[2]
    session['totalFacebookPosts'] = facebookResults[3]
    session['totalFacebookComments'] = facebookResults[1]
    session['totalFacebookReactions'] = facebookResults[0]

    return render_template('resultsFacebook.html',
                           # Facebook Results
                           totalFacebookValue=session['totalFacebookValue'],
                           totalFacebookReactions=session['totalFacebookReactions'],
                           totalFacebookComments=session['totalFacebookComments'],
                           totalFacebookPosts=session['totalFacebookPosts']
                           )


@app.route("/FacebookResults", methods=['POST'])
def FacebookROIResult():
    totalFacebookValue = session['totalFacebookValue']
    totalFacebookPosts = session['totalFacebookPosts']
    totalFacebookComments = session['totalFacebookComments']
    totalFacebookReactions = session['totalFacebookReactions']

    def create_Chart():
        ys = [session['totalFacebookComments'], session['totalFacebookReactions']]
        xs = ["Comments", "Reactions"]
        colors = ['red', 'lightblue']
        plt.pie(ys, startangle=90, autopct='%.1f%%', shadow=True, colors=colors,
                wedgeprops={"edgecolor": "black", 'linewidth': 1, 'linestyle': 'solid', 'antialiased': True},
                pctdistance=0.9, )
        plt.title('Metrics')
        plt.legend(loc='center left', labels=xs)
        # plt.tight_layout()
        plt.savefig('static/FacebookROIplot.png')

    create_Chart()

    if request.method == "POST":
        if request.form['bsubmit'] == "Calculate ROI":
            return render_template("FacebookROI.html",
                                   totalFacebookValue=totalFacebookValue,
                                   totalFacebookPosts=totalFacebookPosts,
                                   totalFacebookComments=totalFacebookComments,
                                   totalFacebookReactions=totalFacebookReactions)


@app.route("/InstagramResults")
def InstagramResult():
    # Facebook Data

    InstagramResults = []

    for item in extract_insta_posts():
        InstagramResults.append(item)

    session['totalInstagramValue'] = InstagramResults[1]
    session['totalInstagramPosts'] = InstagramResults[0]
    session['totalInstagramComments'] = InstagramResults[3]
    session['totalInstagramLikes'] = InstagramResults[2]

    return render_template('resultsInstagram.html',
                           # Instagram Results
                           totalInstagramValue=session['totalInstagramValue'],
                           totalInstagramLikes=session['totalInstagramLikes'],
                           totalInstagramComments=session['totalInstagramComments'],
                           totalInstagramPosts=session['totalInstagramPosts']
                           )


@app.route("/InstagramResults", methods=['POST'])
def InstagramROIResult():
    def create_Chart():
        ys = [session['totalInstagramComments'], session['totalInstagramLikes']]
        xs = ["Comments", "Likes"]
        colors = ['red', 'lightblue']
        plt.pie(ys, startangle=90, autopct='%.1f%%', shadow=True, colors=colors,
                wedgeprops={"edgecolor": "black", 'linewidth': 1, 'linestyle': 'solid', 'antialiased': True},
                pctdistance=0.9, )
        plt.title('Metrics')
        plt.legend(loc='center left', labels=xs)
        # plt.tight_layout()
        plt.savefig('static/InstagramROIplot.png')

    create_Chart()

    if request.method == "POST":
        if request.form['bsubmit'] == "Calculate ROI":
            return render_template("InstagramROI.html",
                                   totalInstagramValue=session['totalInstagramValue'],
                                   totalInstagramLikes=session['totalInstagramLikes'],
                                   totalInstagramComments=session['totalInstagramComments'],
                                   totalInstagramPosts=session['totalInstagramPosts'])


def notResponding():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex(('127.0.0.1', 5000))


class OpenBrowser(threading.Thread):
    def __init__(self):
        super(OpenBrowser, self).__init__()

    def run(self):
        while notResponding():
            print('Did not respond')
        print('Responded')
        webbrowser.open_new('http://127.0.0.1:5000/')


if __name__ == "__main__":
    browser = OpenBrowser()

    browser.start()

    app.run(debug=False)
