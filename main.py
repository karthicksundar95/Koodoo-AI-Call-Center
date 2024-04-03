### Koosoo AI Call Center control flow
'''
    File name: main.py
    Author: Karthick Sundar C K
    Date created: 27/03/2024
    Date last modified: 03/04/2024
    Python Version: 3.10
'''

# importing packages for handling data and speech recognition from google
from pathlib import Path
from google.cloud import speech_v1p1beta1 as speech
import pandas as pd
import re
import streamlit as st
from dotenv import load_dotenv

# importing classes and methods from this project
from transcribe import CallTranscribe
from disclaimer_check import CallDisclaimerCheck
from sentiment import CallSentiment
from summarization import LLMCallSummary
from insights import LLMCallInsights

load_dotenv()
st.set_page_config(layout="wide")

input_file = st.file_uploader("Upload your audio file here", type=['mp3'])


def markdown_progress(x: float) -> str:
    '''
    Returns a bar from a number between 0 and 100.
    '''
    return (f"""![](https://geps.dev/progress/{x})""")


if input_file is not None:
    if st.button("Generate AI report"):
        # to handle the file upload process to google cloud storage
        st.info("Uploading the file to cloud..")
        audio_uri = speech.RecognitionAudio(
            uri="gs://call-center-bucket/{}".format(input_file.name),
        )
        transcribe = CallTranscribe((Path.cwd()).joinpath(*["data",input_file.name]), input_file.name, audio_uri)
        transcribe.upload_file_to_gcs()
        col1, col2 = st.columns([1, 1])

        with col1:
            # generating text from the audio file
            with st.spinner(text="In progress..."):
                # st.write("inside spin")
                transcribed_text = transcribe.speech_to_text()
            st.markdown("**Extracted Text from audio file:**")
            st.info(transcribed_text)

        with col2:
            # checking if disclaimer was included in the conversation by the agent
            st.markdown("**Disclaimer Check:**")
            disclaimer_check = CallDisclaimerCheck(transcribed_text)
            if disclaimer_check.verify_disclaimer():
                st.success(
                    "Disclaimer protocol: PASSED !!! \n\n(The disclaimer has been read by the customer-care executive in the call)",
                    icon="✅")
            else:
                st.error(
                    "Disclaimer protocol: FAILED !!! \n\n(The customer-care executive failed to read the disclaimer in the call)",
                    icon="🚨")

            # Analysing the sentiment in the audio
            st.write("\n\n\n\n\n\n")
            st.markdown("**Sentiment distribution in this audio file:**")
            call_sentiment = CallSentiment(transcribed_text)
            df = pd.DataFrame({"Sentiment": ["Positive", "Neutral", "Negative"],
                               "Polarity": call_sentiment.get_sentiment()})
            df["bar"] = df["Polarity"].map(markdown_progress)
            st.markdown(df[["Sentiment","bar"]].to_markdown())

            # Generating summary from the audio transcribed text
            st.write("\n\n\n\n\n\n")
            st.markdown("**Call Summary:**")
            summarizer = LLMCallSummary(transcribed_text)
            st.info(re.sub("Summary:","",summarizer.summary))

            # generating insights from the transcribed text
            st.write("\n\n\n")
            st.markdown("**Actionable Insights:**")
            call_insights = LLMCallInsights(transcribed_text)
            st.info(re.sub("Actionable Insights:","",call_insights.insights))
