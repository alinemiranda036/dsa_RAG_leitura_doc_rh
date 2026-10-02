# 🧑‍💼 RAG para Leitura de Documentos de RH

Um projeto de **RAG (Retrieval-Augmented Generation)** voltado para responder perguntas sobre políticas internas de RH e documentos corporativos armazenados em PDF, com busca semântica, recuperação de contexto e geração de respostas com IA.

## 📋 Descrição do Projeto

Este repositório implementa um assistente corporativo para responder dúvidas relacionadas a:

- **Férias e licenças**
- **Home office e presença remota**
- **Políticas internas da empresa**
- **Benefícios e regras operacionais**
- **Documentos de RH em formato PDF**

A solução combina:

- **Leitura de PDFs**
- **Chunking e indexação de documentos**
- **Embeddings semânticos**
- **Banco vetorial em ChromaDB**
- **LLM via Groq**
- **Interface em Streamlit**

## 🎯 Caso de Uso

Ideal para:
- 🏢 **Times de RH**: consultar políticas internas com mais rapidez
- 🤖 **Assistentes corporativos**: responder dúvidas frequentes dos colaboradores
- 📚 **Base de conhecimento documental**: organizar regras internas em um sistema inteligente
- 🔍 **Busca semântica em políticas**: encontrar respostas mesmo com linguagem natural
- 🎓 **Estudo de RAG em ambiente corporativo**

## 🏗️ Arquitetura

```
┌──────────────────────────────────────────────────────────────┐
│              Documentos de RH em PDF                        │
│  Políticas internas, benefícios, regras corporativas        │
└────────────────┬─────────────────────────────────────────────┘
                 │
         ┌───────▼────────────┐
         │  PyPDFDirectoryLoader │
         │  Leitura dos PDFs   │
         └───────┬────────────┘
                 │
         ┌───────▼────────────┐
         │ RecursiveTextSplitter │
         │ Divide em chunks    │
         │ (1000 chars / 200 overlap) │
         └───────┬────────────┘
                 │
         ┌───────▼────────────┐
         │  Embeddings        │
         │  all-MiniLM-L6-v2  │
         └───────┬────────────┘
                 │
         ┌───────▼────────────┐
         │  ChromaDB          │
         │  Base vetorial     │
         │  persistência local │
         └───────┬────────────┘
                 │
         ┌───────▼────────────┐
         │  Retriever        │
         │  busca top-k=3    │
         └───────┬────────────┘
                 │
         ┌───────▼────────────┐
         │  Groq + LLM       │
         │  Geração da resposta │
         └────────────────────┘
```

## 📁 Estrutura do Projeto

```
dsa_RAG_leitura_doc_rh/
├── dsa_app.py              # Interface Streamlit com chat corporativo
├── dsa_rag_engine.py       # Motor principal do RAG
├── requirements.txt        # Dependências do projeto
├── chroma_db_data/         # Banco vetorial persistido localmente
├── README.md               # Este arquivo
└── [PDFs de políticas]     # Documentos internos carregados pelo usuário
```

## 🚀 Como Executar

### 1️⃣ Pré-requisitos

- Python 3.10+
- pip
- Chave da API da Groq
- PDF(s) com políticas internas de RH

### 2️⃣ Instalação

```bash
# Clone o repositório
git clone https://github.com/alinemiranda036/dsa_RAG_leitura_doc_rh.git
cd dsa_RAG_leitura_doc_rh

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/macOS
# ou
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 3️⃣ Configurar a API da Groq

Crie um arquivo `.env` na raiz do projeto:

```bash
echo "GROQ_API_KEY=sua_chave_aqui" > .env
```

### 4️⃣ Iniciar a aplicação

```bash
streamlit run dsa_app.py
```

Acesse `http://localhost:8501`.

## 🔧 Componentes Principais

### 1. `dsa_app.py` - Interface do assistente

A interface em Streamlit contém:

- upload de PDFs de políticas corporativas
- processamento e ingestão dos documentos
- chat interativo com o assistente
- exibição de fontes consultadas e metadados
- botão para limpar o banco vetorial

**Fluxo do chat:**

```python
response_payload = rag_engine.get_response(prompt)
answer = response_payload['result']
sources = response_payload['source_documents']
```

