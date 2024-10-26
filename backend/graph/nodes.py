from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import SKLearnVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.schema import Document
from langgraph.graph import END

from fastapi import Request

from chains import *
from tools import *
from graph import *
from graph.shared_resources import shared_resources_list
# from ai import app

from langchain_openai import ChatOpenAI 
from langchain_mistralai import ChatMistralAI
# llm = ChatOpenAI()

# loader = PyPDFLoader('pdfs/ESTYL _ STYLE GUIDE (pdf).pdf')

# docs = loader.load()

# # print(len(docs))

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(docs)
# vectorstore = InMemoryVectorStore.from_documents(
#     documents=splits, embedding=OpenAIEmbeddings()
# )

# retriever = vectorstore.as_retriever()

# router_chain = get_router_chain(llm)
# retrieval_grader_chain = get_retrieval_grader_chain(llm)
# rag_chain = get_generate_chain(llm)
# web_search_tool = get_web_search_tool()

### Nodes
def retrieve(state):
    """
    Retrieve documents from vectorstore

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]

    # Write retrieved documents to documents key in state
    documents = shared_resources_list["retriever"].invoke(question)
    # print("documents 2: ", documents)
    return {"documents": documents}

def generate(state):
    """
    Generate answer using RAG on retrieved documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    loop_step = state.get("loop_step", 0)
    messages = state["messages"]
    
    # RAG generation
    generation = shared_resources_list["rag_chain"].invoke({"context": documents, "question": question, "messages": messages})
    # Create a conversation entry
    # entry = {
    #     "human": question,
    #     "ai": generation
    # }
    # Append the entry to the conversation history
    # conversation_history.append(entry)
    messages = [
        HumanMessage(content=question),
        SystemMessage(content=generation),
    ]
    return {
        "generation": generation, 
        "loop_step": loop_step+1,
        "messages": messages,
    }

def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]
    # llm = ChatOpenAI()
    # retrieval_grader_chain = get_retrieval_grader_chain(llm)
    # # retrieval_grader_chain = state["retrieval_grader_chain"]
    
    # Score each doc
    filtered_docs = []
    web_search = "No"
    for d in documents:
        score = shared_resources_list["retrieval_grader_chain"].invoke({"question": question, "document": d.page_content})
        grade = score.binary_score
        # Document relevant
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        # Document not relevant
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            # We do not include the document in filtered_docs
            # We set a flag to indicate that we want to run web search
            web_search = "Yes"
            continue
    return {"documents": filtered_docs, "web_search": web_search}

def web_search(state):
    """
    Web search based based on the question

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended web results to documents
    """

    print("---WEB SEARCH---")
    # print("state : ", state)
    question = state["question"]
    documents = state["documents"]
    # llm = ChatOpenAI()
    # web_search_tool = get_web_search_tool()
    # # web_search_tool = state["web_search_tool"]

    # Web search
    docs = shared_resources_list["web_search_tool"].invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents}

# def generate_outfits(state):
#     """
#     Generate answer using RAG on retrieved documents

#     Args:
#         state (dict): The current graph state

#     Returns:
#         state (dict): New key added to state, generation, that contains LLM generation
#     """
#     print("---GENERATE---")
#     question = state["question"]
#     documents = state["documents"]
#     loop_step = state.get("loop_step", 0)
    
#     # RAG generation
#     generation = rag_chain.invoke({"context": documents, "question": question})
#     return {"generation": generation, "loop_step": loop_step+1}