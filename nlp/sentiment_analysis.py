import pickle
import re
import spacy
import string

# twitter samples form nltk
from nltk.corpus import twitter_samples

# sklearn library to build model and classify the tweets
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB

SPACY_DIR = 'en'


class Model:
    def __init__(self, algorithm, rebuild=False):
        """
        Constructor
        """
        self.__text_classifier = None
        self.__algorithm = algorithm
        self.__rebuild = rebuild
        self.__sample_size = 50

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

        else:  # load from file
            print('loading model')
            with open('text_classifier', 'rb') as training_model:
                self.__text_classifier = pickle.load(training_model)

    def __build_model(self):
        samples = self.__get_labeled_tweets() # list of cleaned string tweets
        labels = [1] * self.__sample_size + [0] * self.__sample_size

        docs_train, docs_test, y_train, y_test = train_test_split(samples, labels,
                                                                  test_size=0.20, random_state=12)

        # initialize CountVectorizer
        tweetVzer = CountVectorizer(min_df=2, max_features=3000)  # use top 3000 words only. 78.25% acc.

        # fit and tranform using training text
        docs_train_counts = tweetVzer.fit_transform(docs_train)

        # Convert raw frequency counts into TF-IDF values
        tweetTfmer = TfidfTransformer()
        docs_train_tfidf = tweetTfmer.fit_transform(docs_train_counts)



        # testing data
        # Using the fitted vectorizer and transformer, tranform the test data
        docs_test_counts = tweetVzer.transform(docs_test)
        docs_test_tfidf = tweetTfmer.transform(docs_test_counts)



        # Build model with Multinominal Naive Bayes
        # Train a Multimoda Naive Bayes classifier. Again, we call it "fitting"
        self.__text_classifier = MultinomialNB()
        self.text_classifier.fit(docs_train_tfidf, y_train)


        # Testing with actuals
        # Predict the Test set results, find accuracy
        y_pred = self.text_classifier.predict(docs_test_tfidf)
        print(accuracy_score(y_test, y_pred))

        # trying the classifier
        # very short and fake movie reviews
        reviews_new = ['This movie was excellent', 'Absolute joy ride',
                       'Steven Seagal was terrible', 'Steven Seagal shone through.',
                       'This was certainly a movie', 'Two thumbs up', 'I fell asleep halfway through',
                       "We can't wait for the sequel!!", '!', '?', 'I cannot recommend this highly enough',
                       'instant classic.', 'Steven Seagal was amazing. His performance was Oscar-worthy.']

        reviews_new_counts = tweetVzer.transform(reviews_new)  # turn text into count vector
        reviews_new_tfidf = tweetTfmer.transform(reviews_new_counts)  # turn into tfidf vector

        # have classifier make a prediction
        pred = self.text_classifier.predict(reviews_new_tfidf)

        # print out results
        print(len(reviews_new), len(pred))
        for review, category in zip(reviews_new, pred):
            print(review, category)


        print('writing model')
        with open('text_classifier', 'wb') as picklefile:
            pickle.dump(self.text_classifier, picklefile)

    def __get_labeled_tweets(self):
        """
        Get labeled tweets from nltk
        :param file_name: name of file in string
        :return: cleaned list of lists that contain tokens for each tweets
        """
        pos_sample = twitter_samples.tokenized('positive_tweets.json')[:self.__sample_size]
        raw_tweets = [' '.join(tokens) for tokens in pos_sample]

        neg_sample = twitter_samples.tokenized('negative_tweets.json')[:self.__sample_size]
        raw_tweets += [' '.join(tokens) for tokens in neg_sample]
        # print(raw_tweets) # show raw tweets sample form nltk

        return self.algorithm.process_tweets(raw_tweets)


class Algorithm:
    def __init__(self):
        self.__model_nlp = spacy.load(SPACY_DIR)
        self.model = None

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
