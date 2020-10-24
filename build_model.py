from spacy.lang.en import English, stop_words
from nltk.corpus import twitter_samples
import nltk, re


class Model():
    def __init__(self):
        self.__model_nlp = English()

        self.__tokenizer = self.__model_nlp.Defaults.create_tokenizer(self.__model_nlp)
        res = self.__get_labeled_tweets('positive_tweets.json')
        print(res)

    def __get_labeled_tweets(self, file_name):
        raw_tweets = [' '.join(tokens) for tokens in twitter_samples.tokenized(file_name)[:10]]
        tokenized_tweets = []

        # obtain tokenizer object for each tweets from raw_tweets
        for tweet in raw_tweets:
            # tokenized_tweets.append(self.__tokenizer(tweet))
            tokenized_tweets.append(self.__model_nlp(tweet))

        cleaned_list = []
        # for each tokenized tweet, perform operations
        for tweet in tokenized_tweets:
            cleaned_tweet_tokens = []
            for token in tweet:
                if self.__is_surplus(token):
                    continue
                if not token.is_stop:
                    cleaned_tweet_tokens.append(token.lemma_.lower())
            cleaned_list.append(cleaned_tweet_tokens)

        return cleaned_list

    def __is_surplus(self, token):
        '''
        check if given token is surplus or not
        :param token: Doc object from tokenizer
        :return: True if this token is surplus
        '''
        # remove mention @ from tokens
        mention_pattern = r'(@\w+)|(#)'
        if re.match(mention_pattern, token.text):
            return True

        # remove link http... from tokens
        link_pattern = r'http[s]?://[\w|.|/]+'
        if re.match(link_pattern, token.text):
            return True

        return False




model = Model()