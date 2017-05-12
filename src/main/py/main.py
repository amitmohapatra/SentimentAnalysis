__author__ = 'Amit Mohapatra'

from algo.sentiment_analyzer import SentimentAnalyzer

if __name__ == "__main__":
    """
    The main program starts here.
    """

    #print SentimentAnalyzer().sentiment("We remain grateful to our scientists & the then political leadership for the courage shown in Pokhran in 1998.")

    from nltk.stem.porter import PorterStemmer
    porter_stemmer = PorterStemmer()

    from nltk.stem.lancaster import LancasterStemmer
    lancaster_stemmer = LancasterStemmer()

    from nltk.stem import SnowballStemmer
    snowball_stemmer = SnowballStemmer('english')

    from nltk.stem import WordNetLemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()

    print wordnet_lemmatizer.lemmatize("is", pos='v')
