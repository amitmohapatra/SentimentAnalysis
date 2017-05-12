__author__ = 'Amit Mohapatra'

import logging as log
from os import path, sep
from gc import collect, garbage
from collections import namedtuple

from common.resource_manager import ResourceManager
from common.clean_text_processor import CleanTextProcessor
from pattern.en import modality, mood, parse, Sentence, sentiment, parsetree, subjectivity, polarity


class PatternSentimentAnalyzer(object):
    # Return type declaration. return type sent as named tuple object.
    RETURN_TYPE = namedtuple('sentiment', ['polarity', 'subjectivity', 'mood',
                                           'modality', 'modality_score', 'opinion'])

    def __init__(self):
        self.sentence_tokens = None
        self.text = None
        self.base_path = path.dirname(path.dirname(path.dirname(path.dirname(path.dirname(__file__)))))
        opinion_file_path = sep.join([self.base_path, "resources", "opinion"])
        self.names = ResourceManager.read_file(opinion_file_path)

    def sentiment(self, sent_tokens):
        """
        :param sent_tokens: ["sentence of phrase", "sentence of phrase"]. sentences of a phrase as list.
        :return: namedtuple object.
        """

        try:
            if sent_tokens and type(sent_tokens) is list:
                self.sentence_tokens = sent_tokens
                self.text = " ".join(sent_tokens)

                polarity, subjectivity = self.__senti_polarity_subjectivity()
                print polarity
                mood, modality, modality_score = self.__senti_fact()
                opinion = self.__opinion()

                return self.RETURN_TYPE(
                    polarity=polarity,
                    subjectivity=subjectivity,
                    mood=mood,
                    modality=modality,
                    modality_score=modality_score,
                    opinion=opinion
                )
            else:
                raise Exception("sentence token is empty or not list")
        except Exception, e:
            msg = "PatternSentimentAnalyzer : (sentiment) : %s" % e
            log.error(msg)
            raise Exception(e)

    def __senti_polarity_subjectivity(self):
        """
        :return: polarity and subjectivity score of a sentence.
                 polarity : can be negative, positive or 0.0
                 subjectivity : score lies between 0.0 to 1.0
        """

        try:
            avg_polarity = []
            pola = 0.0

            avg_subj = []
            subj = 0.0

            # average polarity calculation of a phrase.
            # finding out polarity of each sentence of phrase and then taking avg.
            for sentence in self.sentence_tokens:
                pola, subj = sentiment(sentence)

                print pola

                if pola != 0.0:
                    avg_polarity.append(pola)
                if subj != 0.0:
                    avg_subj.append(subj)

            # calculate the avg. polarity
            if avg_polarity:
                pola = sum(avg_polarity) / len(avg_polarity)
            # calculate the avg. subjectivity
            if avg_subj:
                subj = sum(avg_subj) / len(avg_subj)

            # calculate the subjectivity of phrase.
            subjec = subjectivity(self.text)
            # calculate the polarity of phrase
            pol = polarity(self.text)
            print pol

            # comparing avg polarity and subjectivity phrase and polarity and subjectivity of phrase
            if pol != 0.0:
                if pol > 0.0:
                    if pol > pola:
                        pola = pol
                elif pol < 0.0:
                    if pol < pola:
                        pola = pol

            if subjec != 0.0:
                if subjec > 0.0:
                    if subjec > subj:
                        subj = subjec

            return pola, float(format(subjec, '.1f'))
        except Exception, e:
            msg = "PatternSentimentAnalyzer : (__senti_polarity_subjectivity()) : %s" % e
            log.error(msg)
            raise Exception(msg)

    def __senti_fact(self):
        """
        :return: mood , modality and modality score
                 mood : indicative, imperative, conditional, subjective
                 modality : fact or not fact
                 score : modality score (0.0 to 0.1)
        """

        try:
            s = parse(self.text, lemmata=True)
            s = Sentence(s)

            __mood = mood(s)
            score = float(format(modality(s), '.1f'))

            __modality = "not fact"
            if score > 0.5:
                __modality = "fact"

            return __mood, __modality, score
        except Exception, e:
            msg = "PatternSentimentAnalyzer : (__senti_fact()) : %s" % e
            log.error(msg)
            raise Exception(msg)

    def __opinion(self):
        """
        :return: opinion of the phrase.
        """

        try:
            result = set()
            s = parsetree(self.text, relations=True, lemmata=True)
            print s
            for sentence in s:
                d = sentence.relations
                # finding the subject of phrase's sentence using part of speech
                if "SBJ" in d:
                    if d["SBJ"]:
                        for i, v in d["SBJ"].iteritems():
                            result.add(v.string)
                # finding the object of phrase's sentence using part of speech
                if "OBJ" in d:
                    if d["OBJ"]:
                        for i, v in d["OBJ"].iteritems():
                            result.add(v.string)
                # finding the foreign words of phrase's sentence using part of speech
                for word in sentence.words:
                    if word.type == "FW":
                        result.add(word.string)
                # finding the preposition words of phrase's sentence using part of speech
                for p in sentence.pnp:
                    result.add(p.string)
                # finding the verb words of phrase's sentence using part of speech
                if "VP" in d:
                    if d["VP"]:
                        for i, v in d["VP"].iteritems():
                            result.add(v.string)

            if not result:
                if len(self.sentence_tokens) == 1:
                    result.add(self.text)
                else:
                    for sentence in s:
                        for word in sentence.words:
                            if word.type == "NN" or word.type == "NNS" \
                                    or word.type == "NNP" or word.type == "NNPS":
                                result.add(word.string)

            output = []
            for r in set(result):
                r = r.strip()
                if r:
                    # cleaning stop word like is , am , are, a, an the ....
                    text = CleanTextProcessor.clean_stop_words(r)
                    text = self.__check_words(text).strip()
                    if text:
                        output.append(text)
            if output:
                return " -- ".join(set(output))
            else:
                return "no opinion"
        except Exception, e:
            msg = "PatternSentimentAnalyzer : (__opinion()) : %s" % e
            log.error(msg)
            raise Exception(msg)

    def __check_words(self, text):

        try:
            # opinion file present in resources folder
            # putting the names that are required while making opinoin.
            # these could be partne name, product name or customer

            result = []
            text = text.strip()

            if text:
                token = text.split()

                for t in token:
                    t = t.strip().lower()

                    t = CleanTextProcessor.clean_dictionary_words(t).strip()
                    if t:
                        if t not in result:
                            result.append(t)

            if result:
                return " ".join(result)
            else:
                return " "
        except Exception, e:
            msg = "PatternSentimentAnalyzer : (__check_words()) : %s" % e
            log.error(msg)
            raise Exception(msg)

    def terminate(self):

        """
        :return: None
        # delete everything from self, so that using this object fails results
        # in an error as quickly as possible
        """

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
