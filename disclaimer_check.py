""" Verification of disclaimer inclusion """

# importing necessary packages
import re

class CallDisclaimerCheck:
    """
    Class to verify the disclaimer protocol
    """
    def __init__(self, transcribed_text):
        """
        Constructor to define all necessary class attributes
        :param transcribed_text: text extracted from the input audio
        """
        self.transcribed_text = transcribed_text

    def verify_disclaimer(self):
        """
        Method to search for the disclaimer script in the audio text
        :return: Boolean True or False based on presence or absence of the script
        """
        if len(re.findall("call is being recorded .* this contact from us", self.transcribed_text))>0:
            return True
        else:
            return False