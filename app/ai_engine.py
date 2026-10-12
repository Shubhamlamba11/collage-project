import time
import asyncio
from typing import Dict, Any, Optional
from app.gemini_client import GeminiClient
from app.memory import memory_store

class AIEngine:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl = 300  # 5 minutes cache TTL

    async def process_query_async(self, user_query: str, use_cache: bool = True) -> str:
        clean_query = user_query.strip()
        if not clean_query:
            return "How may I assist you, sir?"

        # Check in-memory cache for exact query matching
        now = time.time()
        cache_key = clean_query.lower()
        if use_cache and cache_key in self.cache:
            entry = self.cache[cache_key]
            if now - entry["timestamp"] < self.cache_ttl:
                return entry["response"]

        # Record user query in conversation memory
        memory_store.add_message("user", clean_query)
        history = memory_store.get_formatted_history()

        # Generate response asynchronously in thread pool to prevent blocking event loop
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            self.gemini_client.generate_response,
            clean_query,
            history
        )

        # Record assistant response in memory
        memory_store.add_message("assistant", response)

        # Cache response
        if use_cache:
            self.cache[cache_key] = {
                "response": response,
                "timestamp": now
            }

        return response

    def set_api_key(self, api_key: str):
        self.gemini_client = GeminiClient(api_key=api_key)

ai_engine_instance = AIEngine()
