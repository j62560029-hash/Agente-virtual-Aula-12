import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Agente de Venda de Veículos",
    page_icon="🚗",
    layout="centered"
)

# Função para inicializar a IA CORRIGIDA
def inicializar_ia():
    # Pega a chave da variável de ambiente
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("API_KEY")
    
    if not api_key:
        st.error("⚠️ Chave de API não encontrada! Verifique o arquivo .env ou as variáveis do Render.")
        st.stop()

    # Cria o cliente SEM o parâmetro proxies (que causava o erro)
    cliente = OpenAI(
        base_url="https://openrouter.ai/api/v1",  # Endereço oficial do OpenRouter
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://aula-12.onrender.com",  # Seu endereço do Render
            "X-Title": "Agente Venda Veículos"
        }
    )
    return cliente

# Inicializa o cliente
try:
    cliente_ia = inicializar_ia()
except Exception as e:
    st.error(f"❌ Erro ao conectar na IA: {str(e)}")
    st.stop()

# Título
st.title("🚗 Agente Virtual de Venda de Veículos")
st.write("Converse com nosso assistente para saber mais sobre veículos, condições e negociação!")

# Histórico da conversa
if "historico" not in st.session_state:
    st.session_state.historico = [
        {"role": "system", "content": "Você é um assistente especializado em venda de veículos. Responda de forma clara, educada e objetiva, focando em ajudar o usuário com dúvidas sobre carros, preços, condições de pagamento e negociação."}
    ]

# Mostra as mensagens
for mensagem in st.session_state.historico[1:]:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# Entrada do usuário
pergunta = st.chat_input("Digite sua pergunta sobre veículos...")

if pergunta:
    # Adiciona a pergunta ao histórico
    st.session_state.historico.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = cliente_ia.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct",  # Modelo gratuito/compatível
                messages=st.session_state.historico,
                temperature=0.7,
                max_tokens=1000
            )
            texto_resposta = resposta.choices[0].message.content
            st.markdown(texto_resposta)
    
    # Salva a resposta no histórico
    st.session_state.historico.append({"role": "assistant", "content": texto_resposta})
    
