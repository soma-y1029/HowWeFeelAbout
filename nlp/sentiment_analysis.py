import pickle
import re
import spacy
import string

# twitter samples form nltk
from nltk.corpus import twitter_samples

# sklearn library to build model and classify the tweets
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB


class Model:
    """
    Model class that holds model of the sentiment analysis algorithm
    """
    def __init__(self, algorithm, rebuild=False, sample_size=5000):
        """
        Constructor of Model
        """
        self.__text_classifier = None
        self.__algorithm = algorithm
        self.__rebuild = rebuild
        self.__sample_size = sample_size

    @property
    def text_classifier(self):
        """
        Property of text_classifier
        :return: text_classifier
        """
        return self.__text_classifier

    @property
    def algorithm(self):
        """
        Property of algorithm
        :return: algorithm
        """
        return self.__algorithm

    def run_model(self):
        """
        Run this model based on the status of rebuild
        :return: None
        """
        if self.__rebuild:  # build model from nltk sample tweets
            self.__set_model()
            self.__save_to_file()

        else:  # load from file
            self.__load_file()

    def __set_model(self):
        """
        Build model for sentiment analysis
        :return: None
        """
        print('building model')
        # data preparation
        tweet_samples = self.__get_labeled_tweets() # list of cleaned string tweets
        labels = [1] * self.__sample_size + [0] * self.__sample_size
        docs_train, docs_test, y_train, y_test = train_test_split(tweet_samples, labels,
                                                                  test_size=0.20, random_state=12)

        # transform train text data to analyze frequency of terms
        docs_train_counts = self.algorithm.tweetVzer.fit_transform(docs_train)
        # Convert raw frequency counts into TF-IDF valuesa
        docs_train_tfidf = self.algorithm.tweetTfmer.fit_transform(docs_train_counts)

        # testing data
        # Using the fitted vectorizer and transformer, tranform the test data
        docs_test_counts = self.algorithm.tweetVzer.transform(docs_test)
        docs_test_tfidf = self.algorithm.tweetTfmer.transform(docs_test_counts)

        self.__build_classifier(docs_train_tfidf, docs_test_tfidf, y_train, y_test)

    def __build_classifier(self, docs_train_tfidf, docs_test_tfidf, y_train, y_test):
        """
        Building classifier with Multi-nominal Naive Bayes
        :param docs_train_tfidf: tfidf for training
        :param docs_test_tfidf: tfidf for testing
        :param y_train: label for training
        :param y_test: label for testing
        :return: None
        """
        # Build model with Multinominal Naive Bayes
        # Train a Multimoda Naive Bayes classifier. Again, we call it "fitting"
        self.__text_classifier = MultinomialNB()
        self.text_classifier.fit(docs_train_tfidf, y_train)

        # make prediction with the testing data
        y_pred = self.text_classifier.predict(docs_test_tfidf)
        # print accuracy based on this model
        print(f'the accuracy for this model testing: {accuracy_score(y_test, y_pred)}')

    def __save_to_file(self):
        """
        Save data to file for future use
        :return: Nonen
        """
        print('writing data to files')
        with open('text_classifier', 'wb') as file:
            pickle.dump(self.text_classifier, file)

        with open('tweetVzer', 'wb') as file:
            pickle.dump(self.algorithm.tweetVzer, file)

        with open('tweetTfmer', 'wb') as file:
            pickle.dump(self.algorithm.tweetTfmer, file)

    def __load_file(self):
        """
        Load data from file if rebuild is false
        :return: None
        """
        print('loading data from file')

        with open('text_classifier', 'rb') as file:
            self.__text_classifier = pickle.load(file)

        with open('tweetVzer', 'rb') as file:
            self.algorithm.tweetVzer = pickle.load(file)

        with open('tweetTfmer', 'rb') as file:
            self.algorithm.tweetTfmer = pickle.load(file)

    def __get_labeled_tweets(self):
        """
        Get labeled tweets from nltk
        :return: cleaned list of lists that contain tokens for each tweets
        """
        pos_samples = twitter_samples.strings('positive_tweets.json')[:self.__sample_size]
        neg_samples = twitter_samples.strings('negative_tweets.json')[:self.__sample_size]
        # print(pos_samples+neg_samples) # show raw tweets sample form nltk

        return self.algorithm.process_tweets(pos_samples+neg_samples)


