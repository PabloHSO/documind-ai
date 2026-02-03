# Orquestra a pipeline de documentos
# Recebe documento seguindo fluxo abaixo.
# Conecta: Parser -> Chunker -> embeddings -> vectorstore -> agentes

from fastapi import APIRouter, UploadFile, File, HTTPExcepiton
from typing import Dict

from app.document_pipeline.parser import DocumentParser
from app.document_pipeline.chunker import TextChunker
from app.document_pipeline.embeddings import EmbeddingsGenerator
from app.document_pipeline.parser import DocumentParser
from app.vectorstore.store import VectorStore

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("upload", response_model=Dict[str, str])
async def upload_document(file: UploadFile = File(...)):
    """
    Upload e processamento de documentos corporativos.
    Pipeline:
    - Parse
    - Chunk
    - Embeddings
    - Persistência no VectorStore
    """

    if not file.filename:
        raise HTTPExcepiton(status_code=400, detail="Arquivo Inválido")
    
    try:
        # 1. Ler conteúdo do arquivo
        content = await file.read()

        # 2. Parse do documento
        parser = DocumentParser()
        text = parser.parse(file_bytes=content, filename=file.filename)

        # 3. Chuking
        chunker = TextChunker()
        chunks = chunker.split(text)

        if not chunks:
            raise HTTPExcepiton(
                status_code=400,
                detail = "Não foi possível gerar chunks a partir do documento"
            )
        
        # 4. Embeddings
        embedder = EmbeddingsGenerator()
        embeddings = embedder.embed(chunks)

        # 5. Vector Store
        store = VectorStore()
        store.add_documents(
            text= chunks,
            embeddings = embeddings,
            metadata= {"filename": file.filename}
        )

        return {
            "status": "success",
            "filename": file.filename,
            "chunks_created": str(len(chunks))
        }
    
    except Exception as e:
        raise HTTPExcepiton(
            status_code = 500,
            detail = f"Erro ao processar documento: {str(e)}"
        )
