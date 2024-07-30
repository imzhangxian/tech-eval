from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

test_folder = "/home/xian/Workspace/tech-eval/data/load-test/"
db_persist = "/home/xian/Workspace/tech-eval/storage/test/"

loader = PyPDFDirectoryLoader(test_folder)
data = loader.load()
chunks_number = len(data)
print(f'{chunks_number} chunks loaded.')

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma('ipo-documents', embedding_function=embedding_function, persist_directory=db_persist)

for p in range(chunks_number):
    stock_code = 688001 if 'hxyc' in data[p].metadata['source'] else 688002
    stock_name = 'hxyc' if 'hxyc' in data[p].metadata['source'] else 'tzkj'
    data[p].metadata['stock_code'] = stock_code
    data[p].metadata['stock_name'] = stock_name

db.add_documents(data)

search_kwargs =  {"k": 4, "filter": {"stock_code": 688001}}

# k is the number of chunks to retrieve
retriever = db.as_retriever(search_kwargs=search_kwargs)

docs = retriever.invoke("688001 股权占比")

print(docs)