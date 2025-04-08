import ollama

response = ollama.chat(
    model="qwen2.5-coder:1.5b",
    messages=[{"role": "user", "content": "Hello, Ollama!"}],
    stream=False
)

print(response)