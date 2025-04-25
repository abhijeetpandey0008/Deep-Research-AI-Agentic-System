from langchain import hub

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from tavily import TavilyClient
import os
from dotenv import load_dotenv

from langchain_community.tools.tavily_search.tool import TavilySearchResults

def get_tavily_tool():
    return TavilySearchResults()




# Load API keys from .env
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

# Tavily search tool
def tavily_search(query: str) -> str:
    client = TavilyClient(api_key=tavily_key)
    results = client.search(query=query, search_depth="advanced", include_answer=True)
    return results.get("answer", str(results))

# Wrap Tavily as a LangChain Tool
tavily_tool = Tool.from_function(
    name="TavilySearch",
    func=tavily_search,
    description="Searches web using Tavily for relevant, up-to-date info."
)

def get_llm():
    return ChatOpenAI(
        temperature=0.3,
        model="gpt-3.5-turbo",
        openai_api_key=openai_key
    )

# 1. Research Agent
def get_research_agent():
    llm = get_llm()
    return initialize_agent(
        tools=[tavily_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

# 2. Answer Drafting Chain
def get_drafting_chain():
    from langchain_core.runnables import RunnableLambda
    prompt_template = PromptTemplate(
        input_variables=["research_data"],
        template="""
        Based on the following research data:
        {research_data}
        
        Write a well-structured, insightful summary or report.
        """
    )
    return prompt_template |get_llm()

    