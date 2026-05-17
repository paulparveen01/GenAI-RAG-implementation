# That is just demonstration purpose on how you can load text file content, main integration is written in main.py

from langchain_community.document_loaders import TextLoader

data = TextLoader("document loaders/notes.txt")

docs = data.load()

print(docs)