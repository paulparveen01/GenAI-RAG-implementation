# Note - This work as chat in terminal, for web version check app_ui_version file.

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# NOTE - Your RAG data is already stored in vector DB by running create_database.py script.

embedding_model = OpenAIEmbeddings()

# Load vector store
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

# Create Retriever
retriever = vectorstore.as_retriever(
    search_type = "mmr",
    search_kwargs = {
        "k": 4, # total need to return
        "fetch_k": 10, # total needs to fetch
        "lambda_mult": 0.5 # Diverse result variation, kind of temprature
    }
)

llm = ChatMistralAI(model = "mistral-small-2506")

# Define prompt template so that we can define Roles
promptTemplate = ChatPromptTemplate.from_messages(
    [
        ("system",
        """You are a helpful AI assistat.

        Use ONLY the provided context to answer the question.
        
        If the answer is not present in the context,
        say: "I could not find the answer in the document."
        """),
        ("human",
        """Context:
        {context}

        Question:
        {question}
        """)
     ]
)

print("Rag system created")
print("press 0 to exit")

while True:
    query = input("You: ")
    if query == "0":
        break

    docs = retriever.invoke(query) # It will give chunks
    context = "\n\n".join(
        [doc.page_content for doc in docs] # Join all chunks with \n
    )
    # Call LLM
    final_prompt = promptTemplate.invoke({
        "context": context,
        "question": query
    })

    response = llm.invoke(final_prompt)
    print(f"\n AI: {response.content}")


# Sample Questions: 
# 1. Can you tell me about the Word2Vec framework?