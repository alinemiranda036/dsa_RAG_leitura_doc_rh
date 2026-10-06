# 🧑‍💼 RAG para Leitura de Documentos de RH

Um projeto de **RAG (Retrieval-Augmented Generation)** que responde perguntas sobre políticas internas de RH a partir de documentos em PDF, com busca semântica, recuperação de contexto e geração de respostas com IA.

## 📋 Descrição do Projeto

O repositório implementa um assistente corporativo: o usuário carrega os PDFs de políticas da empresa, o sistema indexa o conteúdo em um banco vetorial e um LLM responde às perguntas com base nos trechos recuperados, mostrando as fontes consultadas.

A solução combina:

- **Leitura de PDFs** com `PyPDFDirectoryLoader`
- **Chunking** com `RecursiveCharacterTextSplitter` (1000 caracteres, sobreposição de 200)
- **Embeddings** com o modelo `all-MiniLM-L6-v2` (Hugging Face), executado localmente
- **Banco vetorial** ChromaDB com persistência em disco
- **LLM** `openai/gpt-oss-120b` via API da Groq
- **Interface** em Streamlit

## 🎯 Caso de Uso

- 🏢 **Times de RH**: consultar políticas internas com mais rapidez
- 🤖 **Assistentes corporativos**: responder dúvidas frequentes dos colaboradores
- 🔍 **Busca semântica em políticas**: encontrar respostas com perguntas em linguagem natural
- 🎓 **Estudo de RAG em ambiente corporativo**

## 🏗️ Arquitetura

```
        INGESTÃO (botão "Processar Documentos")

┌──────────────────────────────┐
│  PDFs de políticas de RH     │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│  PyPDFDirectoryLoader        │  leitura dos PDFs
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│  RecursiveCharacterText-     │  chunks de 1000 caracteres
│  Splitter                    │  com sobreposição de 200
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│  Embeddings                  │  all-MiniLM-L6-v2 (local)
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│  ChromaDB                    │  coleção "rh_policies"
│  ./chroma_db_data            │  persistida em disco
└──────────────────────────────┘


        CONSULTA (chat)

┌──────────────────────────────┐
│  Pergunta do usuário         │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│  Retriever (ChromaDB)        │  3 chunks mais similares
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│  LLM via Groq                │  openai/gpt-oss-120b
│  (RetrievalQA, "stuff")      │  temperature = 0
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│  Resposta + fontes           │  arquivo, página e trecho
└──────────────────────────────┘
```

## 📁 Estrutura do Projeto

```
dsa_RAG_leitura_doc_rh/
├── dsa_app.py              # Interface Streamlit (upload, chat, fontes)
├── dsa_rag_engine.py       # Motor de RAG (ingestão, busca e resposta)
├── politicas_rh.pdf        # Documento de exemplo para testar o projeto
├── requirements.txt        # Dependências Python (versões fixadas)
├── .gitignore              # Arquivos e pastas que não vão para o repositório
└── README.md
```

Dois itens não fazem parte do repositório e ficam apenas na sua máquina (estão no `.gitignore`):

| Item | Origem | Conteúdo |
|------|--------|----------|
| `.env` | Criado por você no passo 3 | Sua chave da API da Groq |
| `chroma_db_data/` | Criada automaticamente ao iniciar o app | Banco vetorial do ChromaDB |

## 🚀 Como Executar

### 1️⃣ Pré-requisitos

| Requisito | Detalhe |
|-----------|---------|
| **Python 3.11 ou superior** | Recomendado 3.13. Com 3.10 a instalação falha, pois a versão fixada do `numpy` exige 3.11+ |
| **Chave da API da Groq** | Gratuita, criada em https://console.groq.com/keys |
| **Internet** | Para instalar as dependências, baixar o modelo de embeddings na primeira execução e chamar a API da Groq |
| **Espaço em disco** | De 2 a 8 GB para as bibliotecas, conforme o sistema operacional (o PyTorch é a maior parte) |

Não é preciso Docker nem GPU.

### 2️⃣ Clonar e instalar as dependências

```bash
git clone https://github.com/alinemiranda036/dsa_RAG_leitura_doc_rh.git
cd dsa_RAG_leitura_doc_rh
```

**Opção A — venv**

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

**Opção B — conda**

```bash
conda create --name rag_rh python=3.13
conda activate rag_rh
pip install -r requirements.txt
```

A instalação demora alguns minutos.

### 3️⃣ Configurar a chave da Groq

1. Acesse https://console.groq.com/keys, crie uma conta e gere uma chave (começa com `gsk_`)
2. Na raiz do projeto, crie um arquivo chamado `.env` em um editor de texto (VS Code, Bloco de Notas) com o conteúdo:

```
GROQ_API_KEY=sua_chave_aqui
```

