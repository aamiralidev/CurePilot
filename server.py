# Adapted from
# https://github.com/vllm-project/vllm/blob/main/vllm/entrypoints/openai/api_server.py

import fastapi
from fastapi import Request
import uvicorn
from langchain import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain
import time 
from http import HTTPStatus
from fastapi.responses import JSONResponse, StreamingResponse

import openai_api_protocol
from model import ModelPipelineLoader



logger = None
app = fastapi.FastAPI()

model = {
    "names": ['Mistral']
}

def create_error_response(status_code: HTTPStatus, message: str) -> JSONResponse:
    return JSONResponse(openai_api_protocol.ErrorResponse(message=message,
                        type="invalid_request_error").dict(),
                        status_code=status_code.value)

def create_response(text):
    response = {
        "id": "cmpl-XYZ123",
        "object": "chat_completion",
        "created": 1618910769,
        "model": "gpt-4",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": text
                }
            }
        ]
    }
    return response


@app.get("/v1/models")
async def show_available_models():
    """Show available models. Right now we only have one model."""
    return openai_api_protocol.ModelList(data=[
        openai_api_protocol.ModelCard(id=name, root=name, permission=[openai_api_protocol.ModelPermission()])
    for name in model['names']])
    
@app.post("/v1/models")
async def show_available_models():
    """Show available models. Right now we only have one model."""
    return openai_api_protocol.ModelList(data=[
        openai_api_protocol.ModelCard(id=name, root=name, permission=[openai_api_protocol.ModelPermission()])
    for name in model['names']])

async def chat_completion(raw_request: Request):
    pass 

@app.post("/v1/chat/completions")
async def create_chat_completion(raw_request: Request):
    request = openai_api_protocol.ChatCompletionRequest(**await raw_request.json())
    if request.logit_bias is not None and len(request.logit_bias) > 0:
        return create_error_response(HTTPStatus.BAD_REQUEST, "logit_bias is not currently supported")

    response = model["pipeline"]({"text": request.messages[-1]['content']})['text']
    return create_response(response)


if __name__ == "__main__":
    # model_id = '/mnt/sda/Aamir/FineTunned/Mistral'
    # pipe = ModelPipelineLoader(model_id)
    # llm = HuggingFacePipeline(pipeline=pipe.get_pipeline(), model_kwargs={'temperature': 0})
    # instruction = "{text}"
    # template = ModelPipelineLoader.get_prompt(instruction)
    # prompt = PromptTemplate(template=template, input_variables=["text"])
    # model['pipeline'] = LLMChain(prompt=prompt, llm=llm, verbose=True)
    model['pipeline'] = lambda text: text

    # Run
    uvicorn.run(app,
                host="0.0.0.0",
                port=18888,
                log_level="info",
                access_log=True)
