import time

from nlp.sentiment_analysis import Model, Algorithm
from nlp.twitter import Tweets



def run_sentiment_analyzer(query):
    """
    Driver method to run sentiment analyzer
    :param query: query to be searched
    :return: dictionary of data
    """

    start_time = time.time()

    # values to be adjusted
    rebuild = True
    sample_size_for_model = 5000
    size_of_actual_tweets = 200 # the tweets are only upto 7 past-days

    consumer_key = 'QHDBbSZt7YlCfl7JPWsg5NSih'
    consumer_secret = 'qNTgb8GqKh1kXXTkosQTEd9aPdhxVqilLzAR6q0Je0xJdlzUmX'
    access_token = '1306672127114842113-jAwRNJA1OxgHFfk4c7B8AqLYNox7oh'
    access_token_secret = 'EdJXVxdVuJhrCIuoyLKedMGHenoVibfx9ckf6fk1BJXhO'

    spacy_dir = '/Users/somayoshida/.local/share/virtualenvs/HowWeFeelAbout-hlN-1I0m/lib/python3.8/site-packages/en_core_web_sm/en_core_web_sm-2.3.1'

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



run_sentiment_analyzer('election')