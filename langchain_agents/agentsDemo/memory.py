import os
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory, ConversationSummaryBufferMemory, ConversationBufferWindowMemory, CombinedMemory
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(api_key=os.environ["GROQ_API_KEY"])
buffer_memory = ConversationBufferMemory()

conversation_chain = ConversationChain(
    llm=llm,
    memory = buffer_memory,
    verbose = True
)


print(conversation_chain.predict(input="Hi, my name is Alice."))
print(conversation_chain.predict(input="What's my name?"))
print(conversation_chain.predict(input="Tell me a fun fact about my name."))