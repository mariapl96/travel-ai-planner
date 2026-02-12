"""
Sistema RAG (Retrieval Augmented Generation)
Gestiona la base de conocimiento y búsqueda de información relevante en los documentos
Recupera la información de mis documentos y se la da al LLM para que genere una respuesta con esa información
"""

import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from config import RAG_CONFIG, EMBEDDING_CONFIG


class RAGSystem:
    """
    Sistema RAG para recuperar información relevante de la base de conocimiento
    """
    
    def __init__(self):
        """
        Inicializa el sistema RAG
        """
        self.knowledge_base_path = RAG_CONFIG["knowledge_base_path"]
        self.chunk_size = RAG_CONFIG["chunk_size"]
        self.chunk_overlap = RAG_CONFIG["chunk_overlap"]
        self.top_k = RAG_CONFIG["top_k"]
        
        # Inicializar modelo de embeddings
        print("Cargando modelo de embeddings...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_CONFIG["model_name"],
            model_kwargs={'device': EMBEDDING_CONFIG["device"]}
        )
        
        # Cargar o crear vector store
        self.vector_store = None
        self._load_or_create_vector_store()
        
        print("✅Sistema RAG inicializado correctamente")
    
    
    def _load_documents(self) -> List[Document]:
        """
        Carga todos los documentos de la base de conocimiento.
        Se usa dentro de _load_or_create_vector_store(), que es otro método de la clase Rag.
        
        Returns:
            List[Document]: Lista de documentos cargados
        """
        documents = []
        
        # Verificar que existe la carpeta
        if not os.path.exists(self.knowledge_base_path):
            raise FileNotFoundError(f"No se encuentra la carpeta: {self.knowledge_base_path}")
        
        # Leer todos los archivos .txt de la carpeta
        for filename in os.listdir(self.knowledge_base_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.knowledge_base_path, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        
                        # Crear documento con metadata
                        doc = Document(
                            page_content=content,
                            metadata={
                                "source": filename,
                                "destination": filename.replace('.txt', '').title()
                            }
                        )
                        documents.append(doc)
                        print(f"  ✓ Cargado: {filename}")
                        
                except Exception as e:
                    print(f"  ✗ Error cargando {filename}: {e}")
        
        print(f"Total documentos cargados: {len(documents)}")
        return documents
    
    
    def _split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Divide documentos en fragmentos más pequeños (chunks)
        Se usa dentro de _load_or_create_vector_store(), que es otro método de la clase Rag.

        Args:
            documents: Lista de documentos
            
        Returns:
            List[Document]: Documentos divididos en chunks
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"Documentos divididos en {len(chunks)} fragmentos")
        
        return chunks
    
    
    def _create_vector_store(self, chunks: List[Document]):
        """
        Crea el vector store (base de datos vectorial) a partir de los chunks
        Convierte los chunks en embeddings y los guarda en FAISS.

        1. Coge cada chunk de texto
        2. Lo convierte en un vector (embedding) usando self.embeddings
        3. Guarda el vector + texto original en la base de datos

        Se usa dentro de _load_or_create_vector_store().

        Args:
            chunks: Lista de fragmentos de documentos
        """
        print("Creando vector store (puede tardar un poco)...")
        
        self.vector_store = FAISS.from_documents( # FAISS es una libreria de Facebook que guarda vectores
            documents=chunks,
            embedding=self.embeddings
        )
        
        print("✅Vector store creado correctamente")
    
    
    def _load_or_create_vector_store(self):
        """
        Carga vector store existente o crea uno nuevo

        Se ejecuta dentro de __init__.
        """
        vector_store_path = "data/faiss_index"
        
        # Intentar cargar vector store existente
        if os.path.exists(vector_store_path):
            try:
                print("Cargando vector store existente...")
                self.vector_store = FAISS.load_local(
                    vector_store_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print("✅Vector store cargado desde disco")
                return
            except Exception as e:
                print(f"⚠️Error cargando vector store: {e}")
                print("Creando nuevo vector store...")
        
        # Si no existe o falla la carga, crear nuevo
        documents = self._load_documents()
        
        if not documents:
            raise ValueError("No se encontraron documentos en la base de conocimiento")
        
        chunks = self._split_documents(documents)
        self._create_vector_store(chunks)
        
        # Guardar vector store para futuras ejecuciones
        try:
            os.makedirs("data", exist_ok=True)
            self.vector_store.save_local(vector_store_path)
            print("Vector store guardado en disco")
        except Exception as e:
            print(f"⚠️No se pudo guardar vector store: {e}")
    
    
    def search(self, query: str, k: int = None) -> str:
        """
        Busca información relevante en la base de conocimiento
        Se usa en app.py
        
        Args:
            query: Consulta de búsqueda
            k: Número de resultados a devolver (usa self.top_k por defecto)
            
        Returns:
            str: Información relevante formateada
        """
        if not self.vector_store:
            return "⚠️Sistema RAG no inicializado correctamente"
        
        k = k or self.top_k
        
        try:
            # Búsqueda de similitud
            results = self.vector_store.similarity_search(query, k=k)
            
            if not results:
                return "No se encontró información relevante en la base de conocimiento."
            
            # Formatear resultados
            context = "**Información relevante de la base de conocimiento:**\n\n"
            
            for i, doc in enumerate(results, 1):
                destination = doc.metadata.get("destination", "Desconocido")
                content = doc.page_content.strip()
                
                context += f"**[Fuente: {destination}]**\n{content}\n\n"
                
                # Separador entre fragmentos
                if i < len(results):
                    context += "---\n\n"
            
            return context
            
        except Exception as e:
            return f"⚠️Error en búsqueda RAG: {str(e)}"
    
    
    def search_by_destination(self, destination: str) -> str:
        """
        Busca información específica de un destino
        
        Args:
            destination: Nombre del destino
            
        Returns:
            str: Información del destino
        """
        query = f"información completa sobre {destination} atracciones gastronomía transporte presupuesto"
        return self.search(query, k=5)
    
    
    def get_destination_summary(self, destination: str) -> str:
        """
        Obtiene un resumen del destino
        
        Args:
            destination: Nombre del destino
            
        Returns:
            str: Resumen del destino
        """
        # Buscar archivo específico del destino
        filename = f"{destination.lower()}.txt"
        filepath = os.path.join(self.knowledge_base_path, filename)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Devolver primeros 1000 caracteres como resumen
                    return content[:1000] + "..." if len(content) > 1000 else content
            except Exception as e:
                return f"Error leyendo información de {destination}: {e}"
        else:
            # Si no existe archivo específico, usar búsqueda semántica
            return self.search_by_destination(destination)


# Función auxiliar para testing
if __name__ == "__main__":
    print("Testing RAG System...\n")
    
    # Inicializar sistema
    rag = RAGSystem()
    
    # Test 1: Búsqueda general
    print("\n" + "="*50)
    print("TEST 1: Búsqueda general sobre París")
    print("="*50)
    results = rag.search("mejores restaurantes y comida en París")
    print(results)
    
    # Test 2: Búsqueda por destino
    print("\n" + "="*50)
    print("TEST 2: Información completa de Barcelona")
    print("="*50)
    results = rag.search_by_destination("Barcelona")
    print(results)
    
    print("\n✅Tests completados")