import tweepy
import time


class Tweets:
    """
    Tweets class that gain tweets with provided query form twitter.com
    """
    def __init__(self, text_query, size=100):
        """
        Constructor of Tweets
        :param text_query: query to be searched
        :param size: size of tweet to be obtained from twitter
        """
        self.__text_query = text_query
        self.__count = size
        self.__api = None
        self.__tweets_list = []

        # developer account keys
        self.__consumer_key = ''
        self.__consumer_secret = ''
        self.__access_token = ''
        self.__access_token_secret = ''

    @property
    def tweets_list(self):
        """
        Property of tweets_list
        :return: tweets_list
        """
        return self.__tweets_list

    def run(self):
        """
        Run two methods to obtain tweets
        :return: None
        """
        self.__set_api()
        self.__get_tweets()

    def set_keys(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret
        self.__access_token = access_token
        self.__access_token_secret = access_token_secret

    def __set_api(self):
        """
        Set api with keys
        :return: None
        """
        # authentication of twitter developer account
        auth = tweepy.OAuthHandler(self.__consumer_key, self.__consumer_secret)
        auth.set_access_token(self.__access_token, self.__access_token_secret)
        self.__api = tweepy.API(auth, wait_on_rate_limit=True)

    def __get_tweets(self):
        """
        Get tweets with query from twitter
        :return: None
        """
        try:
            # create query from tweet api search.
            # limits to english, self.__count number of tweet
            quries = tweepy.Cursor(self.__api.search, q=self.__text_query, lang='en',
                                   tweet_mode='extended', result_type='recent').items(self.__count)

            # get status from quries and get full text from tweet_status
            for tweet_status in quries:
                self.__get_full_text(tweet_status)

        except BaseException as e: # error getting tweets
            print('failed __get_tweets,', str(e))
            time.sleep(3)

    def __get_full_text(self, status):
        """
        Get full text based on the tweet status
        :param status: status of a tweet
        :return: None
        """
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            if hasattr(status, "retweeted_status"):  # Check if Retweet
                self.__tweets_list.append(f'{status.retweeted_status.full_text}')
            else:
                self.__tweets_list.append(f'{status.full_text}')
