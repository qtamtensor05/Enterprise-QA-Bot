import os
import re
import PyPDF2
import docx
from langchain_text_splitters import RecursiveCharacterTextSplitter

#Trich van ban
def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    text = ""

    try:
        if ext == '.txt':
            with open (file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        elif ext == '.pdf':
            with open(file_path,'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + " "
        elif ext == '.docx':
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + " "
        else:
            raise ValueError("Loi dinh dang")
    except:
        print("Loi doc file")
    return text

#Lam sach text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

#chunking
def create_chunks(text, chunk_size=400, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks

def process_document(file_path):
    raw_text = extract_text(file_path)
    if not raw_text:
        return []
        
    cleaned_text = clean_text(raw_text)
    chunks = create_chunks(cleaned_text)
    return chunks

if __name__ == "__main__":
    file_path = "./Docs/E-14533.pdf" 
    
    chunks = process_document(file_path)
    
    if chunks:
        print(chunks[0])
