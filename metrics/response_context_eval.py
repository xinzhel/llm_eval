import os

from rouge import Rouge

import semantic_kernel as sk

import semantic_kernel.connectors.ai.open_ai as sk_oai

from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

rouge = Rouge()

kernel = sk.Kernel()

 

deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()

kernel.add_chat_service(

    "eval", AzureChatCompletion(deployment, endpoint, api_key, api_version="2023-06-01-preview")

)

 

# Luke: perhaps transform this into a library + function parameters.

# check llm harness

skills_directory = os.getcwd() + "/skills"

fact_skills = kernel.import_semantic_skill_from_directory(skills_directory, "Evaluation")

fact_function = fact_skills["factuality"]

relevance_function = fact_skills['relevance']

helpfulness_function = fact_skills['helpfulness']

 

def groundedness(response: str, documents: list[str]):

    hyps, refs = [response] * len(documents), documents

    scores = rouge.get_scores(hyps, refs)

    max_rouge2 = max([d['rouge-2']['f'] for d in scores])

    return max_rouge2


def helpfulness(response: str, documents: list[str]):

    help_context = kernel.create_new_context()

    help_context['retrieved_documents'] = '\n'.join(documents)

    help_context['response'] = response

    helpfulness_eval = helpfulness_function(context = help_context)

    return helpfulness_eval


class RetrievalMetrics:
    def __init__(self, question, response, context) -> None:
        self.question = question
        self.response = response
        self.context = context
    
    def context_precision(self):
        """ Signal-to-noise ratioin in the retrieved contexts. 
        |Relevant_Setences| / |Sentences| <- arg P(Relevant_Setences in Context | Question)"""
        pass

    def context_recall(self):
        """" Whether Retrieval retrieve all the necessary information needed to answer the question. 
        
        Step 1: Find Statements from Ground_truth response
        Step 2: Find how many Statements (from Ground_truth response) are in Context 
        Step 3: Statements in Context / Statements in Ground_truth"""
        pass

class GenerationMetrics:
    def __init__(self, question, response, context) -> None:
        self.question = question
        self.response = response
        self.context = context

    def factuality(self, response: str, documents: list[str]):
        """  |Correct Statements Supported by the Context| / |Statements| <- arg P(Statements|Q, A)"""

        fact_context = kernel.create_new_context()

        fact_context['retrieved_documents'] = '\n'.join(documents)

        fact_context['response'] = response

        fact_eval = fact_function(context = fact_context)

        return fact_eval

    

    def resonpse_relevancy(self, response: str, documents: list[str]):
        """ Response/Answer relevancy to the question. Sim(Questions', Actual Question) <- arg max P(Questions' | Answer)"""

        rel_context = kernel.create_new_context()

        rel_context['retrieved_documents'] = '\n'.join(documents)

        rel_context['response'] = response

        relevance_eval = relevance_function(context = rel_context)

        return relevance_eval

 



   



# Factuality
"""
You are evaluating a response for a specific question based on a list of retrieved documents, using a specific set of standards. Below are the retrieved documents.

 

{{$retrieved_documents}}

 

Below is the response:
{{$response}}

 

Below is the criteria.
Determine if the information in the response can be found in one or more search documents.

 

Does the response meet the criterion? First, write out in a step-by-step manner your reasoning about the criterion to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset. Then print only the single character "Y" or "N" (without quotes or punctuation) on its own line corresponding to the correct answer. In the end, repeat just the letter again by itself on a new line.
Reasoning:
"""


# Helpfulness
"""
You are evaluating a response for a specific question based on a list of retrieved documents, using a specific set of standards. Below are the retrieved documents.

 

{{$retrieved_documents}}

 

Below is the response:
{{$response}}

 

Below is the criteria.
Does the response directly solve the question?

 

Does the response meet the criterion? First, write out in a step-by-step manner your reasoning about the criterion to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset. Then print only the single character "Y" or "N" (without quotes or punctuation) on its own line corresponding to the correct answer. In the end, repeat just the letter again by itself on a new line.
Reasoning:
"""

# Relevance
"""
You are evaluating a response for a specific question based on a list of retrieved documents, using a specific set of standards. Below are the retrieved documents.

 

{{$retrieved_documents}}

 

Below is the response:
{{$response}}

 

Below is the criteria.
Is the response relevant to the topic at hand? It’s essential to recognize that the response does not need to be highly specific to the preceding question. As long as it remains focused on the topic at hand, it is considered relevant.

 

Does the response meet the criterion? First, write out in a step-by-step manner your reasoning about the criterion to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset. Then print only the single character "Y" or "N" (without quotes or punctuation) on its own line corresponding to the correct answer. In the end, repeat just the letter again by itself on a new line.
Reasoning:
"""