import re
import spacy
import string

from nltk.corpus import twitter_samples

SPACY_DIR = 'en'


class Model():
    def __init__(self):
        """
        Constructor
        """
        self.__model_nlp = spacy.load(SPACY_DIR)

        pos_sample = self.__get_labeled_tweets('positive_tweets.json')
        neg_sample = self.__get_labeled_tweets('negative_tweets.json')

    def __get_labeled_tweets(self, file_name):
        """
        Get labeled tweets from nltk
        :param file_name: name of file in string
        :return: cleaned list of lists that contain tokens for each tweets
        """
        raw_tweets = [' '.join(tokens) for tokens in twitter_samples.tokenized(file_name)[:10]]
        tokenized_tweets = []

        # obtain tokenizer object for each tweets from raw_tweets
        for tweet in raw_tweets:
            tokenized_tweets.append(self.__model_nlp(tweet))

        cleaned_list = []
        # for each tokenized tweet, perform operations
        for tweet in tokenized_tweets:
            cleaned_tweet_tokens = [] # temporarily store filtered tokens for tweet
            for token in tweet:
                if self.__is_surplus(token): # skip if this is surplus
                    continue
                # append only if token is not stop words
                if not token.is_stop:
                    cleaned_tweet_tokens.append(token.lemma_.lower())
            cleaned_list.append(cleaned_tweet_tokens)

        return cleaned_list


    def __is_surplus(self, token):
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


# for testing
model = Model()
