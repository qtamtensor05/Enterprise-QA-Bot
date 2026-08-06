from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="enterprise_knowledge")

def ask_question(query, top_k=2):
    print(f"\nCâu hỏi của người dùng: '{query}'")
    
    query_vector = model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )
    
    retrieved_chunks = results['documents'][0]
    
    if not retrieved_chunks:
        return "Không tìm thấy tài liệu liên quan."
        
    context = "\n---\n".join(retrieved_chunks)
    
    prompt = f"""Bạn là trợ lý ảo nội bộ của doanh nghiệp. Hãy dựa vào [Ngữ cảnh] dưới đây để trả lời [Câu hỏi] của nhân viên.
Nếu thông tin không có trong Ngữ cảnh, hãy nói 'Tôi không có đủ thông tin để trả lời câu hỏi này', tuyệt đối không tự bịa ra dữ liệu.

[Ngữ cảnh]:
{context}

[Câu hỏi]: {query}

[Trả lời]:"""

    return prompt

if __name__ == "__main__":
    user_query = "Tôi muốn xin nghỉ phép 4 ngày để đi du lịch thì phải báo trước bao lâu?"
    
    final_prompt = ask_question(user_query)
    
    print(final_prompt)