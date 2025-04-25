# Deep-Research-AI-Agentic-System

This project is an intelligent research assistant system built using LangChain, LangGraph, OpenAI, and Tavily. It leverages an agentic architecture to autonomously search the web, gather context, and generate insightful summaries in response to user queries.
LangChain:

LangChain is a powerful framework for developing applications that utilize large language models (LLMs). It provides abstractions for:

Chaining LLM calls (LLMChain)

Building tool-using agents (initialize_agent)

Prompt engineering (PromptTemplate)

Integrating external tools (e.g., web search)

We are using it becouse it : simplifies the construction of multi-step AI workflows by abstracting logic into "chains" and "agents" that are easy to integrate and extend.

In this project:

Used to define an LLM summarization chain.

Creates a research agent that intelligently invokes tools like Tavily to answer user questions.

LangGraph:
LangGraph is an execution engine built on top of LangChain, designed to define workflows as stateful graphs. Each "node" performs a step in the flow.
LangGraph provides a clean, visualizable way to manage multi-step processes where the output of one function becomes input to the next, making logic modular and composable.

In this project:

A two-node graph is built:

Research Node (searches and collects data)

Drafting Node (writes a final summary)

Ensures sequential flow: question ➝ context ➝ answer.

OpenAI (via LangChain) :

OpenAI provides the GPT family of LLMs like gpt-3.5-turbo and gpt-4.

we use this to generate human-like summaries based on research data, using the powerful reasoning and language generation capabilities of GPT.

In this project:

The GPT model is used for two main purposes:

Generating fallback answers if Tavily fails.

Drafting the final summary based on researched context.

Tavily API

Tavily is an AI-powered web search engine designed for LLMs. It provides accurate, real-time search results in a clean, structured format.

used to  fetch up-to-date, reliable web data for grounding the LLM’s answers in real-world, current information — solving the "LLM hallucination" problem.

In this project:

Used as the primary tool for fetching context.

Integrated as a LangChain-compatible tool for use inside the agent.

File Structure & Responsibilities
agent.py – Tool and Agent Setup
This file defines:

The Tavily tool for real-time search.

The LLM model for generation.

A LangChain agent that combines tools and language models.

A drafting chain that uses custom prompts to generate summaries from research context.

graph_workflow.py – Workflow Orchestration
This file builds the entire logic flow using LangGraph:

Defines a shared GraphState (holds question, context, answer).

Implements two graph nodes:

research_node: Uses Tavily or the agent to gather information.

drafting_node: Summarizes that info using OpenAI.

Compiles and returns a LangGraph-based application.

main.py – Execution Entry Point
The main script that:

Loads environment variables.

Builds the research graph.

Prompts the user for a research query.

Invokes the graph and prints the final summarized output.

Flow Summary
User enters a query.

The system searches the web via Tavily or an agent.

A GPT model summarizes the findings.

The summary is presented back to the user.

This modular, agentic design makes the system highly extensible — other tools, APIs, or steps can be added to the workflow with minimal changes.
