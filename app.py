import os
import sys
import streamlit as st
from openai import OpenAI

# ✅ ISSO AQUI ACABA COM O ERRO DE ACENTO PARA SEMPRE
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Configuração da página
st.set_page_config(page_title="Agente de Venda de Veículos", page_icon="🚗", layout="centered")

# Pega a chave direto das variáveis do Render
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    st.error("Chave da API não encontrada!")
    st.stop()

# Conecta no OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

# Interface
st.title("🚗 Agente Virtual de Venda de Veículos")
st.write("Converse com nosso assistente para saber mais sobre veículos, condições e negociação!")

# Histórico de conversa
if "chat" not in st.session_state:
    st.session_state.chat = [
        {"role": "system", "content": "Você é um atendente de loja de veículos. Responda SEMPRE em português do Brasil, com acentos e tudo certo, de forma simples e educada."}
    ]

# Mostra as mensagens
for mensagem in st.session_state.chat[1:]:
    st.chat_message(mensagem["role"]).write(mensagem["content"])

# Entrada do usuário
pergunta = st.chat_input("Digite sua pergunta sobre veículos...")
if pergunta:
    st.session_state.chat.append({"role": "user", "content": pergunta})
    st.chat_message("user").write(pergunta)

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.chat
    )
    texto = resposta.choices[0].message.content
    st.session_state.chat.append({"role": "assistant", "content": texto})
    st.chat_message("assistant").write(texto)
    
