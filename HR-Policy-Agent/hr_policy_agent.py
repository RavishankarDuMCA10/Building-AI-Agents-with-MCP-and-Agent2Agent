from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.prompts import load_mcp_prompt
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

#-----------------------------------------------------------------------------------
# Setup the LLM for the HR Policy Agent
# This uses the OpenAI service with a specific model
# Please replace the environment variables with your own values
#-----------------------------------------------------------------------------------

openai_api_key = os.getenv("OPENAI_API_KEY")
model=ChatOpenAI(
    api_key=openai_api_key,
    model="gpt-4o-mini",
    temperature=0.0,
)

#-----------------------------------------------------------------------------------
# Define the HR policy agent that will use the MCP server
# to answer queries about HR policies.
#-----------------------------------------------------------------------------------

async def run_hr_policy_agent(prompt: str) -> str:
    
    # Make sure the right path to the server file is passed.
    hr_mcp_server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "hr_policy_server.py"))

    print("HR MCP server path:", hr_mcp_server_path)

    # Create the server parameters for the MCP server
    server_params = StdioServerParameters(
        command="python",
        args=[hr_mcp_server_path],
    )

    # Create a client session parameters for the MCP server
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read, write) as session:
            print("initializing session")
            await session.initialize()

            print("\nloading tools & prompt")
            hr_policy_tools = await load_mcp_tools(session)
            hr_policy_prompt = await load_mcp_prompt(session, "get_llm_prompt", arguments={"query": prompt})

            print("\nTools loaded:", hr_policy_tools[0].name)
            print("\nPrompt loaded:", hr_policy_prompt)

            print("\nCreating agent")
            agent=create_react_agent(model,hr_policy_tools)

            print("\nAnswering prompt :", prompt)
            agent_response=await agent.ainvoke({"messages": hr_policy_prompt})

            return agent_response["messages"][-1].content
        
        return "Error"
    

if __name__ == "__main__":
    # Run the HR policy agent with a sample query
    print("\nRunning HR Policy Agent...")
    response = asyncio.run(run_hr_policy_agent("What is the policy on remote work?"))

    print("\nResponse from HR Policy Agent:\n", response)
