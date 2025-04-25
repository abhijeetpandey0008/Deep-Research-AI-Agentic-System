from typing import TypedDict
from agents import get_tavily_tool, get_research_agent, get_drafting_chain
from langgraph.graph import StateGraph, END
import time
import random
from openai import RateLimitError, APIError, Timeout


# STEP 1: Define the state schema that will flow through the graph
class GraphState(TypedDict):
    question: str
    context: str
    answer: str

# STEP 2: Research Node
def research_node(state: GraphState) -> GraphState:
    question = state["question"]
    tavily_tool = get_tavily_tool()
    tavily_result = tavily_tool.invoke(question)
    print(" Researching...")

    if tavily_result and "No answer found" not in tavily_result:
        print(" Tavily search result found.")
        return {
            **state,
            "context": tavily_result,
        }

    agent = get_research_agent()
    result = agent.run(question)
    print(" Research complete.")
    return {
        **state,
        "context": result,
    }

# STEP 3: Drafting Node with exponential backoff
def drafting_node(state: GraphState) -> GraphState:
    print(" Drafting answer...")
    chain = get_drafting_chain()
    retries = 5
    backoff = 1  # seconds

    for attempt in range(retries):
        try:
            result = chain.invoke({
                "research_data": state["context"],
                "question": state["question"]
            })
            print(" Drafting complete.")
            return {
                **state,
                "answer": result.content,
            }

        except RateLimitError as e:
            if attempt == retries - 1:
                print(" Max retries reached due to rate limits. Raising error.")
                raise
            print(f"⏳ Rate limit reached (attempt {attempt + 1}/{retries}). Retrying in {backoff:.1f}s...")
            time.sleep(backoff + random.uniform(0, 1))
            backoff *= 2

        except (APIError, Timeout) as e:
            if attempt == retries - 1:
                print(" Max retries reached due to API error. Raising error.")
                raise
            print(f" Temporary API error: {e}. Retrying in {backoff:.1f}s...")
            time.sleep(backoff + random.uniform(0, 1))
            backoff *= 2

# STEP 4: Build the graph with LangGraph
def build_graph():
    graph = StateGraph(GraphState)

    # Register nodes
    graph.add_node("research", research_node)
    graph.add_node("drafting", drafting_node)

    # Set the flow of nodes
    graph.set_entry_point("research")
    graph.add_edge("research", "drafting")
    graph.add_edge("drafting", END)

    # Compile and return the graph app
    return graph.compile()
