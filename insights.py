""" To generate actionable insights for the audio call"""

# importing the LLM model supporting framework packages
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


class LLMCallInsights:
    """
    Class to generate insights for the audio call
    """
    def __init__(self, call_convo):
        """
        Constructor to define all necessary class attributes
        :param call_convo: transcribed text from the audio file
        """
        self.insights = None
        self.prompt = None
        self.call_convo = call_convo
        print(os.getenv('HUGGING_FACE_TOKEN'))
        self.llm = ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=os.getenv('HUGGING_FACE_TOKEN'))
        self.get_insights()

    def get_prompt(self):
        """
        To generate the prompt message for the LLM to understand
        the task of generating insight from transcribed text
        """
        generic_template = '''
        You are an expert assistant with expertize in understanding call center calls between 
        customer and agent and suggesting actionable insights for the company. The call center is a support service for the postal services.
        Please understand the following call conversation between the customer and the agent and suggest the most 
        optimsed actionable insights:
        {}'''.format(self.call_convo)

        prompt = PromptTemplate(
            input_variables=['call_convo'],
            template=generic_template
        )
        return generic_template, prompt

    def get_insights(self):
        """
        To generate insights by sending the prompt and transcribed text
        """
        generic_template, prompt_template = self.get_prompt()
        model = ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=os.getenv('HUGGING_FACE_TOKEN'))
        llm_chain = LLMChain(llm=model, prompt=prompt_template)
        self.insights = llm_chain.run({'speech': self.call_convo})
