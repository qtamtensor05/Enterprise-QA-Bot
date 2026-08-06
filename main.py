from chunking_ingestion.loader_chunker import process_document
from embedding_vector_storage.vector_storage import store_chunks_to_db

if __name__ == "__main__":
    file_path = "./Docs/quydinh.txt" 
    
    chunks = process_document(file_path)
    
    if chunks:
        print(chunks[0])

    store_chunks_to_db(chunks=chunks)