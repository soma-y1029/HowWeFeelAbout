import pickle
import re
import spacy
import string

# twitter samples form nltk
from nltk.corpus import twitter_samples

# sklearn library to build model and classify the tweets
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB

SPACY_DIR = 'en'


class Model:
    def __init__(self, algorithm, rebuild=False, sample_size=5000):
        """
        Constructor
        """
        self.__text_classifier = None
        self.__algorithm = algorithm
        self.__rebuild = rebuild
        self.__sample_size = sample_size

    @property
    def text_classifier(self):
        return self.__text_classifier

    @property
    def algorithm(self):
        return self.__algorithm

    def run(self):
        if self.__rebuild:  # build model from nltk sample tweets
            print('building model')
            self.__build_model()
            self.__save_to_file()

        else:  # load from file
            self.__load_file()

    def __build_model(self):
        tweet_samples = self.__get_labeled_tweets() # list of cleaned string tweets
        labels = [1] * self.__sample_size + [0] * self.__sample_size

        docs_train, docs_test, y_train, y_test = train_test_split(tweet_samples, labels,
                                                                  test_size=0.20, random_state=12)

        # fit and transform using training text
        docs_train_counts = self.algorithm.tweetVzer.fit_transform(docs_train)
        # Convert raw frequency counts into TF-IDF values
        docs_train_tfidf = self.algorithm.tweetTfmer.fit_transform(docs_train_counts)

        # testing data
        # Using the fitted vectorizer and transformer, tranform the test data
        docs_test_counts = self.algorithm.tweetVzer.transform(docs_test)
        docs_test_tfidf = self.algorithm.tweetTfmer.transform(docs_test_counts)
        self.__build_classifier(docs_train_tfidf, docs_test_tfidf, y_train, y_test)

    def __build_classifier(self, docs_train_tfidf, docs_test_tfidf, y_train, y_test):
        # Build model with Multinominal Naive Bayes
        # Train a Multimoda Naive Bayes classifier. Again, we call it "fitting"
        self.__text_classifier = MultinomialNB()
        self.text_classifier.fit(docs_train_tfidf, y_train)

        # Testing with actuals
        # Predict the Test set results, find accuracy
        y_pred = self.text_classifier.predict(docs_test_tfidf)
        print(f'the accuracy for this model testing: {accuracy_score(y_test, y_pred)}')

    def __save_to_file(self):
        print('writing data to files')
        with open('text_classifier', 'wb') as file:
            pickle.dump(self.text_classifier, file)

        with open('tweetVzer', 'wb') as file:
            pickle.dump(self.algorithm.tweetVzer, file)

        with open('tweetTfmer', 'wb') as file:
            pickle.dump(self.algorithm.tweetTfmer, file)

    def __load_file(self):
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
        :param file_name: name of file in string
        :return: cleaned list of lists that contain tokens for each tweets
        """
        pos_samples = twitter_samples.strings('positive_tweets.json')[:self.__sample_size]
        neg_samples = twitter_samples.strings('negative_tweets.json')[:self.__sample_size]
        # print(pos_samples+neg_samples) # show raw tweets sample form nltk

        return self.algorithm.process_tweets(pos_samples+neg_samples)


class Algorithm:
    def __init__(self):
        self.__model_nlp = spacy.load(SPACY_DIR)
        self.model = None

        self.tweetVzer = CountVectorizer(min_df=2, max_features=3000)
        self.tweetTfmer = TfidfTransformer()

    def predict_sentiment(self, processed_tweets):
        tweets_counts = self.tweetVzer.transform(processed_tweets)  # turn text into count vector
        tweets_tfidf = self.tweetTfmer.transform(tweets_counts)  # turn into tfidf vector

        # have classifier make a prediction
        pred = self.model.text_classifier.predict(tweets_tfidf)
        pos_tweets, neg_tweets = [], []

        # print out results
        for review, category in zip(processed_tweets, pred):
            print(f'{review=}, \t{category=}')
            # store 10 sample data
            if category and len(pos_tweets) < 10:
                pos_tweets.append(review)
            elif len(neg_tweets) < 10:
                neg_tweets.append(review)

        # create dictionary to be returned with information
        res_dict = dict()
        res_dict['Positiveness'] = sum(pred)/len(pred)*100
        res_dict['Positive_tweets'] = pos_tweets[:]
        res_dict['Negative_tweets'] = neg_tweets[:]
        res_dict['Num_actual_tweets'] = len(processed_tweets)

        return res_dict

    def process_tweets(self, tweets):
        tweets = self.clean_tweets(tweets)
        tweets = [' '.join(tweet) for tweet in tweets]
        return tweets

    def clean_tweets(self, raw_tweets):
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
