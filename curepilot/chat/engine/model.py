from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, Pipeline, PreTrainedTokenizer
from typing import Any
import torch


class ModelPipelineLoader:
    def __init__(self, model_id: str) -> None:
        """"""
        self._tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(
            model_id)
        self._model: Any = AutoModelForCausalLM.from_pretrained(
            model_id, load_in_8bit=True)
        self._pipeline: Pipeline | None = None

        self._parameters: dict = {
            'torch_dtype': 'torch.bfloat16',
            'device_map': 'auto',
            'max_new_tokens': 8192,
        }

    def __repr__(self) -> str:
        return f'{self.model}, {self.tokenizer}'

    @property
    def model(self):
        return self._model

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def pipeline(self):
        return self._pipeline

    @property
    def parameters(self):
        return self._parameters

    def get_pipeline(self) -> Pipeline:
        """"""
        if self.pipeline is None:
            self._pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                torch_dtype=self.parameters['torch_dtype'],
                device_map=self.parameters['device_map'],
                max_new_tokens=self.parameters['max_new_tokens'],
                eos_token_id=self._tokenizer.eos_token_id,
            )

        return self.pipeline

    def reset(self):
        try:
            del self._tokenizer
            del self._model
            torch.cuda.empty_cache()
            del self
        except:
            print("Already destroyed.")

    def __del__(self):
        try:
            del self._tokenizer
            del self._model
            torch.cuda.empty_cache()
            del self
        except:
            print("Already destroyed.")
            
    @staticmethod
    def get_prompt(instruction):
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<<SYS>>\n\n"
        system_prompt = """
        You are an expert in The line `CSharp programming. Use the provided context and your knowledge to ass` is not doing anything meaningful in the code. It seems to be a partial sentence or a typo.
        CSharp programming. Use the provided context and your knowledge to assist users with CSharp-related queries.
        Read the context carefully before providing answers and guide users through Python coding steps.
        If you cannot answer a question solely based on the provided context, inform the user accordingly.
        Your responses should contain CSharp code and explanations tailored to the given context.
        """
        
        SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
        prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
        
        return prompt_template