import pytest
from app.tools import get_current_time_and_date, execute_math, get_system_info, simulate_web_search

def test_get_current_time_and_date():
    res = get_current_time_and_date()
    assert "Current date and time:" in res

def test_execute_math_valid():
    res = execute_math("2 + 2 * 10")
    assert "Result: 22" in res

def test_execute_math_pow():
    res = execute_math("pow(2, 3)")
    assert "Result: 8" in res

def test_execute_math_invalid():
    res = execute_math("import os; os.system('ls')")
    assert "Result:" in res or "Math Evaluation Error" in res

def test_get_system_info():
    info = get_system_info()
    assert "os" in info
    assert "architecture" in info
    assert info["status"] == "JARVIS Systems Operational"

def test_simulate_web_search():
    res_weather = simulate_web_search("weather in New York")
    assert "Simulated Weather Data" in res_weather

    res_news = simulate_web_search("global news")
    assert "Simulated Global News Briefing" in res_news

    res_gen = simulate_web_search("quantum physics")
    assert "Search results for 'quantum physics'" in res_gen
