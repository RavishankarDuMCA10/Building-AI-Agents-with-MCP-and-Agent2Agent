from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.resources import load_mcp_resources
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

#-----------------------------------------------------------------------------------
# Configure the MCP Server Connection
#-----------------------------------------------------------------------------------

#Make sure the right path to the MCP server file is passed.
server_params = StdioServerParameters(
    command="python",
    args=[os.getcwd() + "/Code-of-Conduct Assistant/code_of_conduct_server.py"],
)

#-----------------------------------------------------------------------------------
# Setup the OpenAI model
#-----------------------------------------------------------------------------------
openai_api_key = os.getenv("OPENAI_API_KEY")

model=ChatOpenAI(
    api_key=openai_api_key,
    model="gpt-4o-mini",
    temperature=0.0,
)

#-----------------------------------------------------------------------------------
# Asynchronous function to fetch content from MCP resource
# Boilerplate code to run MCP and fetch resources
#-----------------------------------------------------------------------------------
async def fetch_resource_content():
    print("Running the MCP server...")
    async with stdio_client(server_params) as (read, write):
        # Initialize a session with the MCP server
        async with ClientSession(read, write) as session:
            print("initilizing session")
            await session.initialize()

            # Load list of resources avalaible & print
            print("\nloading resources")
            resources=await load_mcp_resources(session)
            print("Resources loaded :")
            for resource in resources:
                print(resource.metadata)

            #Return the body of the first resouce
            #This contains the content of the code of conduct PDF
            return resources[0].data
    
    return "done"

#-----------------------------------------------------------------------------------
# Run the MCP Client, fetch resouce and generate response
#-----------------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n--------------------------------")
    print("Running the code-of-client application")
    # Get content from the MCP resource
    retrieved_content = asyncio.run(fetch_resource_content())
    print("\nContent retrieved:", retrieved_content)

    # Simulated User query
    user_query = "What are the data privacy policies of the company?"
    print("\nUser query:", user_query)

    # Use the retirieved content to answer the user query
    prompt = f"""Answer the query based on the following context provided. \n
            Context: {retrieved_content}\n
            Query: {user_query}\n
            """
    
    #Invoke the model with the prompt
    model_response = model.invoke(prompt)
    print("\nModel response:", model_response.content)