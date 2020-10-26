from nlp.sentiment_analysis import Model, Algorithm
from nlp.twitter import Tweets


def run_sentimet_analyzer(query):
    rebuild = False
    sample_size_for_model = 500
    size_of_actual_tweets = 50

    print(f'running sentiment analyzer with:\n'
          f'\t{rebuild=}, {sample_size_for_model=}, {size_of_actual_tweets=}')

    algorithm = Algorithm()
    model = Model(algorithm, rebuild=rebuild, sample_size=sample_size_for_model)
    algorithm.model = model
    model.run()

    print(f'\nobtaining actual tweets from twitter.com')
    tweets = Tweets(query, size=size_of_actual_tweets)
    real_tweets = tweets.get_tweets_list()

    print(f'processing actual tweets')
    processed_tweets = algorithm.process_tweets(real_tweets)

    print(f'predicting sentiment for all tweets\n')
    res_dict = algorithm.predict_sentiment(processed_tweets)

    print(f'\n\nsample output: {res_dict=}')
    return res_dict


run_sentimet_analyzer('vote')
