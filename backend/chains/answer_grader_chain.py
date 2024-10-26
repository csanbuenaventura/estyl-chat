from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel, Field

### Answer Grader 

# Data model
class GradeAnswer(BaseModel):
    """Binary score to assess answer addresses question."""

    binary_score: str = Field(description="Answer addresses the question, 'yes' or 'no'")
    explanation: str = Field(description="Explain the reasoning for the score")

def get_structured_llm_grader(llm):
    return llm.with_structured_output(schema=GradeAnswer)

def get_answer_grader_chain(llm):
    structured_llm_grader = get_structured_llm_grader(llm)

    # Prompt 
    system = """You are a grader assessing whether an answer addresses / resolves a question \n 
        Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
        ]
    )

    answer_grader_chain = answer_prompt | structured_llm_grader

    return answer_grader_chain