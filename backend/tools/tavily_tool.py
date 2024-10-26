from langchain_community.tools.tavily_search import TavilySearchResults

def get_web_search_tool(k=3):
    return TavilySearchResults(k=k)