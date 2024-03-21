import os
import json

import bittensor as bt

from insights.llm.base_llm import BaseLLM
from insights.llm.prompts import query_schema
from insights.protocol import Query, QueryOutput, NETWORK_BITCOIN

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from neurons.setup_logger import setup_logger

logger = setup_logger("OpenAI LLM")

class OpenAILLM(BaseLLM):
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY") or ""
        if not api_key:
            raise Exception("OpenAI_API_KEY is not set.")

        self.chat = ChatOpenAI(api_key=api_key, model="gpt-4", temperature=0)
        
    def build_query_from_text(self, query_text: str) -> Query:
        messages = [
            SystemMessage(
                content=query_schema
            ),
            HumanMessage(
                content=query_text
            ),
        ]
        try:
            ai_message = self.chat.invoke(messages)
            query = json.loads(ai_message.content)
            return Query(
                network=NETWORK_BITCOIN,
                type=query["type"] if "type" in query else None,
                target=query["target"] if "target" in query else None,
                where=query["where"] if "where" in query else None,
                limit=query["limit"] if "limit" in query else None,
                skip=query["skip"] if "skip" in query else None,
            )
        except Exception as e:
            bt.logging.error(f"LlmQuery build error: {e}")
            return None
        
    def interpret_result(self, query_text: str, result: dict) -> str:
        bt.logging.info(f"query_text: {query_text}")
        bt.logging.info(f"result: {result}")
        return "Interpreted result"
        
    def generate_llm_query_from_query(self, query: Query) -> str:
        pass
    