import datetime
import math
import platform
import os
import re

def get_current_time_and_date():
    now = datetime.datetime.now()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S (%A)')}"

def execute_math(expression: str) -> str:
    """Safely evaluates math expressions."""
    # Clean expression
    cleaned = re.sub(r'[^a-zA-Z0-9\+\-\*\/\%\(\)\.\s\,]', '', expression)
    if not cleaned.strip():
        return "Invalid math expression."
    try:
        # Safe evaluation namespace
        safe_dict = {
            "abs": abs, "round": round, "min": min, "max": max,
            "pow": pow, "sqrt": math.sqrt, "sin": math.sin,
            "cos": math.cos, "tan": math.tan, "pi": math.pi, "e": math.e
        }
        result = eval(cleaned, {"__builtins__": None}, safe_dict)
        return f"Result: {result}"
    except Exception as e:
        return f"Math Evaluation Error: {str(e)}"

def get_system_info():
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "status": "JARVIS Systems Operational"
    }

def simulate_web_search(query: str) -> str:
    query_lower = query.lower()
    if "weather" in query_lower:
        return "Simulated Weather Data: Currently 22°C (72°F) with clear skies and 45% humidity."
    elif "news" in query_lower:
        return "Simulated Global News Briefing: Quantum computing milestone achieved; Renewable energy grid efficiency hits record high."
    else:
        return f"Search results for '{query}': JARVIS Knowledge Base updated with latest global telemetry on {query}."
