""" Speech recognition and transcription"""

# importing packages to do speech recognition and some display properties via streamlit
from google.cloud import storage, speech_v1p1beta1 as speech
from time import sleep
import streamlit as st
from stqdm import stqdm
from dotenv import load_dotenv
import constants

load_dotenv()


class CallTranscribe:
    """
    Class to transcribe the audio provided as input
    """
    def __init__(self, filepath, filename, audio_uri):
        """
        Constructor to initialized and set all necessary class attributes
        :param filepath: path to the audio file
        :param filename: name of the audio file
        :param audio_uri: google cloud storage location of the audio file uploaded
        """
        self.storage_client = storage.Client.from_service_account_json(constants.GCP_SERVICE_ACCOUNT_CREDENTIALS)
        self.filename = filename
        self.filepath = filepath
        self.config = constants.CONFIG
        self.audio = audio_uri
        self.bucket = self.storage_client.get_bucket(constants.GCP_BUCKET)
        self.text = []

    def upload_file_to_gcs(self):
        """
        To upload the audio file provided as input to gcs
        """
        bucket = self.storage_client.get_bucket(self.bucket)
        blob = bucket.blob(self.filename)
        try:
            blob.upload_from_filename(self.filepath)
            for _ in stqdm(range(30), st_container=st.sidebar):
                sleep(0.5)
        except Exception as e:
            status_code = e.response.status_code
            status_desc = e.response.json()['error']['message']
        else:
            status_code = 200
            status_desc = 'success'
        finally:
            st.write("File upload successful!!!")
            #return status_code, status_desc

        sleep(10)


    def speech_to_text(self) -> speech.RecognizeResponse:
        """
        To transcribe the audio file provided
        :return: Transcribed text with speaker diarization
        """
        client = speech.SpeechClient()
        # Synchronous speech recognition request
        try:
            response = client.recognize(config=self.config, audio=self.audio)
            result = response.results[-1]
        except:
            response = client.long_running_recognize(config=self.config, audio=self.audio)
            result = response.result().results[-1]

        words_info = result.alternatives[0].words

        tag = 1
        speaker = ""
        for index, word_info in enumerate(words_info):

            if word_info.speaker_tag == tag:
                speaker = speaker + " " + word_info.word

            else:
                # print("speaker {}: {}".format(tag,speaker))
                self.text.append("speaker" + " " + str(tag) + ":" + "  " + str(speaker))
                tag = word_info.speaker_tag
                speaker = "" + word_info.word

        # print("speaker {}: {}".format(tag,speaker))
        self.text.append("speaker" + " " + str(tag) + ":" + "  " + str(speaker))

        return "  \n  \n".join(self.text)

