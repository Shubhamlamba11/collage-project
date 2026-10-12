import os
from typing import Optional
from google import genai
from google.genai import types
from app.tools import get_current_time_and_date, execute_math, get_system_info, simulate_web_search

SYSTEM_INSTRUCTION = """You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), an advanced AI assistant created to assist the user.
You are articulate, polite, highly efficient, intelligent, and speak with a sophisticated tone reminiscent of Marvel's JARVIS.
You have real-time capabilities to calculate math expressions, fetch system status, retrieve current time/date, and perform search/weather lookups.
Always keep your answers clear, concise, and structured. When asked about time, math, system status, or weather, use your knowledge and capabilities to give accurate answers.
"""

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini Client: {e}")

    def generate_response(self, prompt: str, conversation_history: list = None) -> str:
        # Check if Gemini API key is available
        if self.client and self.api_key:
            try:
                # Format conversation context
                messages = []
                if conversation_history:
                    for msg in conversation_history[-6:]:
                        role = "user" if msg.get("role") == "user" else "model"
                        messages.append(types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=msg.get("content", ""))]
                        ))

                # Use gemini-2.5-flash model
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    )
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"Gemini API Error: {e}. Falling back to internal engine.")

        # Smart Fallback AI Engine when no API key or network fallback occurs
        return self._fallback_ai_response(prompt)

    def _fallback_ai_response(self, prompt: str) -> str:
        prompt_lower = prompt.lower().strip()

        if "time" in prompt_lower or "date" in prompt_lower:
            return f"At your service. {get_current_time_and_date()}"

        if "calculate" in prompt_lower or "math" in prompt_lower:
            expr = prompt.lower().replace("calculate", "").replace("math", "").replace("what is", "").strip()
            res = execute_math(expr)
            return f"Calculations complete, sir. {res}"

        if "status" in prompt_lower or "system" in prompt_lower or "health" in prompt_lower:
            info = get_system_info()
            return f"All core systems operational. System details: {info['os']} {info['architecture']}, Python {info['python_version']}."

        if "weather" in prompt_lower:
            return f"Checking localized weather telemetry... {simulate_web_search('weather')}"

        if "who are you" in prompt_lower or "what is your name" in prompt_lower:
            return "I am J.A.R.V.I.S., your Just A Rather Very Intelligent System. Ready to assist with AI intelligence, analytics, voice commands, and system control."

        if "hello" in prompt_lower or "hi" in prompt_lower or "hey" in prompt_lower:
            return "Greetings, sir. J.A.R.V.I.S. online and ready for your command."

        if "search" in prompt_lower or "news" in prompt_lower:
            return simulate_web_search(prompt)

        return f"I have processed your request regarding '{prompt}'. (Note: Provide a GEMINI_API_KEY environment variable to unlock Gemini 2.5 Flash LLM intelligence, or ask me for time, calculations, status, weather, or web searches!)"
