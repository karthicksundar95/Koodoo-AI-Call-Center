""" Summarize the audio call """

# importing the LLM model supporting framework packages
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

import constants

load_dotenv()


class LLMCallSummary:
    """
    Class to generate text summary for the audio call
    """
    def __init__(self, call_convo):
        """
        Constructor to define necessary class attributes
        :param call_convo: transcribed text
        """
        self.summary = None
        self.prompt = None
        self.call_convo = call_convo
        print(os.getenv('HUGGING_FACE_TOKEN'))
        self.llm = ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=os.getenv('HUGGING_FACE_TOKEN'))
        self.get_summary()

    def get_prompt(self):
        """
        To generate the prompt message for the LLM to understand
        the task of summarizing from transcribed text
        """
        generic_template = '''
        You are an expert assistant with expertize in summarizing call center calls between 
        customer and agent. The call center is a support service for the postal services.
        Please provide a short and concise summary of the following call conversation between the customer and the agent:
        {}'''.format(self.call_convo)

        prompt = PromptTemplate(
            input_variables=['call_convo'],
            template=generic_template
        )
        return generic_template, prompt

    def get_summary(self):
        """
        To generate summary by sending the prompt and transcribed text
        """
        generic_template, prompt_template = self.get_prompt()
        model = ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=os.getenv('HUGGING_FACE_TOKEN'))
        llm_chain = LLMChain(llm=model, prompt=prompt_template)
        self.summary = llm_chain.run({'speech': self.call_convo})
