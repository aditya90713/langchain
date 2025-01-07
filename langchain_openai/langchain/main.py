import openai
from dotenv import load_dotenv
import os



load_dotenv()

secret_key=os.getenv("OPENAI_API_KEY")


# from huggingface_hub import InferenceClient

# # Replace with your API token from Hugging Face
# client = InferenceClient(model="gpt2", token=secret_key)

# # Perform text generation
# response = client.text_generation("What is the capital of France?", max_new_tokens=50)
# print(response)






# print(openai.api_key)


# try:
#     models = openai.models.list()
#     print("Api key is working. Models Available")
#     print(models)
# except openai.error.AuthenticationError:
#     print("Invalid Api Key.")
# except Exception as e:
#     print(f"An error is {e}")

# from langchain_community.chat_models import ChatOpenAI


# llm = ChatOpenAI(
#     openai_api_key=secret_key,
#     temperature=0,
#     max_tokens=50,
#     model="gpt-3.5-turbo"
# )

# try:
#     response = llm.invoke("What is the capital of India?")
#     print(response)
# except Exception as e:
#     print(f"An error occurred: {e}")



# llm = openai(
#     temperature=0,  # Lower temperature ensures deterministic outputs (saves tokens)
#     max_tokens=50,  # Limit token usage
#     openai_api_key=openai.api_key
# )

# response = llm("What is the capital of France?")
# print(response)