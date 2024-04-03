""" Sentiment analysis on customer-agent interaction in the audio"""

# importing sentiment package
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class CallSentiment:
    """
    Class to perform sentiment analysis on the conversation between customer and agent
    """
    def __init__(self, transcribed_text):
        """
        Constructor to define all the necessary class attributes
        :param transcribed_text: transcribed text from the input audio
        """
        self.transcribed_text = transcribed_text
        self.result = None

    def get_sentiment(self):
        """
        Rule-based approach for sentiment analysis, that gives a collective score
        for positive, negative and neutral aspects in the conversation
        """
        sia = SentimentIntensityAnalyzer()
        self.result = sia.polarity_scores(self.transcribed_text)
        return [round(self.result['pos']*100), round(self.result['neu']*100), round(self.result['neg']*100)]