Sem aspas e sem espaços ao redor do `=`. No Windows, confira se o arquivo não foi salvo como `.env.txt`.

> O `.env` está no `.gitignore`. Nunca envie sua chave para o GitHub.

### 4️⃣ Iniciar a aplicação

Execute a partir da raiz do projeto:

```bash
streamlit run dsa_app.py
```

O navegador abre em http://localhost:8501. Na primeira execução o modelo de embeddings (~90 MB) é baixado do Hugging Face, então a tela pode levar um pouco mais para aparecer.

### 5️⃣ Usar o assistente

1. Na barra lateral, em **Carregar Novas Políticas (PDF)**, selecione o arquivo `politicas_rh.pdf` que acompanha o repositório (ou os seus próprios PDFs)
2. Clique em **📂 Processar Documentos** e aguarde a mensagem `Processado com sucesso! N fragmentos de texto adicionados à Collection.`
3. Faça uma pergunta no campo de chat
4. Abra **📚 Fontes Consultadas (Metadados)** abaixo da resposta para ver o arquivo, a página e o trecho usados

O banco vetorial fica salvo em `chroma_db_data/`. Ao fechar e abrir o app de novo, não é preciso reprocessar os documentos.

> **Atenção:** clicar em "Processar Documentos" mais de uma vez com o mesmo PDF grava os fragmentos em duplicidade. Para recarregar um documento, use antes o botão **🗑️ Limpar Banco de Dados**.

### Encerrar

`Ctrl+C` no terminal. Para apagar o banco vetorial por completo, exclua a pasta `chroma_db_data/`.

## 📚 Exemplos de Perguntas

Perguntas que o documento de exemplo `politicas_rh.pdf` responde:

- "Qual a antecedência mínima para solicitação de férias?"
- "Há necessidade de presença física em algum momento no modelo de trabalho remoto?"
- "Posso instalar softwares por conta própria no computador da empresa?"
- "Quais benefícios a empresa oferece?"
- "O que acontece se eu descumprir as normas de segurança da informação?"
- "Para quem devo reportar um caso de assédio?"

O documento de exemplo cobre: férias, benefícios, trabalho remoto, uso de equipamentos, segurança da informação e conduta e ética.

## 🔧 Componentes Principais

### 1. `dsa_rag_engine.py` — Motor de RAG

Define a classe `DSARAGEngine` e cria a instância global `rag_engine`, usada pela interface.

| Método | O que faz |
|--------|-----------|
| `__init__()` | Carrega o modelo de embeddings, o LLM da Groq e abre (ou cria) a coleção `rh_policies` no ChromaDB |
| `ingest_documents(temp_dir_path)` | Lê os PDFs da pasta, divide em chunks, gera os embeddings e grava no banco vetorial |
| `get_response(query)` | Recupera os 3 chunks mais similares e gera a resposta com o LLM, devolvendo também os documentos de origem |
| `clear_database()` | Apaga a coleção e recria uma vazia |

Configurações principais:

```python
PERSIST_DIRECTORY = "./chroma_db_data"

self.embedding_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
self.llm = ChatGroq(temperature = 0, model_name = "openai/gpt-oss-120b")
```

### 2. `dsa_app.py` — Interface Streamlit

- **Barra lateral**: upload de um ou mais PDFs, botão para processar os documentos e botão para limpar o banco vetorial
- **Área principal**: chat com histórico da sessão e painel de fontes consultadas

Os PDFs enviados são gravados em uma pasta temporária, processados e apagados em seguida; apenas os vetores e os trechos de texto ficam no ChromaDB.

```python
response_payload = rag_engine.get_response(prompt)
answer = response_payload['result']
sources = response_payload['source_documents']
```

## 🧠 Como o RAG funciona aqui

1. O PDF é carregado e dividido em chunks
2. Cada chunk é convertido em um vetor (embedding) e gravado no ChromaDB com seus metadados (arquivo e página)
3. A pergunta do usuário também é convertida em vetor
4. O ChromaDB devolve os 3 chunks mais próximos da pergunta
5. O LLM recebe a pergunta junto com esses trechos e escreve a resposta

Com isso, a resposta se apoia no conteúdo real do documento, o que reduz respostas inventadas e permite conferir a fonte.

## 📦 Dependências Principais

| Biblioteca | Versão | Uso |
|-----------|--------|-----|
| `streamlit` | 1.52.0 | Interface web |
| `langchain` | 1.0.5 | Framework de orquestração |
| `langchain-classic` | 1.0.0 | Chain `RetrievalQA` |
| `langchain-groq` | 1.0.0 | Integração com o LLM da Groq |
| `langchain-huggingface` | 1.0.1 | Modelo de embeddings |
| `langchain-chroma` | 1.0.0 | Integração com o ChromaDB |
| `chromadb` | 1.3.5 | Banco vetorial |
| `sentence-transformers` | 5.1.2 | Execução do modelo de embeddings |
| `pypdf` | 6.4.0 | Leitura de PDFs |
| `python-dotenv` | 1.2.1 | Leitura do arquivo `.env` |