### 2. `dsa_rag_engine.py` - Motor de RAG

É o núcleo da solução. Possui:

- `DSARAGEngine.__init__()`
- `ingest_documents(temp_dir_path)`
- `get_response(query)`
- `clear_database()`

**Funcionamento:**

```python
# Leitura de PDFs
documents = loader.load()

# Quebra em chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# Indexação no banco vetorial
self.vector_store.add_documents(documents=chunks)

# Busca por recuperação
a = RetrievalQA.from_chain_type(
    llm=self.llm,
    retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
)
```

## 🧠 Como o RAG funciona aqui

O sistema segue esta lógica:

1. O PDF com políticas internas é carregado
2. O conteúdo é segmentado em chunks
3. Cada chunk é convertido em embedding
4. A pergunta do colaborador é transformada em embedding
5. O sistema busca os chunks mais relevantes no ChromaDB
6. O modelo LLM recebe esse contexto e responde em linguagem natural

**Vantagem:**
- considera o contexto real do documento
- reduz respostas fabricadas
- funciona bem para políticas internas e regras corporativas

## 📚 Exemplos de Perguntas

Você pode perguntar:

- "Qual a antecedência mínima para solicitar férias?"
- "Há necessidade de presença física em algum momento no home office?"
- "Posso instalar softwares por conta própria no computador da empresa?"
- "Quais são as regras para benefício de auxílio-creche?"
- "Existe restrição para trabalho remoto?"

## ⚙️ Configuração Avançada

### Ajustar número de chunks recuperados

No `dsa_rag_engine.py`:

```python
search_kwargs = {"k": 3}
```

Você pode aumentar para 5 ou 10 se quiser mais contexto.

### Ajustar chunking

```python
RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
```

É bom equilibrar:
- chunks muito pequenos: perdem contexto
- chunks muito grandes: piora a recuperação

### Trocar o modelo de embedding

```python
self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

Você pode trocar por outros modelos da Hugging Face conforme necessidade.

## 📊 Fluxo de uso da aplicação

```text
Usuário faz input -> sistema busca no banco vetorial -> LLM responde com contexto -> exibe fontes consultadas
```

A interface mostra também os metadados dos documentos utilizados, como:
- fonte
- página
- trecho recuperado

## 🛡️ Segurança e Privacidade

- ✅ Processamento local dos PDFs e embeddings
- ✅ Persistência local em ChromaDB
- ✅ Respostas baseadas no contexto documental
- ⚠️ Sempre confirmar informações críticas antes de usar em decisões administrativas
- ⚠️ Em ambiente real, recomenda-se controle de acesso e auditoria

## 📈 Melhorias Futuras

- [ ] Suporte a múltiplos tipos de documentos (Word, TXT, HTML)
- [ ] Sistema de autenticação para uso interno
- [ ] Histórico de conversas por usuário
- [ ] FAQ automática baseada em documentos
- [ ] Extração de metadados adicionais por página
- [ ] API REST para integração interna
- [ ] Dashboard de qualidade e métricas de recuperação
- [ ] Suporte a documentos em outros idiomas

## 🤝 Contribuindo

Contribuições são bem-vindas! Você pode:
1. Melhorar o mecanismo de busca
2. Adicionar suporte a novos tipos de documentos
3. Melhorar a interface de chat
4. Expandir o sistema de metadata e filtros
5. Reportar bugs ou sugerir melhorias

## 📝 Licença

Este projeto é fornecido como material educacional e de demonstração.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação do LangChain: https://python.langchain.com/
- Consulte a documentação do ChromaDB: https://docs.trychroma.com/
- Consulte a documentação da Groq: https://console.groq.com/docs
- Consulte o Hugging Face: https://huggingface.co/

## 🎓 Recursos e Referências

- [LangChain Documentation](https://python.langchain.com/docs/)
- [Hugging Face Embeddings](https://huggingface.co/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Groq API Docs](https://console.groq.com/docs)
- [RAG Patterns](https://python.langchain.com/docs/tutorials/retrievers/)

---

**Desenvolvido com ❤️ para a comunidade de IA aplicada a RH e conhecimento interno**
