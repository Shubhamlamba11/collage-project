import pytest
from app.memory import ConversationMemory

def test_memory_add_and_get():
    memory = ConversationMemory(max_history=5)
    memory.clear()

    memory.add_message("user", "Hello JARVIS")
    memory.add_message("assistant", "Greetings sir")

    history = memory.get_formatted_history()
    assert len(history) == 2
    assert history[0] == {"role": "user", "content": "Hello JARVIS"}
    assert history[1] == {"role": "assistant", "content": "Greetings sir"}

def test_memory_max_history_limit():
    memory = ConversationMemory(max_history=3)
    memory.clear()

    for i in range(5):
        memory.add_message("user", f"Msg {i}")

    history = memory.get_formatted_history()
    assert len(history) == 3
    assert history[0]["content"] == "Msg 2"
    assert history[2]["content"] == "Msg 4"

def test_memory_clear():
    memory = ConversationMemory()
    memory.add_message("user", "Test")
    memory.clear()
    assert len(memory.get_formatted_history()) == 0