class Algorithm:
    """
    Algorithm class that hodls algorithms to process sentiment analysis
    """

    def __init__(self, spacy_dir):
        """
        Constructor
        """
        self.__model_nlp = spacy.load(spacy_dir)
        self.__model = None
        self.__tweetVzer = CountVectorizer(min_df=2, max_features=3000)
        self.__tweetTfmer = TfidfTransformer()

    @property
    def tweetVzer(self):
        return self.__tweetVzer

    @property
    def tweetTfmer(self):
        return self.__tweetTfmer

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, classification_model):
        self.__model = classification_model

    @tweetVzer.setter
    def tweetVzer(self, tweetVzer):
        self.__tweetVzer = tweetVzer

    @tweetTfmer.setter
    def tweetTfmer(self, tweetTfmer):
        self.__tweetTfmer = tweetTfmer

    def predict_sentiment(self, processed_tweets, real_tweets):
        """
        Predict sentiment with model and given tweets
        :param processed_tweets: cleaned tweets
        :param real_tweets: unprocessed tweets for returning information
        :return: dictionary of the result with process information
        """
        tweets_counts = self.tweetVzer.transform(processed_tweets)  # turn text into count vector
        tweets_tfidf = self.tweetTfmer.transform(tweets_counts)  # turn into tfidf vector

        # have classifier make a prediction
        pred = self.model.text_classifier.predict(tweets_tfidf)
        pos_tweets, neg_tweets = [], [] # holds tweets for returning

        # print out results
        for tweet, category, i in zip(processed_tweets, pred, range(len(pred))):
            # print(f'{tweet=}, \t{category=}')
            # store 10 sample data
            if category and len(pos_tweets) < 10:
                pos_tweets.append(real_tweets[i])
            elif len(neg_tweets) < 10:
                neg_tweets.append(real_tweets[i])

        # create dictionary to be returned with information
        res_dict = dict()
        res_dict['Positiveness'] = sum(pred)/len(pred)*100
        res_dict['Positive_tweets'] = pos_tweets[:]
        res_dict['Negative_tweets'] = neg_tweets[:]
        res_dict['Num_actual_tweets'] = len(processed_tweets)

        return res_dict

    def process_tweets(self, tweets):
        """
        process tweets to be used in algorithm
        :param tweets: tweets to be processed
        :return: processed algorithm-use-ready tweets
        """
        tweets = self.__clean_tweets(tweets)
        tweets = [' '.join(tweet) for tweet in tweets]
        return tweets

    def __clean_tweets(self, raw_tweets):
        """
        clean given tweets
        :param raw_tweets: list of strings
        :return: cleaned tokenized tweets
        """
        tokenized_tweets = []

        # obtain tokenizer object for each tweets from raw_tweets
        for tweet in raw_tweets:
            tokenized_tweets.append(self.__model_nlp(tweet))

        cleaned_list = []
        # for each tokenized tweet, perform operations
        for tweet in tokenized_tweets:
            cleaned_tweet_tokens = []  # temporarily store filtered tokens for tweet
            for token in tweet:
                if Algorithm.__is_surplus(token):  # skip if this is surplus
                    continue
                # append only if token is not stop words
                if not token.is_stop:
                    cleaned_tweet_tokens.append(token.lemma_.lower())
            cleaned_list.append(cleaned_tweet_tokens)

        return cleaned_list

    @staticmethod
    def __is_surplus(token):
        """
        check if given token is surplus or not
        :param token: Doc object from tokenizer
        :return: True if this token is surplus
        """
        # remove mention @ from tokens
        mention_pattern = r'(@\w+)|(#)'
        if re.match(mention_pattern, token.text):
            return True

        # remove link http... from tokens
        link_pattern = r'http[s]?://[\w|.|/]+'
        if re.match(link_pattern, token.text):
            return True

        # remove token consists of only nums
        nums_only_pattern = r'^[0-9]+$'
        if re.match(nums_only_pattern, token.text):
            return True

        if token.text in string.punctuation:
            return True

        return False