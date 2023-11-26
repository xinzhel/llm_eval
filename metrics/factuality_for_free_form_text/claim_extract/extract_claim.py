# Clean re-implementation of the claim extraction pipline from https://github.com/GAIR-NLP/factool/blob/main/factool/knowledge_qa/pipeline.py
# This version is more modular and easier to understand
import os
import json
import yaml
from openai_wrapper import OpenAIChat
from typing import List

class ClaimExtractor:
    def __init__(self) -> None:
        with open(os.path.join("claim_extract/claim_extraction.yaml"), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.claim_prompt = data['knowledge_qa']
        self.chat = OpenAIChat(model_name='gpt-4')

    def _claim_extraction(self, responses):
        messages_list = [
            [
                {"role": "system", "content": self.claim_prompt['system']},
                {"role": "user", "content": self.claim_prompt['user'].format(input=response)},
            ]
            for response in responses
        ]
        return self.chat.run(messages_list, List)


claim_extractor = ClaimExtractor()
responses= [
    """Based on the provided sources, there are several projects that are funded by Lendlease. Here is a list of some of these projects:

DWTC One Central: This project is listed under the current projects in the document DWTC One Central - Project Examples.

Woodside Technology Education Design (TED) Building: This project is mentioned in the document 3200-Woodside Technology Education Design (TED) Building and is part of several other projects listed in the document.

Translational Research Institute (TRI): This project is mentioned in the document 3180-Translational Research Institute (TRI) along with various other projects.

Frankston Hospital PPP: This project is mentioned in the document LendLease Frankston Hospital PPP_LLB_CLEANSED.

These are just a few examples of the projects funded by Lendlease. It is important to note that there may be other projects funded by Lendlease that are not mentioned in the provided sources. For a comprehensive list, it would be best to refer to official Lendlease documentation or websites."""
]

claims_in_response =  claim_extractor._claim_extraction(responses=responses)
claims_in_response = [[claim['claim'] for claim in response] for response in claims_in_response]

# save a list of claims in a json file
with open("claims_in_response.json", "w") as file:
    json.dump(claims_in_response, file, indent=4)