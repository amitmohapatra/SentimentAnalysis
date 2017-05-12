__author__ = 'Amit Mohapatra'

import string
import logging as log
from string import punctuation

import enchant
from nltk.corpus import stopwords

from pattern.en import tokenize
from stack_trace import StackTrace

from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()

stop_words = stopwords.words('english')  # global declaration
dic_en = enchant.Dict("en_US")


class CleanTextProcessor(object):
    @staticmethod
    def clean_text(text):
        """
        :param text: text as str
        :return: list of sentences
        """

        try:
            text = text.strip()
            if text:
                final_sentences = []
                token_text = tokenize(text)

                for sentence in token_text:
                    words = sentence.split()
                    cleaned_tokens = [porter_stemmer.stem(word) for word in words if word not in punctuation]
                    cleaned_sent = " ".join(cleaned_tokens)
                    cleaned_sent = CleanTextProcessor.clean_not_words(cleaned_sent)
                    cleaned_sentence = cleaned_sent + "."
                    final_sentences.append(cleaned_sentence)
                return final_sentences
            else:
                return []
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "CleanTextProcessor (clean_text()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def clean_not_words(text):

        try:
            text = text.strip()
            if text:
                text = text.replace("n't", "not")
                return text
            else:
                return " "
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "CleanTextProcessor (clean_not_words()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def clean_stop_words(text):

        try:
            text = text.strip()
            if text:
                tokens = [word for word in text.split() if word not in stop_words]
                return " ".join(tokens)
            else:
                return " "
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "CleanTextProcessor (clean_stop_words()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def clean_dictionary_words(text):

        try:
            result = []
            text = text.strip()
            if text:
                for t in text.split():
                    t = t.strip()

                    if not dic_en.check(t):
                        result.append(t)
                return " ".join(result)
            else:
                return " "
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "CleanTextProcessor (clean_dictionary_words()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def clean_escape_codes(text):

        try:
            text = text.strip()
            if text:
                return str(text).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\a", " ").replace(
                    "\b", " ").strip()
            else:
                return " "
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "CleanTextProcessor (clean_escape_codes()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def clean_codecs(text):

        try:
            text = text.strip()
            if text:

                if not isinstance(text, (int, long)):
                    text = filter(lambda x: x in string.printable, text)
                return text
            else:
                return " "
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "CleanTextProcessor (clean_codecs()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def clean_product_names(text, product_names):
        """
        :param text:  text as str
        :return: modified text as str
        This method will replace product names provided in product_name_replace.csv in resource.
        Ex : xen server => xenserver
        basically space will be removed from product names.
        """

        try:
            text = text.strip()
            if text:
                for key, val in product_names.iteritems():

                    if key in text:
                        text = text.replace(key, val)
                return text
            else:
                return " "
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "CleanTextProcessor (clean_product_names()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)
