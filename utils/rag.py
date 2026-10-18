import chromadb
from groq import Groq
from utils.embeddings import get_embedding
import streamlit as st

client_groq = Groq(api_key=st.secrets["GROQ_API_KEY"])

client = chromadb.Client()
collection = client.get_or_create_collection(name="study_collection")

def add_documents_to_db(chunks):
    embeddings = get_embedding(chunks)
    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=[str(i) for i in range(len(chunks))]
    )

def ask_question(question):
    question_embedding = get_embedding([question])
    results = collection.query(query_embeddings=question_embedding.tolist(), n_results=1)
    
    if not results['documents'] or not results['documents'][0]:
        return "عذراً، لم أجد أي ملفات في قاعدة البيانات. ارفع ملفاً أولاً."
        
    context = results['documents'][0][0]
    
    chat_completion = client_groq.chat.completions.create(
        messages=[
            {"role": "system", "content": "أنت مساعد دراسي ذكي. أجب على سؤال المستخدم بناءً على النص المرفق فقط."},
            {"role": "user", "content": f"النص:\n{context}\n\nالسؤال: {question}"}
        ],
        model="allam-2-7b",    )
    
    return chat_completion.choices[0].message.content