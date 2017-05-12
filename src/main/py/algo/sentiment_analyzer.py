__author__ = 'Amit Mohapatra'

import re
from sets import Set
import logging as log
from os import sep, path
from gc import collect, garbage
from collections import namedtuple

from common.resource_manager import ResourceManager
from common.clean_text_processor import CleanTextProcessor
from pattern_sentiment_analyzer import PatternSentimentAnalyzer


class SentimentAnalyzer(object):
    # Return type declaration. returning a named tuple object.
    RETURN_TYPE = namedtuple('sentiment', ["classification", "polarity",
                                           "subjectivity", "subjectivity_score",
                                           "mood", "modality", "modality_score", "opinion"])

    def __init__(self):
        self._pattern_score = PatternSentimentAnalyzer()
        self.base_path = path.dirname(path.dirname(path.dirname(path.dirname(path.dirname(__file__)))))
        self.pattern = re.compile('\W')
        # Reading the neg_features from resource and store as set in memory.
        self.not_set = ResourceManager.read_file(sep.join([self.base_path, "resources", "neg_features"]))
        # Reading the pos_features from resource and store as set in memory.
        self.pos_set = ResourceManager.read_file(sep.join([self.base_path, "resources", "pos_features"]))

    def sentiment(self, text):

        try:
            # cleaning the text.
            text = CleanTextProcessor.clean_codecs(text)
            text = CleanTextProcessor.clean_escape_codes(text)
            sentence_tokens = CleanTextProcessor.clean_text(text)

            if sentence_tokens:
                pattern_result = self._pattern_score.sentiment(sentence_tokens)

                classification = "positive"
                polarity = 0.0

                if pattern_result.polarity < -0.1:
                    polarity = pattern_result.polarity
                    classification = 'negative'
                elif pattern_result.polarity > 0.1:
                    polarity = pattern_result.polarity
                    classification = 'positive'
                else:
                    all_text = " ".join(sentence_tokens)

                    all_text = Set([re.sub(self.pattern, '', word) for word in all_text.split()])

                    if len(all_text.intersection(self.not_set)) > 0:
                        polarity = -0.11
                        classification = 'negative'
                    elif len(all_text.intersection(self.pos_set)) > 0:
                        polarity = 0.1
                        classification = 'positive'
                    else:
                        polarity = 0.0
                        classification = 'neutral'

                sub = "objective"
                if pattern_result.subjectivity > 0.0:
                    sub = "subjective"

                return self.RETURN_TYPE(
                    classification=classification,
                    polarity=polarity,
                    subjectivity=sub,
                    subjectivity_score=pattern_result.subjectivity,
                    mood=pattern_result.mood,
                    modality=pattern_result.modality,
                    modality_score=pattern_result.modality_score,
                    opinion=pattern_result.opinion
                )
            else:
                return self.RETURN_TYPE(
                    classification="neutral",
                    polarity=0.0,
                    subjectivity="objective",
                    subjectivity_score=0.0,
                    mood="none",
                    modality="none",
                    modality_score=0.0,
                    opinion="no opinion"
                )
        except Exception, e:
            msg = "SentimentAnalyzer (sentiment) : %s" % e
            log.error(msg)
            raise Exception(msg)

    def terminate(self):
        """
        :return: None
        # delete everything from self, so that using this object fails results
        # in an error as quickly as possible
        """
        self._pattern_score.terminate()
        try:
            for val in self.__dict__.keys():
                try:
                    delattr(self, val)
                except:
                    pass
        except Exception, e:
            pass

        collect()
        del garbage[:]

