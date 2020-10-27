from nlp.sentiment_analysis import Model, Algorithm
from nlp.twitter import Tweets


def run_sentiment_analyzer(query):
    """
    Driver method to run sentiment analyzer
    :param query: query to be searched
    :return: dictionary of data
    """
    # values to be adjusted
    rebuild = False
    sample_size_for_model = 500
    size_of_actual_tweets = 200 # the tweets are only upto 7 past-days

    print(f'running sentiment analyzer with:\n'
          f'\t{rebuild=}, {sample_size_for_model=}, {size_of_actual_tweets=}')

    # create and run modules for text classification
    algorithm = Algorithm()
    classification_model = Model(algorithm, rebuild=rebuild, sample_size=sample_size_for_model)
    algorithm.model = classification_model
    classification_model.run_model()

    # obtain tweets with query from twitter.com
    print(f'\nobtaining actual tweets from twitter.com')
    tweets = Tweets(query, size=size_of_actual_tweets)
    real_tweets = tweets.tweets_list

    # process the obtained data from twitter
    print(f'processing actual tweets')
    processed_tweets = algorithm.process_tweets(real_tweets)

    # predict sentiment by running algorithm and get output
    print(f'predicting sentiment for all tweets\n')
    res_dict = algorithm.predict_sentiment(processed_tweets, real_tweets)

    # return the res_dict that contains information about the sentiment analysis and the result
    print(f'\n\nsample output: {res_dict=}')
    return res_dict


run_sentiment_analyzer('vote')
