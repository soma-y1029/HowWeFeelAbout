from nlp.sentiment_analysis import Model, Algorithm
from nlp.twitter import Tweets

# @staticmethod
def run_sentimet_analyzer(query):
    print('run model')
    algorithm = Algorithm()
    model = Model(algorithm, rebuild=True, sample_size=500)
    algorithm.model = model
    model.run()

    tweets = Tweets(query, size=10)
    real_tweets = tweets.get_tweets_list()

    processed_tweets = algorithm.process_tweets(real_tweets)
    res_dict = algorithm.predict_sentiment(processed_tweets)

    return res_dict

# run_sentimet_analyzer('vote')