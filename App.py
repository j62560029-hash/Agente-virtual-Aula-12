import os
import streamlit as st
from openai import OpenAI
from typing import Dict, List, Optional

st.set_page_config(
    page_title="Atendimento ROA Veículos",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inicializar_cliente_openrouter() -> Optional[OpenAI]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        st.error("Chave de API não configurada!")
        return None
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://render.com/",
            "X-Title": "ROA Veículos"
        }
    )

cliente = inicializar_cliente_openrouter()

DADOS_EMPRESA: Dict = {
    "nome": "ROA Veículos",
    "missao": "Oferecer os melhores veículos com atendimento rápido e transparente",
    "contato": "(19) 9XXXX-XXXX | atendimento@roaveiculos.com.br",
    "endereco": "Campinas - SP"
}

CATALOGO_VEICULOS: List[Dict] = [
    {"modelo": "HB20 0km", "preco": "R$ 79.990,00", "destaque": "Entrega imediata, até 60x"},
    {"modelo": "Corolla Usado", "preco": "R$ 95.900,00", "destaque": "Único dono, garantia de 1 ano"},
    {"modelo": "Compass 4x4", "preco": "R$ 149.990,00", "destaque": "Versão completa, pouca km"},
    {"modelo": "Fiorino Trabalho", "preco": "R$ 62.500,00", "destaque": "Pronto para uso comercial"}
]

CONTEXTO_SISTEMA = f"""
Você é o atendente virtual da {DADOS_EMPRESA['nome']}, especializado em venda de veículos.
- Seja educado e direto
- Use apenas esses dados: {CATALOGO_VEICULOS}
- Contato: {DADOS_EMPRESA['contato']}
- Não invente informações!
"""

def exibir_menu_lateral() -> None:
    st.sidebar.title(f"🚘 {DADOS_EMPRESA['nome']}")
    st.sidebar.subheader("Sobre nós")
    st.sidebar.write(DADOS_EMPRESA["missao"])
    st.sidebar.write(f"📍 {DADOS_EMPRESA['endereco']}")
    st.sidebar.write(f"📞 {DADOS_EMPRESA['contato']}")
    st.sidebar.divider()
    st.sidebar.subheader("Catálogo")
    for v in CATALOGO_VEICULOS:
        st.sidebar.markdown(f"**{v['modelo']}** — {v['preco']}\n✅ {v['destaque']}")

def exibir_tela_inicial() -> None:
    st.title("🚗 Atendimento Virtual ROA Veículos")
    st.subheader("Escolha seu veículo com a ajuda do nosso assistente!")
    st.write("Pergunte sobre preços, condições ou agende uma visita.")

def gerenciar_conversa() -> None:
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = [{"role": "system", "content": CONTEXTO_SISTEMA}]
    
    for msg in st.session_state.mensagens[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    pergunta = st.chat_input("Digite sua dúvida...")
    if pergunta and cliente:
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)
        
        try:
            with st.chat_message("assistant"):
                resposta_texto = ""
                resposta = cliente.chat.completions.create(
                    model="meta-llama/llama-3.1-8b-instruct:free",
                    messages=st.session_state.mensagens,
                    stream=True,
                    temperature=0.7
                )
                espaco = st.empty()
                for parte in resposta:
                    if parte.choices[0].delta.content:
                        resposta_texto += parte.choices[0].delta.content
                        espaco.markdown(resposta_texto)
                st.session_state.mensagens.append({"role": "assistant", "content": resposta_texto})
        except Exception as e:
            st.error(f"Erro: {str(e)}. Tente novamente mais tarde.")

if __name__ == "__main__":
    exibir_menu_lateral()
    exibir_tela_inicial()
    gerenciar_conversa()
