# import os
# import requests
# from langchain.chains import LLMChain
# from langchain.prompts import (
#     ChatPromptTemplate,
#     HumanMessagePromptTemplate,
#     MessagesPlaceholder,
# )
# from langchain_core.messages import SystemMessage
# from langchain.chains.conversation.memory import ConversationBufferWindowMemory
# from langchain_groq import ChatGroq
# from langchain.agents import initialize_agent, Tool
# from langchain.tools import tool
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()


# # Mock Search Tool
# @tool
# def search_tool(query: str) -> str:
#     """
#     Simulates a search engine query.
#     """
#     mock_database = {
#         "capital of france": "The capital of France is Paris.",
#         "capital of germany": "The capital of Germany is Berlin.",
#         "best programming language": "The best programming language depends on your use case, but Python is widely popular.",
#         "capital of japan": "The capital of Japan is Tokyo.",
#         "who is the president of the usa": "The president of the USA is Joe Biden."
#     }

#     return mock_database.get(query.lower(), "Sorry, I couldn't find an answer to your question. Please try again or ask something else.")


# @tool
# def get_weather(city: str):
#     """
#     Fetches the current weather of a given city using the OpenWeatherMap API.
#     """
#     weather_api_key = os.environ.get("WEATHER_API_KEY")
#     base_url = "https://api.openweathermap.org/data/2.5/weather"

#     params = {
#         "q": city,
#         "appid": weather_api_key,
#         "units": "metric"
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()
#         data = response.json()
#         temperature = data["main"]["temp"]
#         weather_condition = data["weather"][0]["description"].capitalize()

#         return f"The weather in {city} is {weather_condition} with a temperature of {temperature}°C."

#     except requests.exceptions.RequestException as e:
#         return f"Error: Unable to fetch weather data. Details: {e}"
#     except KeyError:
#         return "Error: Unexpected response format from the weather service."


# @tool
# def perform_calculation(expression: str):
#     """
#     Evaluates a mathematical expression provided by the user.
#     """
#     try:
#         return str(eval(expression))
#     except Exception as e:
#         return f"Error: {e}"

# # Dynamically handle non-searchable queries like greetings using LLM
# def handle_non_searchable_queries(user_input: str) -> str:
#     """
#     Use the LLM to dynamically determine if the user input is a general conversation query.
#     If so, respond appropriately without using the search tool.
#     """
#     # Initialize the LLM (Groq) for conversation handling
#     groq_api_key = os.environ.get("GROQ_API_KEY")
#     model = "llama3-8b-8192"
#     groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model)

#     # Create a prompt template for handling casual conversations and greetings
#     system_prompt = "You are a helpful assistant. Respond to casual greetings and other general conversations naturally. If the query is not related to specific tools, provide a conversational response."

#     prompt = ChatPromptTemplate.from_messages([
#         ("system", system_prompt),
#         ("human", "{user_input}")
#     ])

#     # Generate response using LLM
#     response = groq_chat.predict(user_input)
#     return response.strip()

# def main():
#     """
#     Main entry point for the chatbot application.
#     """
#     # Initialize the Groq chat LLM
#     groq_api_key = os.environ.get("GROQ_API_KEY")
#     model = "llama3-8b-8192"
#     groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model)

#     print(
#         "Hello! I'm your friendly Groq chatbot. I can answer your questions, fetch data, or just chat!"
#     )

#     # Define memory for conversation history
#     memory_length = 5
#     memory = ConversationBufferWindowMemory(
#         k=memory_length, memory_key="chat_history", return_messages=True
#     )

#     # Define tools for the agent
#     tools = [
#         Tool(
#             name="Search Tool",
#             func=search_tool.run,
#             description="Use this tool to search for information online, like general knowledge, facts, or specific questions. If I don't know the answer, I'll try to find it for you."
#         ),
#         Tool(
#             name="Perform Mathematical Operations",
#             func=perform_calculation.run,
#             description="Use this tool to perform calculations and solve mathematical expressions."
#         ),
#         Tool(
#             name="Weather Tool",
#             func=get_weather.run,
#             description="Use this tool to fetch the current weather of a given city using the OpenWeatherMap API."
#         )
#     ]
# # Define the system prompt for the agent
#     system_prompt = "You are a helpful assistant. Use available tools to answer the user's question. If the question cannot be answered by tools, respond with a natural conversational reply."

#     # Create a prompt template with the system message
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", system_prompt),
#         ("human", "{user_input}")
#     ])

#     # Initialize the agent with tools, LLM, and prompt
#     agent = initialize_agent(
#         tools=tools,
#         llm=groq_chat,
#         verbose=True
#     )

#     while True:
#         user_question = input("Ask a question: ")
#         if "bye" in user_question:
#             print("Goodbye! Have a great day!")
#             break

#         try:
#             # Try to run the agent to process the user question
#             response = agent.run(user_question)

#             # Check if the response is valid, if not, handle with non-searchable queries function
#             if not response or "Sorry" in response:
#                 response = handle_non_searchable_queries(user_question)

#             print("Chatbot:", response)

#         except Exception as e:
#             # Handle the agent stopping due to iteration/time limit or other errors
#             print("Error:", str(e))
#             # Fallback to handle non-searchable queries
#             response = handle_non_searchable_queries(user_question)
#             print("Chatbot:", response)


# if __name__ == "__main__":
#     main()



import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import load_tools, initialize_agent, AgentType,create_react_agent, AgentExecutor,create_structured_chat_agent
from langchain.tools import Tool,DuckDuckGoSearchRun


load_dotenv()


llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.7,
    model_kwargs={"top_p":0.8, "seed":1337}
)

# Zero-shot React Agent
search = DuckDuckGoSearchRun()
# def get_word_length(word:str)->int:
#     "returns the length of word"
#     return len(word)

tools = load_tools(['wikipedia', "llm-math"], llm=llm)
# zero_shot_agent = initialize_agent(
#     tools,
#     llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

# zero_shot_agent.invoke(
#     "What is the square root of the year Pythagoras was born?"
# )


# STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION Agent

# lan_and_execute_agent = initialize_agent(
#     tools, 
#     llm, 
#     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )


# lan_and_execute_agent.run("Find out who invented the telephone and calculate the number of years between that invention and the first moon landing."
# )


# 3. Creating Custom Tools for Agents

def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

word_length_tool = Tool(
    name="WordLength",
    func=get_word_length,
    description="Useful for greeting the length of a word"
)

# custom_tool = [word_length_tool]+tools
# custom_Agent = initialize_agent(
#     custom_tool, 
#     llm, 
#     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )


# custom_Agent.run(
#     "What's the length of the word 'supercalifragilisticexpialidocious' and its square root?"
# )
tools_web_search =[
    Tool(
        name="DuckDuckGo Search",
        func=search.run,
        description="Useful for searching the internet for current information"
    )
]

all_tools = tools + tools_web_search + [word_length_tool]

multi_tool_agent = initialize_agent(
    all_tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

multi_tool_agent.run(
    """Please perform the following tasks:
    1. Find the current temperature in New York City.
    2. Calculate the square root of that temperature.
    3. Find a famous quote about weather and tell me how many characters it has.
    Provide a summary of your findings.
    """
)