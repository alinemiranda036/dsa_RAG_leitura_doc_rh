# Projeto 1 - Assistente Corporativo de Perguntas e Respostas com RAG Sobre Documentos Internos
# Módulo da App

# Imports
import os
import tempfile
import streamlit as st
from dsa_rag_engine import rag_engine

# Variável de ambiente
# Evita um comportamento indesejado do Hugging Face Tokenizers quando usado dentro de aplicações que executam várias threads em paralelo, 
# como Streamlit, FastAPI ou Jupyter.
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Configuração Inicial da Aplicação Streamlit
st.set_page_config(
    page_title="Engenharia de Dados para IA - Data Science Academy",  # Título que aparece na aba do navegador
    page_icon="🤖",                      # Ícone (emoji) que aparece na aba do navegador
    layout="wide",                      # Define o layout da página para usar a largura total da tela
    initial_sidebar_state="expanded",   # Garante que a sidebar (menu lateral) comece aberta
)
# Estilização customizada (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Reduz o espaço vazio no topo da página */
    .block-container {
        padding-top: 2rem;
    }

    /* Fundo em degradê para o app inteiro */
    .stApp {
        background: linear-gradient(160deg, #0F172A 0%, #14224a 45%, #0B1220 100%);
    }

    /* Bolhas de chat mais suaves */
    div[data-testid="stChatMessage"] {
        border-radius: 14px;
        border: 1px solid #1E293B;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
        padding: 0.5rem 0.25rem;
    }

    /* Botão: gradiente azul + sombra + brilho espelhado no topo */
    .stButton > button {
        position: relative;
        overflow: hidden;
        border-radius: 999px;
        border: none;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.3rem;
        background: linear-gradient(180deg, #2C5282 0%, #1A365D 100%);
        box-shadow:
            0 4px 14px rgba(59, 130, 246, 0.45),
            inset 0 1px 0 rgba(255, 255, 255, 0.25);
        transition: all 0.2s ease;
    }

    /* Faixa de "reflexo" na metade superior do botão (efeito espelhado) */
    .stButton > button::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 50%;
        background: linear-gradient(180deg, rgba(255,255,255,0.35) 0%, rgba(255,255,255,0) 100%);
        pointer-events: none;
    }

    .stButton > button:hover {
        background: linear-gradient(180deg, #2B6CB0 0%, #2C5282 100%);
        box-shadow:
            0 6px 20px rgba(59, 130, 246, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }

    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)


# Títulos
st.markdown("""
<div style="text-align:center; padding: 0.5rem 0 1.5rem 0;">
    <h1 style="margin-bottom:0;">🤖 Assistente de RH Corporativo</h1>
    <p style="color:#94A3B8; font-size:0.95rem; margin-top:0.3rem;">
        Engenharia de Dados para IA · Data Science Academy
    </p>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ Sobre este sistema", expanded=True):
    st.markdown("""
    Este sistema utiliza **RAG (Retrieval-Augmented Generation)** para responder perguntas 
    baseadas nas políticas internas da empresa.
    - Modelo de Embeddings: `all-MiniLM-L6-v2` (Hugging Face)
    - Modelo de LLM: `openai/gpt-oss-120b` (Groq)
    - Vetorização e Indexação: `ChromaDB`
    - Framework: `LangChain`
    """)

with st.expander("💡 Perguntas modelo", expanded=False):
    st.markdown("""
    - Qual a antecedência mínima para solicitação de férias?
    - Há necessidade de presença física em algum momento no modelo de trabalho remoto?
    - Posso instalar softwares por conta própria no computador da empresa?
    """)


# --- Sidebar: Área de Gestão de Documentos (CRUD e Ingestão) ---
with st.sidebar:

    st.header("⚙️ Gestão de Conhecimento")
    
    # Upload de arquivos
    uploaded_files = st.file_uploader(
        "📄 Carregar Novas Políticas (PDF)",
        type = ["pdf"], 
        accept_multiple_files = True
    )
    
    if st.button("📂 Processar Documentos"):
        
        if uploaded_files:
            
            with st.spinner("Processando (Lendo, Vetorizando e Indexando)..."):
                
                # Cria diretório temporário para salvar os arquivos para o Loader ler
                with tempfile.TemporaryDirectory() as temp_dir:
                    
                    for uploaded_file in uploaded_files:
                        
                        file_path = os.path.join(temp_dir, uploaded_file.name)
                        
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                    
                    # Chama a engine para processar
                    result_msg = rag_engine.ingest_documents(temp_dir)

                    st.success(result_msg)
        else:
            st.warning("Por favor, faça upload de arquivos PDF.")

    st.markdown("---")

    st.markdown("⚠️ Ao acionar o botão abaixo o banco de dados vetorizado criado com base no PDF importado será deletado.")

    if st.button("🗑️ Limpar Banco de Dados"):
        msg = rag_engine.clear_database()
        st.warning(msg)

    st.markdown("---")

    st.sidebar.markdown(
        """
        <div style="background-color:#1A365D; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px;">
            <h3 style="color:white; margin:0; font-weight:bold;">Dúvidas?</h3>
            <p style="color:white; margin:0; font-weight:bold; font-size:0.7rem; white-space:nowrap;">suporte@datascienceacademy.com.br</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Área Principal: Chat ---

# Inicializa histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Pergunte sobre férias, benefícios, home office..."):
    
    # 1. Adiciona pergunta ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Gera resposta usando o RAG Engine
    with st.chat_message("assistant"):
        
        with st.spinner("Consultando base vetorial..."):
            
            # Obtém a resposta completa
            response_payload = rag_engine.get_response(prompt)
            
            # Extrai a resposta
            answer = response_payload['result']
            
            # Extrai os metadados
            sources = response_payload['source_documents']
            
            # Exibe a resposta
            st.markdown(answer)
            
            # --- Exibindo Metadados ---
            with st.expander("📚 Fontes Consultadas (Metadados)"):
                
                for doc in sources:
                    
                    # Extrai metadados do documento recuperado
                    source_name = doc.metadata.get('source', 'Desconhecido')
                    page_num = doc.metadata.get('page', 'N/A')
                    preview = doc.page_content[:150] + "..."
                    
                    st.markdown(f"**Fonte:** `{os.path.basename(source_name)}` | **Página:** `{page_num}`")
                    st.caption(f"Trecho: {preview}")

    # 3. Adiciona resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": answer})


# Fim
