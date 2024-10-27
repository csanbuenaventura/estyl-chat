import operator
from typing_extensions import TypedDict
from typing import List, Annotated, Any, Dict
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    """
    Graph state is a dictionary that contains information we want to propagate to, and modify in, each graph node.
    """
    messages: Annotated[list, add_messages]
    question : str # User question
    generation : str # LLM generation
    web_search : str # Binary decision to run web search
    max_retries : int # Max number of retries for answer generation 
    answers : int # Number of answers generated
    documents : List[str] # List of retrieved documents
    loop_step: Annotated[int, operator.add] # loop step
    generate_outfit: str # do i generate an outfit
    # conversation_history: List[Dict[str, Any]]
    # generate_outfit : bool 
    # generated_outfit : dict
    # outfit_request : str
