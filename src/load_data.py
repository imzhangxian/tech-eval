from langchain_community.document_loaders.llmsherpa import LLMSherpaFileLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings
    )
from langchain_community.vectorstores  import Chroma
from langchain_text_splitters import CharacterTextSplitter
# from llmsherpa.readers import LayoutPDFReader, Section
# import json

LLM_SHERPA_URL = "http://localhost:5010/api/parseDocument?renderFormat=all"
pdf_filename = "/home/xian/Workspace/tech-transfer/data/shar/688001.SH_华兴源创-20190703.pdf"

def llmsherpa_load(llmsherpa_api_url, pdf_url):
    loader = LLMSherpaFileLoader(
        file_path=pdf_url, 
        new_indent_parser=True, 
        apply_ocr=True, 
        strategy="chunks", 
        llmsherpa_api_url=llmsherpa_api_url
        )
    docs = loader.load()
    return docs

def docToJson(doc):
    sections = doc.sections()
    with open("output.txt", "w")  as f:
        for i, sec in enumerate(sections):
            f.write(f'section {i}: {sec.title}')
            f.write('\n')
            paragraphs = sec.paragraphs()
            for j, para in enumerate(paragraphs):
                f.write(f'    paragraph {j}')
                f.write('\n')
            # json.dump(sec.block_json, f)

docs = llmsherpa_load(LLM_SHERPA_URL, pdf_filename)
print(len(docs))

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(docs, embedding_function)
