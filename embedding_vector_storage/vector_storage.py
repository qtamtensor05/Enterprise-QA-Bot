from sentence_transformers import SentenceTransformer
import chromadb
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="enterprise_knowledge")

def store_chunks_to_db(chunks, source_file = ""):
    if not chunks:
        print("khong co chunks!")
        return
    ids = [f"{source_file}_chunks_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source_file, "chunk_id": i} for i in range(len(chunks))]

    embeddings = model.encode(chunks).tolist()

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
