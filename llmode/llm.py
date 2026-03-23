import logging
from typing import List
from concurrent.futures import ThreadPoolExecutor

import torch
from openai import OpenAI

SYSTEM_TEMPLATE='''You are a scientist whose task is to perform Symbolic Regression. \
You should search the function space to find the best simple function that fits the data. \
You are given {N_CONTEXT} examples of proposed equations sorted from worst to best. \
Your goal is to suggest {N_NEW} improved equations of varying complexity. Replace all numerical constants with "C" -- \
they will be optimized with an external optimizer. \
Write one equation per line from simplest to most complex with no extra explanation. \
Available operators: +, -, *, **, /, sin, log, exp, abs. \
Independent variables: {INDEPENDENT_VARIABLES}.
'''


def generate_prompt(examples_str: List[str], n_new: int, n_variables: int):
    independent_variables = ', '.join([f"x_{i}" for i in range(n_variables)])
    context = "\n".join(examples_str)
    messages = [
        {"role": "system", "content": SYSTEM_TEMPLATE.format(
            N_CONTEXT=len(examples_str),
            N_NEW=n_new,
            INDEPENDENT_VARIABLES=independent_variables)},
        {"role": "user", "content": context},
    ]
    return messages

class Llm:
    def __init__(self, openai_api_key, openai_api_base):
        self.n_queries = 1
        self.request_kwargs = {
            'max_output_tokens': 1024,
        }

        self.client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
        self.model_name = self.get_model_name()

    def get_model_name(self):
        models = self.client.models.list()
        return models.data[0].id

    def make_request(self, prompt):
        response = self.client.responses.create(
            model=self.model_name,
            input=prompt,
            **self.request_kwargs
        )
        return response.output_text

    def query(self, prompts: List[dict[str, str]]):
        for prompt_id in range(len(prompts)):
            logging.info(f"## Query {self.n_queries + prompt_id} BEGIN ##")
            logging.info(prompts[prompt_id])
            logging.info(f"## Query {self.n_queries + prompt_id} END ##")

        with ThreadPoolExecutor(max_workers=20) as executor:
            responses = list(executor.map(self.make_request, prompts))

        for prompt_id, response in enumerate(responses):
            logging.info(f"## Response {self.n_queries + prompt_id} BEGIN ##")
            logging.info(response)
            logging.info(f"## Response {self.n_queries + prompt_id} END ##")
        self.n_queries += len(prompts)
        return responses
