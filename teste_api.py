# teste_api.py
import os
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()  # carrega o .env antes de tudo

client = Anthropic()  # busca ANTHROPIC_API_KEY do ambiente automaticamente

resposta = client.messages.create(
    model="claude-haiku-4-5-20251001",  # mais rápido e barato para uso diário
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Responda em português: Olá, você está funcionando?"}
    ]
)

print(resposta.content[0].text)