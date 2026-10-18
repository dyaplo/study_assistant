from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

print("جاري تحميل موديل الـ Embeddings...")
SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
print("تم تحميل موديل الـ Embeddings بنجاح!")

print("جاري تحميل موديل الإجابة...")
model_name = "deepset/xlm-roberta-base-squad2"
AutoTokenizer.from_pretrained(model_name)
AutoModelForQuestionAnswering.from_pretrained(model_name)
print("تم تحميل موديل الإجابة بنجاح!")