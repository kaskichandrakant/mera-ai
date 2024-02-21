from langchain_community.llms import GPT4All

from tools import sql_functions

llm = GPT4All(model='/Users/chandrakantkaski/project/explore/privateGPT/models/ggml-model-gpt4all-falcon-q4_0.bin',
              backend="llama")