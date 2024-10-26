from langgraph.graph import StateGraph
from IPython.display import Image, display
from langchain.schema import Document
from langgraph.graph import END
from langgraph.checkpoint.memory import MemorySaver
from .state import GraphState
from .nodes import *
from .edges import *

def create_graph():
    workflow = StateGraph(GraphState) 

    # Define the nodes
    workflow.add_node("websearch", web_search) # web search
    workflow.add_node("retrieve", retrieve) # retrieve
    workflow.add_node("grade_documents", grade_documents) # grade documents
    workflow.add_node("generate", generate) # generatae

    # Build graph
    workflow.set_conditional_entry_point(
        route_question,
        {
            "websearch": "websearch",
            "vectorstore": "retrieve",
            "generate": "generate",
        },
    )
    workflow.add_edge("websearch", "generate")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "websearch": "websearch",
            "generate": "generate",
        },
    )
    workflow.add_conditional_edges(
        "generate",
        grade_generation_v_documents_and_question,
        {
            "not supported": "generate",
            "useful": END,
            "not useful": "websearch",
            "max retries": END,
        },
    )

    memory = MemorySaver()

    # Compile
    graph = workflow.compile(checkpointer=memory)

    return graph

