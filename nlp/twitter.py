import tweepy, time


class Tweets():
    def __init__(self, text_query, size=100):
        self.__text_query = text_query
        self.__count = size
        self.__api = None
        self.tweets_list = []
        self.__run()

    def get_tweets_list(self):
        return self.tweets_list

    def __run(self):
        self.__set_api()
        self.__get_tweets()

    def __set_api(self):
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.__api = tweepy.API(auth, wait_on_rate_limit=True)

    def __get_tweets(self):
        try:
            # create query from tweet api search.
            # limits to english, self.__count number of tweet
            quries = tweepy.Cursor(self.__api.search, q=self.__text_query, lang='en',
                                   tweet_mode='extended', result_type='recent').items(self.__count)

            for tweet_status in quries:
                self.__get_full_text(tweet_status)

        except BaseException as e: # error getting tweets
            print('failed __get_tweets,', str(e))
            time.sleep(3)

    def __get_full_text(self, status):
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            if hasattr(status, "retweeted_status"):  # Check if Retweet
                self.tweets_list.append(f'{status.retweeted_status.full_text}')
            else:
                self.tweets_list.append(f'{status.full_text}')
