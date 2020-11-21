import time

from nlp.sentiment_analysis import Model, Algorithm
from nlp.twitter import Tweets
from decouple import config


def run_sentiment_analyzer(query):
    """
    Driver method of nlp to run sentiment analyzer
    :param query: query to be searched
    :return: dictionary of data
    """
    start_time = time.time()

    # values to be adjusted
    rebuild = config('rebuild') in ('True', )
    sample_size_for_model = int(config('sample_size_for_model'))
    size_of_actual_tweets = int(config('size_of_actual_tweets'))  # the tweets are only upto 7 past-days

    consumer_key = config('CONSUMER_KEY')
    consumer_secret = config('CONSUMER_SECRET')
    access_token = config('ACCESS_TOKEN')
    access_token_secret = config('ACCESS_TOKEN_SECRET')
    spacy_dir = config('SPACY_DIR')

    print(f'running sentiment analyzer with:\n'
          f'\t{rebuild=}, {sample_size_for_model=}, {size_of_actual_tweets=}')

    # create and run modules for text classification
    algorithm = Algorithm(spacy_dir)

    classification_model = Model(algorithm, rebuild=rebuild, sample_size=sample_size_for_model)
    algorithm.model = classification_model
    classification_model.run_model()

    # obtain tweets with query from twitter.com
    print(f'\nobtaining actual tweets from twitter.com')
    tweets = Tweets(query, size=size_of_actual_tweets)
    real_tweets = tweets.tweets_list
    tweets.set_keys(consumer_key, consumer_secret, access_token, access_token_secret)
    tweets.run()

    # process the obtained data from twitter
    print(f'processing actual tweets')
    processed_tweets = algorithm.process_tweets(real_tweets)

    # predict sentiment by running algorithm and get output
    print(f'predicting sentiment for all tweets\n')
    res_dict = algorithm.predict_sentiment(processed_tweets, real_tweets)

    # return the res_dict that contains information about the sentiment analysis and the result
    print(f'\n\nsample output: {res_dict=}')

    print(f'\n\n {time.time()-start_time}')
    return res_dict
