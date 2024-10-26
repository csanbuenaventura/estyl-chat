from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Any, Callable, Dict, List, Union
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# # make sure you have .env file saved locally with your API keys
# from dotenv import load_dotenv

# load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import SKLearnVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import sys

import os, getpass
import pprint

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

# _set_env("TAVILY_API_KEY")
os.environ['TOKENIZERS_PARALLELISM'] = 'true'

# _set_env("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = "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"
os.environ["LANGCHAIN_PROJECT"] = "estyl"
os.environ['TAVILY_API_KEY'] = "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"
os.environ["OPENAI_API_KEY"] = "sk-svcacct-vZG2VCHIjZUn7fl3EmK51F77F3aPcLnrVf7Bd0-Z0DUzt9Zv9mfomR09b_7gvT3BlbkFJPnOvUAPfOk75znoM8NPQDGS8KAEhSuj82s5I5jmjpvLo7-13URd9cnDBHk_wgA"

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from chains import *
from tools import *
from graph import *
from graph.shared_resources import shared_resources_list

# data = {}

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Init
#     print("Startup")
#     # Initialize the resources once
#     llm = ChatOpenAI()
#     loader = PyPDFLoader('pdfs/ESTYL _ STYLE GUIDE (pdf).pdf')
#     docs = loader.load()

#     print("shared :", shared_resources_list)

#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     splits = text_splitter.split_documents(docs)
#     vectorstore = InMemoryVectorStore.from_documents(documents=splits, embedding=OpenAIEmbeddings())
#     retriever = vectorstore.as_retriever()

#     web_search_tool = get_web_search_tool()
#     router_chain = get_router_chain(llm)
#     retrieval_grader_chain = get_retrieval_grader_chain(llm)
#     rag_chain = get_generate_chain(llm)

#     # Store resources globally in `shared_resources`
#     data["retriever"] = vectorstore.as_retriever()
#     data["llm"] = llm
#     data["web_search_tool"] = get_web_search_tool()
#     data["router_chain"] = get_router_chain(llm)
#     data["retrieval_grader_chain"] = get_retrieval_grader_chain(llm)
#     data["rag_chain"] = get_generate_chain(llm)

#     data["chat_graph"] = create_graph()

#     yield

#     # Shutdown
#     print("Shutdown")
#     data.clear()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    global retriever, llm, web_search_tool, router_chain, retrieval_grader_chain, rag_chain
    
    # Initialize the resources once
    llm = ChatOpenAI()
    loader = PyPDFLoader('pdfs/ESTYL _ STYLE GUIDE (pdf).pdf')
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = InMemoryVectorStore.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()

    web_search_tool = get_web_search_tool()
    router_chain = get_router_chain(llm)
    retrieval_grader_chain = get_retrieval_grader_chain(llm)
    rag_chain = get_generate_chain(llm)

    # Store resources globally in `shared_resources`
    shared_resources_list["retriever"] = vectorstore.as_retriever()
    shared_resources_list["llm"] = llm
    shared_resources_list["web_search_tool"] = get_web_search_tool()
    shared_resources_list["router_chain"] = get_router_chain(llm)
    shared_resources_list["retrieval_grader_chain"] = get_retrieval_grader_chain(llm)
    shared_resources_list["rag_chain"] = get_generate_chain(llm)

    shared_resources_list["structured_llm_router"] = get_structured_llm_router(llm)

    shared_resources_list["hallucination_grader_chain"] = get_hallucination_grader_chain(llm)
    shared_resources_list["answer_grader_chain"] = get_answer_grader_chain(llm)

    # init graph
    chat_graph = create_graph()
    shared_resources_list["chat_graph"] = chat_graph

    return

print("Global resources initialized")
origins = ["*"]    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    expose_headers=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatBody(BaseModel):
    text: str

@app.post("/ai")
async def ai(body: ChatBody):
    if not body.text:
        raise HTTPException(status_code=400, detail="No chat provided.")

    text = body.text
    
    # print(text)

    inputs = {
        "question": text,
        "documents": [],
    }
    # print("shared again :", shared_resources_list)
    # Inject the initialized objects into the workflow's state
    # inputs = {
    #     "question": text,
    #     "llm": app.state.llm,
    #     "retriever": app.state.retriever,
    #     "web_search_tool": app.state.web_search_tool,
    #     "router_chain": app.state.router_chain,
    #     "retrieval_grader_chain": app.state.retrieval_grader_chain,
    #     "rag_chain": app.state.rag_chain,
    #     "documents": []  # initialize an empty list of documents
    # }
    config = {"configurable": {"thread_id": "1"}}
    # chat_graph = data["chat_graph"]
    for output in shared_resources_list["chat_graph"].stream(inputs, config):
        # print("output: ", output)
        for key, value in output.items():
            print(f"Finished running: {key}:")
    response = value["generation"]

    # # The dictionary `results` is returned, and FastAPI will automatically convert it into a JSON response.
    return {"text": response}
