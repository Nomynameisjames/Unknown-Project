#!/usr/bin/env python3
"""response = ollama.chat(model='llama3', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content']) """

"""from llama_index.llms.ollama import Ollama

try:
    llm = Ollama(model="codellama")
    res = llm.complete("write a function that multiply two matrices")
    print(res)
except Exception as e:
    print(e) """

import os
from dotenv import load_dotenv

load_dotenv()

os.environ["REPLICATE_API_TOKEN"] = "API-KEY"

from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.replicate import Replicate
from transformers import AutoTokenizer

# set the LLM
llama2_7b_chat = "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e"
Settings.llm = Replicate(
    model=llama2_7b_chat,
    temperature=0.01,
    additional_kwargs={"top_p": 1, "max_new_tokens": 300},
)

# set tokenizer to match LLM
Settings.tokenizer = AutoTokenizer.from_pretrained(
    "NousResearch/Llama-2-7b-chat-hf"
)

# set the embed model
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",

)

documents = SimpleDirectoryReader("file").load_data()
#index = VectorStoreIndex.from_documents(
#    documents,
#)
try:
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
except FileNotFoundError:
    index = VectorStoreIndex.from_documents(
    documents,
)
    index.storage_context.persist()

if __name__ == "__main__":

    
    query_engine = index.as_query_engine()
    result = query_engine.query("highlight the limitations")
    #res = index.storage_context.persist()
    print(result)
    
