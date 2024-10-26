### Router

from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# Data model
class RouteQuery(BaseModel):
    """ Route a user query to the most relevant datasource. """

    datasource: Literal["generate", "vectorstore", "websearch"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore or generate.",
    )

# Instructions for the router 
ROUTER_INSTRUCTIONS = """
You are an expert in routing a user question to the appropriate datasource or directly to the LLM for general conversation.
- Use "generate" if the question is conversational in nature or if the question is not clear enough to be directed to vectorstore or websearch (e.g. one word queries, etc.).
- Use "vectorstore" if the question is specific to fashion styles, outfit suggestions, or context available in documents.
- Use "websearch" if the question is related to fashion but goes beyond the available fashion-related documents or requires external information.

Always aim to provide the most precise route based on the user's question. 
"""

def get_structured_llm_router(llm):

    structured_llm_router = llm.with_structured_output(RouteQuery) 
    
    return structured_llm_router

def get_router_chain(llm):
    # LLM with structured output
    structured_llm_router = get_structured_llm_router(llm)

    # Define the prompt template
    router_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", ROUTER_INSTRUCTIONS),
            ("human", "User question: {question}"),
        ]
    )

    # Chain the prompt and the structured LLM output
    router_chain = router_prompt | structured_llm_router

    return router_chain