### Retrieval Grader 

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.pydantic_v1 import BaseModel, Field
# Import directly from pydantic
from pydantic import BaseModel, Field

# Data model
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")

def get_structured_llm_grader(llm):
    return llm.with_structured_output(GradeDocuments)

def get_retrieval_grader_chain(llm):
    # LLM with function call 
    # llm = ChatMistralAI(model=mistral_model, temperature=0)
    structured_llm_grader = get_structured_llm_grader(llm)

    # Prompt 
    system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
        If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
        ]
    )

    retrieval_grader_chain = grade_prompt | structured_llm_grader

    return retrieval_grader_chain

# if __name__ == '__main__':
