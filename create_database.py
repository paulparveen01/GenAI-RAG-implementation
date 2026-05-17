# NOTE - this file needs to run single time as it will create embedding of your pdf data and store in vector db.
# steps Involved
# load pdf (using PyPDFLoader)
# split into chunks (using RecursiveCharacterTextSplitter)
# create the embeddings (using OpenAIEmbeddings)
# store into chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

data = PyPDFLoader("document loaders/deeplearning.pdf")
docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)
chunks = splitter.split_documents(docs)

embedding_model = OpenAIEmbeddings()

# it will create embedding of that chunks and store in vector db
vectorstore = Chroma.from_documents(
    documents = chunks,
    embedding = embedding_model,
    persist_directory= "chroma_db" 
)