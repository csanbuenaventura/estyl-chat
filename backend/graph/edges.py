from langchain.schema import Document
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END
from chains import *
from tools import *
from graph import *

from langchain_openai import ChatOpenAI 
from graph.shared_resources import shared_resources_list

# # from langchain_mistralai import ChatMistralAI
# llm = ChatOpenAI()

# structured_llm_router = get_structured_llm_router(llm)

# hallucination_grader_chain = get_hallucination_grader_chain(llm)
# answer_grader_chain = get_answer_grader_chain(llm)

### Edges

def route_question(state):
    """
    Route question to web search or RAG 

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    # llm = ChatOpenAI()
    # structured_llm_router = get_structured_llm_router(llm)
    # # structured_llm_router = state["structured_llm_router"]

    print("---ROUTE QUESTION---")
    print(state["question"])
    source = shared_resources_list["structured_llm_router"].invoke([SystemMessage(content=ROUTER_INSTRUCTIONS)] + [HumanMessage(content=state["question"])]) 
    if source.datasource == 'generate':
        print("---ROUTE QUESTION TO GENERATE---")
        return "generate"
    elif source.datasource == 'websearch':
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return "websearch"
    elif source.datasource == 'vectorstore':
        print("---ROUTE QUESTION TO RAG---")
        return "vectorstore"

def decide_to_generate(state):
    """
    Determines whether to generate an answer, or add web search

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """

    print("---ASSESS GRADED DOCUMENTS---")
    question = state["question"]
    web_search = state["web_search"]
    filtered_documents = state["documents"]

    if web_search == "Yes":
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        print("---DECISION: NOT ALL DOCUMENTS ARE RELEVANT TO QUESTION, INCLUDE WEB SEARCH---")
        return "websearch"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "generate"
    
def grade_generation_v_documents_and_question(state):
    """
    Determines whether the generation is grounded in the document and answers question

    Args:
        state (dict): The current graph state

    Returns:
        str: Decision for next node to call
    """

    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]
    # llm = ChatOpenAI()

    # hallucination_grader_chain = get_hallucination_grader_chain(llm)
    # answer_grader_chain = get_answer_grader_chain(llm)
    # # hallucination_grader_chain = state["hallucination_grader_chain"]
    # # answer_grader_chain = state["answer_grader_chain"]
    max_retries = state.get("max_retries", 3) # Default to 3 if not provided

    score = shared_resources_list["hallucination_grader_chain"].invoke({"documents": documents, "generation": generation})
    grade = score.binary_score

    # Check hallucination
    if grade == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        # Check question-answering
        print("---GRADE GENERATION vs QUESTION---")
        # Test using question and generation from above 
        score = shared_resources_list["answer_grader_chain"].invoke({"question": question,"generation": generation})
        grade = score.binary_score
        if grade == "yes":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        elif state["loop_step"] <= max_retries:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
        else:
            print("---DECISION: MAX RETRIES REACHED---")
            return "max retries"  
    elif state["loop_step"] <= max_retries:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"
    else:
        print("---DECISION: MAX RETRIES REACHED---")
        return "max retries"  
    
def decide_to_generate_outfits(state):
    """
    Determines whether to generate an outfit

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """

    print("---ASSESS GRADED DOCUMENTS---")
    generate_outfit = state["generate_outfit"]

    if web_search == "Yes":
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        print("---DECISION: NOT ALL DOCUMENTS ARE RELEVANT TO QUESTION, INCLUDE WEB SEARCH---")
        return "websearch"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "generate"