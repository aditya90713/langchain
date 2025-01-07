import os
from groq import Groq
from dotenv import load_dotenv  

# Load environment variables from .env file
load_dotenv()

# Create the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initial system prompt
system_prompt = {
    "role": "system",
    "content": "You are a helpful assistant. You reply with very short answers."
}

chat_history = [system_prompt]

while True:
    # Get user input from the console
    user_input = input("You: ")
    chat_history.append({"role": "user", "content": user_input})

    # Call Groq API for a chat completion
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=100,
        temperature=1.2
    )

    # Add assistant's response to the chat history
    chat_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })

    # Print the assistant's response
    print("Assistant:", response.choices[0].message.content)
