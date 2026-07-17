# CORREÇÃO DE CODIFICAÇÃO — COLOQUEI AQUI NO INÍCIO
import sys
sys.stdout.reconfigure(encoding='utf-8')

import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Agente de Venda de Veiculos",  # Sem acento no título da página
    page_icon="🚗",
    layout="centered"
)

def inicializar_ia():
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        st.error("⚠️ Chave de API nao encontrada! Verifique as variáveis do Render.")
        st.stop()

    cliente = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://aula-12.onrender.com",
            "X-Title": "Agente Venda Veiculos",
            "Content-Type": "application/json; charset=utf-8"
        }
    )
    return cliente

try:
    cliente_ia = inicializar_ia()
except Exception as e:
    st.error(f"❌ Erro ao conectar: {str(e)}")
    st.stop()

st.title("🚗 Agente Virtual de Venda de Veículos")
st.write("Converse com nosso assistente para saber mais sobre veículos, condições e negociação!")

if "historico" not in st.session_state:
    st.session_state.historico = [
        {"role": "system", "content": "Voce é um assistente especializado em venda de veiculos. Responda sempre em portugues do Brasil, de forma clara, educada e objetiva, focando em ajudar com duvidas sobre carros, precos, condicoes de pagamento e negociacao."}
    ]

for mensagem in st.session_state.historico[1:]:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta = st.chat_input("Digite sua pergunta sobre veiculos...")

if pergunta:
    st.session_state.historico.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Processando..."):
            resposta = cliente_ia.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct",
                messages=st.session_state.historico,
                temperature=0.7,
                max_tokens=1000
            )
            texto_resposta = resposta.choices[0].message.content
            st.markdown(texto_resposta)
    
    st.session_state.historico.append({"role": "assistant", "content": texto_resposta})
    
