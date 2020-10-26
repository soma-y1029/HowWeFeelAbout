import pickle
import re
import spacy
import string

# twitter samples form nltk
from nltk.corpus import twitter_samples, stopwords

# sklearn library to build model and classify the tweets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

SPACY_DIR = '/Users/somayoshida/.local/share/virtualenvs/HowWeFeelAbout-hlN-1I0m/lib/python3.8/site-packages/en_core_web_sm/en_core_web_sm-2.3.1'


class Model:
    def __init__(self, rebuild=False):
        """
        Constructor
        """
        self.text_classifier = None
        self.algorithm = Algorithm()

        if rebuild:  # build model from nltk sample tweets
            print('building model')
            self.__build_model()

        else:  # load from file
            print('loading model')
            with open('text_classifier', 'rb') as training_model:
                self.text_classifier = pickle.load(training_model)

    def __build_model(self):
        pos_samples = self.algorithm.get_labeled_tweets('positive_tweets.json')
        neg_samples = self.algorithm.get_labeled_tweets('negative_tweets.json')

        pos_samples = [' '.join(tweet) for tweet in pos_samples]
        neg_samples = [' '.join(tweet) for tweet in neg_samples]

        # vectorizer = TfidfVectorizer(max_features=2500, min_df=7, max_df=0.8, stop_words=stopwords.words('english'))
        vectorizer = TfidfVectorizer(max_features=2500)
        samples = vectorizer.fit_transform(pos_samples + neg_samples).toarray()
        # neg_samples = vectorizer.fit_transform(neg_samples).toarray()

        labels = [1] * len(pos_samples) + [0] * len(neg_samples)

        text_train, text_test, label_train, label_test = \
            train_test_split(samples, labels, test_size=0.2, random_state=0)
        self.text_classifier = RandomForestClassifier(n_estimators=200, random_state=0)
        self.text_classifier.fit(text_train, label_train)
        predictions = self.text_classifier.predict(text_test)

        print(accuracy_score(label_test, predictions))
        print('writing model')
        with open('text_classifier', 'wb') as picklefile:
            pickle.dump(self.text_classifier, picklefile)


class Algorithm:
    def __init__(self):
        self.__model_nlp = spacy.load(SPACY_DIR)

    def get_labeled_tweets(self, file_name):
        """
        Get labeled tweets from nltk
        :param file_name: name of file in string
        :return: cleaned list of lists that contain tokens for each tweets
        """
        raw_tweets = [' '.join(tokens) for tokens in twitter_samples.tokenized(file_name)[:100]]
        # print(raw_tweets) # show raw tweets sample form nltk
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
