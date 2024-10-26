# from langchain_core.prompts import ChatPromptTemplate
# # from langchain_core.pydantic_v1 import BaseModel, Field
# # Import directly from pydantic
# from pydantic import BaseModel, Field

# ### Hallucination Grader 

# # Data model
# from pydantic import BaseModel, Field

# # Data model
# class GeneratedOutfit(BaseModel):
#     """Structured data model for a generated outfit recommendation."""

#     top: str = Field(description="The recommended top clothing item for the outfit, e.g., shirt, blouse.")
#     bottom: str = Field(description="The recommended bottom clothing item for the outfit, e.g., trousers, skirt.")
#     shoes: str = Field(description="The recommended shoes for the outfit.")
#     accessories: str = Field(
#         default="",
#         description="Optional accessories to complement the outfit, e.g., scarf, necklace."
#     )
#     occasion: str = Field(
#         default="casual",
#         description="The occasion or setting this outfit is best suited for, e.g., 'formal', 'casual', 'business'."
#     )
#     style_notes: str = Field(
#         default="",
#         description="Additional style notes or suggestions, such as color or material preferences."
#     )
#     complete: bool = Field(
#         default=True,
#         description="Indicates whether the outfit recommendation is complete or if more details are needed."
#     )

#     def summary(self) -> str:
#         """Return a summary of the outfit suggestion."""
#         outfit_description = (
#             f"Top: {self.top}, Bottom: {self.bottom}, Shoes: {self.shoes}."
#         )
#         if self.accessories:
#             outfit_description += f" Accessories: {self.accessories}."
#         return outfit_description
    
# def get_structured_llm_grader(llm):
#     return llm.with_structured_output(schema=GradeHallucinations)

# def get_hallucination_grader_chain(llm):
#     structured_llm_grader = get_structured_llm_grader(llm)

#     # Prompt 
#     system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
#         Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""
#     hallucination_prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", system),
#             ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
#         ]
#     )

#     hallucination_grader_chain = hallucination_prompt | structured_llm_grader
    
#     # hallucination_grader.invoke({"documents": docs, "generation": generation})

#     return hallucination_grader_chain