Lista completa em `requirements.txt`.

## ⚙️ Personalização

### Número de chunks recuperados

Em `dsa_rag_engine.py`, método `get_response()`:

```python
search_kwargs = {"k": 3}   # aumente para 5 ou mais se quiser dar mais contexto ao LLM
```

### Tamanho dos chunks

Em `dsa_rag_engine.py`, método `ingest_documents()`:

```python
RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
```

Chunks muito pequenos perdem contexto; chunks muito grandes pioram a precisão da busca. Depois de alterar, limpe o banco e processe os documentos de novo.

### Modelo do LLM

```python
self.llm = ChatGroq(temperature = 0, model_name = "openai/gpt-oss-120b")
```

A Groq atualiza e descontinua modelos periodicamente. Consulte a lista em https://console.groq.com/docs/models e troque o `model_name` se necessário.

### Modelo de embedding

```python
self.embedding_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
```

Ao trocar o modelo, apague a pasta `chroma_db_data/` e processe os documentos novamente, pois os vetores antigos deixam de ser compatíveis.

## 🛡️ Privacidade

- ✅ **Local**: a leitura dos PDFs, a geração de embeddings e o banco vetorial ficam na sua máquina
- ⚠️ **Enviado para a Groq**: a cada pergunta, o texto da pergunta e os trechos recuperados dos documentos são enviados para a API da Groq para gerar a resposta. Não use documentos confidenciais sem avaliar isso antes
- ⚠️ Confirme informações críticas no documento original antes de usá-las em decisões administrativas
- ⚠️ Em ambiente real, recomenda-se controle de acesso e auditoria

## 🐛 Troubleshooting

### `GroqError: The api_key client option must be set...`

O app não encontrou a chave. Verifique se o arquivo `.env` está na raiz do projeto, se o nome é exatamente `.env`, se contém `GROQ_API_KEY=...` e se o comando `streamlit run` foi executado nessa mesma pasta.

No Windows, se o arquivo foi criado com `echo ... > .env` no PowerShell, ele pode ter sido salvo em uma codificação que o app não lê. Recrie o arquivo em um editor de texto.

### Erro `401` / `Invalid API Key`

A chave está incorreta ou foi revogada. Gere outra em https://console.groq.com/keys.

### Erro `404` / `model_not_found` ou `model_decommissioned`

O modelo configurado não está mais disponível na Groq. Troque o `model_name` em `dsa_rag_engine.py` por um da lista em https://console.groq.com/docs/models.

### Erro `429` / rate limit

O limite do plano gratuito da Groq foi atingido. Aguarde alguns instantes e tente de novo.

### Erro ao instalar o `numpy`

Versão do Python abaixo de 3.11. Confira com `python --version` e recrie o ambiente com Python 3.11+.

### Erro de conexão com `huggingface.co` ao iniciar

O modelo de embeddings é baixado na primeira execução. Verifique a internet (ou o proxy da rede corporativa) e inicie de novo.

### "Processado com sucesso! 0 fragmentos..." ao processar

O PDF não tem texto extraível, como em documentos escaneados (imagem). Use um PDF com texto selecionável.

### A resposta diz que não sabe ou não encontrou a informação

Confirme que clicou em "Processar Documentos" depois do upload e que a mensagem de sucesso apareceu. O assistente só responde com base nos documentos carregados.

### Respostas com fontes repetidas

O mesmo PDF foi processado mais de uma vez. Clique em "Limpar Banco de Dados" e processe novamente.

### Porta 8501 em uso

```bash
streamlit run dsa_app.py --server.port 8502
```

## 📈 Melhorias Futuras

- [ ] Evitar duplicidade ao reprocessar o mesmo documento
- [ ] Suporte a outros formatos (Word, TXT, HTML)
- [ ] Histórico de conversa considerado nas respostas (memória)
- [ ] Autenticação para uso interno
- [ ] Filtros por documento ou tema na busca
- [ ] Métricas de qualidade da recuperação
- [ ] API REST para integração com outros sistemas

## 📝 Licença

Projeto de Pós-Graduação, desenvolvido para fins de estudo e portfólio durante a Pós-Graduação em Engenharia de Dados para IA da Data Science Academy. Não possui licença de uso comercial.


## 🎓 Referências

- [LangChain Documentation](https://python.langchain.com/docs/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Groq API Docs](https://console.groq.com/docs)
- [all-MiniLM-L6-v2 (Hugging Face)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Streamlit Documentation](https://docs.streamlit.io/)

