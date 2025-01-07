# from langchain_core.tools import tool
# from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
# import requests
# from dotenv import load_dotenv
# import os

# load_dotenv()

# @tool
# def get_weather(city:str):
#     """fetches current weather of given city using OpenWeathermap Api"""
#     weather_api_key = os.environ.get("WEATHER_API_KEY")
#     base_url = "https://api.openweathermap.org/data/2.5/weather"
    
#     params={
#         "q":city,
#         "appid":weather_api_key,
#         "units":"metric"
#     }
    
    
#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()
        
#         data = response.json()
#         tempreture = data["main"]["temp"]
#         weather_condition = data["weather"][0]["description"].capitalize()
        
#         return f"The weather in {city} is {weather_condition} with a temperature of {tempreture}°C."
    
#     except requests.exceptions.RequestException as e:
#         return f"Error: Unable to fetch weather data. Details: {e}"
#     except KeyError:
#         return "Error: Unexpected response format from the weather service."
    
    
    
    
# @tool
# def perform_calculation(expression:str):
#     """Perform a caluculation"""
#     try:
#         return str(eval(expression))
#     except Exception as e:
#         return f"Error: {e}"
    
    
# def interaction_with_llm(llms_with_tools, user_input):
#     system_prompt = SystemMessage("You are a smart assistant that can provide weather and calcaulations")
#     messages = [system_prompt, HumanMessage(content=user_input)]
#     ai_response = llms_with_tools.invoke(messages)
    
    
#     for tool_call in ai_response.tool_calls:
#         # Identify which tool to use
#         if tool_call["name"] == "get_weather":
#             tool_response = get_weather(*tool_call["args"])
#         elif tool_call["name"] == "perform_calculation":
#             tool_response = perform_calculation(*tool_call["args"])
#         else:
#             tool_response = "Error: Tool not recognized."

#         # Append tool response
#         messages.append(ToolMessage(content=tool_response, tool_call_id=tool_call["id"])) 
#     final_response = llms_with_tools.invoke(messages)
#     return final_response.content   


# from langchain_groq import ChatGroq
# llm = ChatGroq(groq_api_key = os.environ.get("GROQ_API_KEY"), model="llama3-70b-8192")
# llms_with_tools = llm.bind_tools([get_weather, perform_calculation])

# if __name__ == "__main__":
#     while True:
#         user_prompt = input("You: ")
#         assistant_response = interaction_with_llm(llms_with_tools, user_prompt)
#         print(f"Assistant: {assistant_response}")







from langchain_core.tools import tool
import requests
from dotenv import load_dotenv
import os
from langchain.memory import ConversationBufferMemory

load_dotenv()

@tool
def get_weather(city: str):
    """
    Fetches the current weather of a given city using the OpenWeatherMap API.
    
    **Parameters:**
    - `city` (str): The name of the city for which the weather information is required.
    
    **Returns:**
    - A string containing the weather description and temperature in the city.
    
    **Example Usage:**
    - Input: "Fetch the weather in New York."
    - Output: "The weather in New York is Clear sky with a temperature of 25°C."
    
    **Error Handling:**
    - If the city is not found or the API fails, an appropriate error message is returned.
    """
    weather_api_key = os.environ.get("WEATHER_API_KEY")
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        temperature = data["main"]["temp"]
        weather_condition = data["weather"][0]["description"].capitalize()

        return f"The weather in {city} is {weather_condition} with a temperature of {temperature}°C."

    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch weather data. Details: {e}"
    except KeyError:
        return "Error: Unexpected response format from the weather service."


@tool
def perform_calculation(expression: str):
    """
    Evaluates a mathematical expression provided by the user.
    
    **Parameters:**
    - `expression` (str): The mathematical expression to be evaluated. It should be in a valid Python syntax.
    
    **Returns:**
    - The result of the evaluated expression as a string.
    
    **Example Usage:**
    - Input: "What is 5 * (2 + 3)?"
    - Output: "25"
    
    **Error Handling:**
    - If the expression is invalid, an error message indicating the issue is returned.
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"



from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq

memory = ConversationBufferMemory(memory_key="conversation_history")
def interaction_with_llm(llms_with_tools, user_input):
    system_prompt = SystemMessage(
        content=(
            "You are a smart assistant capable of handling both general conversational queries and performing tasks like "
            "fetching weather updates or solving calculations. If a tool is needed but input is incomplete, ask follow-up "
            "questions to gather the required information. Otherwise, respond conversationally to general inputs."
        )
    )
    messages = [system_prompt, HumanMessage(content=user_input)]
    messages.extend(memory.load_memory_variables({}).get("history", []))

    # Get AI's initial response
    ai_response = llms_with_tools.invoke(messages)

    # Debugging: Log AI response
    print("AI Response (initial):", ai_response)

    # Handle non-tool responses directly
    if not ai_response.tool_calls:
        memory.save_context({"input": user_input}, {"output": ai_response.content})
        return ai_response.content  # Return conversational response if no tools are needed

    # Process tool calls
    for tool_call in ai_response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call.get("args", {})
        tool_response = None

        if tool_name == "get_weather":
            city = tool_args.get("city")
            if not city:
                # Handle missing argument dynamically
                tool_response = (
                    "It seems you want the weather, but I need to know the city name. "
                    "Could you please provide it?"
                )
            else:
                tool_response = get_weather.invoke(city)

        elif tool_name == "perform_calculation":
            expression = tool_args.get("expression")
            if not expression:
                # Handle missing argument dynamically
                tool_response = (
                    "I see you'd like to perform a calculation, but I need the expression to solve. "
                    "Could you please provide it?"
                )
            else:
                tool_response = perform_calculation.invoke(expression)

        else:
            # Unknown tool
            tool_response = f"Error: Unknown tool '{tool_name}' called."
        memory.save_context({"input": user_input}, {"output": tool_response})
        # Debugging: Log tool responses
        print(f"Tool Response ({tool_name}):", tool_response)

        # Append tool response as a message
        messages.append(ToolMessage(content=tool_response, tool_call_id=tool_call["id"]))

        # Handle dynamic follow-ups for incomplete arguments
        if "Could you please provide" in tool_response:
            return tool_response  # Return the follow-up question to the user

    # Get final AI response after tool usage
    final_response = llms_with_tools.invoke(messages)
    return final_response.content





from langchain_groq import ChatGroq
llm = ChatGroq(groq_api_key=os.environ.get("GROQ_API_KEY"), model="llama3-70b-8192")
llms_with_tools = llm.bind_tools([get_weather, perform_calculation])

if __name__ == "__main__":
    print("Assistant is ready! Type 'exit' to quit.")
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() == "exit":
            print("Goodbye!")
            break

        assistant_response = interaction_with_llm(llms_with_tools, user_prompt)
        print(f"Assistant: {assistant_response}")
        
# # function to calculate the factorial of a number
# def factorial(x):
#     if x == 1:
#         return 1
#     else:
#         return x * factorial(x-1)