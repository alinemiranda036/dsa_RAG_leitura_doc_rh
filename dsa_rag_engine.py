# Projeto 1 - Assistente Corporativo de Perguntas e Respostas com RAG Sobre Documentos Internos
# Módulo de RAG

# Imports
import os # importado para interação com o sistema operacional (ex: manipulação de arquivos)
from dotenv import load_dotenv # importado para carregar variáveis de ambiente de um arquivo .env
from langchain_groq import ChatGroq #importado para utilizar o modelo de linguagem Groq (LLM)
from langchain_huggingface import HuggingFaceEmbeddings # importado para gerar embeddings de texto usando modelos da HuggingFace
from langchain_chroma import Chroma #importado para criar e gerenciar um banco de dados vetorial usando Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader #importado para carregar documentos PDF de um diretório
from langchain_text_splitters import RecursiveCharacterTextSplitter #importado para dividir textos em fragmentos menores (chunks) de forma recursiva, respeitando limites de tamanho e sobreposição
from langchain_classic.chains import RetrievalQA #importado para criar uma cadeia de perguntas e respostas que utiliza recuperação de informações (RAG)

# Carrega variáveis de ambiente
load_dotenv()

# Configurações de Caminhos para Persistência
# Aqui aplicamos o conceito de PERSISTÊNCIA: os dados não somem quando a app fecha. (caso não haja mudança na base de dados já carregada - documento da empresa de referência não alterado - 
# seguimos com a persistência para leitura do banco de dados já criado com o  primeiro arquivo carregado 
# não sendo necessário processar e gerar o banco de dados novamente)
PERSIST_DIRECTORY = "./chroma_db_data"

# Classe do módulo de RAG
class DSARAGEngine:
    
    def __init__(self):
        
        # 1. Inicializa o Modelo de Embeddings
        # Responsável por transformar texto em vetores numéricos (Embeddings)
        self.embedding_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
        
        # 2. Inicializa o LLM (Groq)
        self.llm = ChatGroq(temperature = 0, model_name = "openai/gpt-oss-120b")
        
        # 3. Inicializa/Carrega o Banco de Dados Vetorial
        # Se a pasta existir, ele carrega os dados persistidos.
        self.vector_store = Chroma(
            persist_directory = PERSIST_DIRECTORY,
            embedding_function = self.embedding_model,
            collection_name = "rh_policies" 
        )

    def ingest_documents(self, temp_dir_path):
        """
        Lê PDFs, cria chunks, gera embeddings e salva no banco vetorial.
        """
        
        # Carregamento 
        loader = PyPDFDirectoryLoader(temp_dir_path)
        documents = loader.load()
        
        if not documents:
            return "Nenhum documento encontrado."

        # Divisão em Chunks (Para caber no contexto e melhorar a busca)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200
        )
        
        chunks = text_splitter.split_documents(documents)

        # Inserção no Banco Vetorial 
        # O Chroma gera os Embeddings e salva os Metadados (origem, página)
        self.vector_store.add_documents(documents = chunks)
        
        return f"Processado com sucesso! {len(chunks)} fragmentos de texto adicionados à Collection."

    def get_response(self, query):
        """
        Executa a busca semântica e gera a resposta.
        """
        
        # Cria a Chain de QA (Retrieval Augmented Generation)
        qa_chain = RetrievalQA.from_chain_type(
            llm = self.llm,
            chain_type = "stuff",
            retriever = self.vector_store.as_retriever(
                search_kwargs = {"k": 3} # Retorna os 3 chunks mais similares
            ),
            return_source_documents = True # Para mostrar Metadados
        )

        # Executa a query
        response = qa_chain.invoke({"query": query})

        return response
    
    def clear_database(self):
        """
        Deleta a coleção para reiniciar 
        """
        self.vector_store.delete_collection()
        
        # Recria a instância vazia
        self.vector_store = Chroma(
            persist_directory = PERSIST_DIRECTORY,
            embedding_function = self.embedding_model,
            collection_name = "rh_policies"
        )
        return "Banco de dados limpo com sucesso."

# Instância global para ser usada na App
rag_engine = DSARAGEngine()


