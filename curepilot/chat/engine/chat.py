from .model import ModelPipelineLoader
from langchain import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain


model_id = '/mnt/sda/Aamir/FineTunned/Mistral'
pipe = ModelPipelineLoader(model_id)
llm = HuggingFacePipeline(pipeline=pipe.get_pipeline(), model_kwargs={'temperature': 0})
instruction = "{text}"
template = ModelPipelineLoader.get_prompt(instruction)
prompt = PromptTemplate(template=template, input_variables=["text"])
model = LLMChain(prompt=prompt, llm=llm, verbose=True)

def completion(message):
    return model({'text': message['prompt']})['text']