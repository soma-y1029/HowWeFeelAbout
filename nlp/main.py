from nlp.sentiment_analysis import Model, Algorithm
from nlp.twitter import Tweets


# @staticmethod
def run_sentimet_analyzer(query):
    print('run model')
    algorithm = Algorithm()
    model = Model(algorithm, rebuild=True)
    algorithm.model = model
    model.run()

    tweets = Tweets(query)
    real_tweets = tweets.get_tweets_list()

    processed_tweets = algorithm.process_tweets(real_tweets)
    # model.text_classifier.predict(processed_tweets)


    return 75

run_sentimet_analyzer('test')