from spacy.tokenizer import Tokenizer
from spacy.lang.en import English, stop_words
from nltk.corpus import twitter_samples
import nltk, re


class Model():
    def __init__(self):
        self.model_nlp = English()
        self.__get_labeled_tweets('positive_tweets.json')

    def __get_labeled_tweets(self, file_name):
        raw_tweets = [' '.join(tokens) for tokens in twitter_samples.tokenized(file_name)]
        tokenized_tweets = []
        for tweet in raw_tweets:
            tokenized_tweets.append(self.model_nlp(tweet))

        for tokens in tokenized_tweets:
            self.__remove_surplus(tokens)
            self.__lemmatize(tokens)
            self.__remove_stop_words(tokens)

    def __remove_surplus(self, tokens):
        '''
        remove surplus tokens from given tokens
        :param tokens: list of token
        '''
        for token in tokens[:]:
            # remove mention @ from tokens
            mention_pattern = r'@\w+'
            if re.match(mention_pattern, token):
                tokens.remove(token)

            # remove link http... from tokens
            link_pattern = r'http[s]?://[\w|.|/]+'
            if re.match(link_pattern, token):
                tokens.remove(token)

    def __lemmatize(self, tokens):
        pass

    def __remove_stop_words(self, tokens):

        pass



model = Model()