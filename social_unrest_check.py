import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import pandas as pd
# from textblob import TextBlob
# import re
from langdetect import detect
from analysis import TweetAnalyzer
#Analysing the individual tweets:
def run_analysis(Tweets):
    tweet_analysis = TweetAnalyzer()
    for i in Tweets:
        print(i)
        print("###############################################################################")
    print('no of tweets: ',len(Tweets))
    data_synthesized = [tweet_analysis.clean_tweet(tweet) for tweet in Tweets]
    print('data synthesize length: ',len(data_synthesized))
    print(data_synthesized)
    sentiments = [tweet_analysis.analysis_sentiment(tweet) for tweet in Tweets]
    print(f"1: {sentiments.count(1)}, 0: {sentiments.count(0)}, -1: {sentiments.count(-1)}")
    try:
        negativity = sentiments.count(-1)/(sentiments.count(1)+sentiments.count(-1))
    except ZeroDivisionError:
        return (0,1)
    if negativity<0.2:
        return(1,negativity)
    return tweet_analysis.social_unrest_evaluate(data_synthesized,sentiments,negativity)

#Scraping tweets from twitter
def scrape_tweets(driver):
    Tweets = []
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    for article in articles:
        tweet_text = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
        Tweets.append(tweet_text)
        
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    print("scraper_tweet, sleeping")
    sleep(3)
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    Tweets[:] = list(set(Tweets))  # Remove duplicates in-place
    
    return Tweets

def scrape_caller(keyword):
    print(f"keyword is :{keyword}, its type is {type(keyword)}")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    PATH = "C:\Program Files\driver\chromedriver.exe"
    print("Path selected")
    driver = webdriver.Chrome(PATH,options=chrome_options)
    print('driver initiated')

    url ='https://twitter.com/explore'
    driver.get(url)
    print('driver.get ho gya')

    # username = driver.find_element(By.XPATH,"//input[@name='text']")
    username = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
    username.send_keys("@AjaySin14354883")
    next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
    next_button.click()
    print("next button clicked")
    print("sleeping for 3 sec")
    sleep(3)

    password = driver.find_element(By.XPATH,"//input[@name='password']")
    password.send_keys('ajaysingh11')
    log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
    log_in.click()

    subject = keyword
    print("sleeping for 3 sec")
    sleep(3)
    search_box = driver.find_element(By.XPATH,"//input[@data-testid='SearchBox_Search_Input']")
    search_box.send_keys(subject)
    search_box.send_keys(Keys.ENTER)

    # Initialize variables
    Tweets = []
    # Specify the total number of scraping rounds
    num_rounds = 5
    interval = 3  # seconds

    for _ in range(num_rounds):
        print("running loop")
        Tweets.append(scrape_tweets( driver))
        sleep(interval)

    # Close the driver when done
    driver.quit()
    tweet_list = [element for sublist in Tweets for element in sublist]
    return tweet_list

# if __name__ =='__main__':
#      keyword = 'manipur'
#      tweets = scrape_caller(keyword)
#      print("Tweets gathered, Now analysing...")
#      run_analysis(tweets[1])




