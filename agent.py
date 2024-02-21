from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

from langchain_model import llm
from prompt import analyst_prompt

analyst_agent = (
        {
            "question": lambda x: x["question"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"]),
        }
        | analyst_prompt
        | llm
        | OpenAIFunctionsAgentOutputParser()
)
