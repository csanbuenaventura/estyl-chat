from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.pydantic_v1 import BaseModel, Field
# Import directly from pydantic
from pydantic import BaseModel, Field

### Hallucination Grader 

# Data model
class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(description="Answer is grounded in the facts, 'yes' or 'no'")
    explanation: str = Field(description="Explain the reasoning for the score")
    
def get_structured_llm_grader(llm):
    return llm.with_structured_output(schema=GradeHallucinations)

def get_hallucination_grader_chain(llm):
    structured_llm_grader = get_structured_llm_grader(llm)

    # Prompt 
    system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
        Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""
    hallucination_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
        ]
    )

    hallucination_grader_chain = hallucination_prompt | structured_llm_grader
    
    # hallucination_grader.invoke({"documents": docs, "generation": generation})

    return hallucination_grader_chain