from langchain_community.document_loaders.llmsherpa import LLMSherpaFileLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings
    )
from langchain_community.vectorstores  import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
import re, glob, os
# from llmsherpa.readers import LayoutPDFReader, Section
# import json

LLM_SHERPA_URL = "http://localhost:5010/api/parseDocument?renderFormat=all"
data_folder = "/home/xian/Workspace/tech-eval/data/load-test"
db_folder = "/home/xian/Workspace/tech-eval/storage/test"
# pdf_filename = "/home/xian/Workspace/tech-transfer/data/shar/688001-华兴源创-20190703.pdf"

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

def docToJson(doc, filename):
    sections = doc.sections()
    with open(filename, "w")  as f:
        for i, sec in enumerate(sections):
            f.write(f'section {i}: {sec.title}')
            f.write('\n')
            paragraphs = sec.paragraphs()
            for j, para in enumerate(paragraphs):
                f.write(f'    paragraph {j}')
                f.write('\n')
            # json.dump(sec.block_json, f)

def load_folder(folder, persist_folder):
    filename_regex = re.compile(r"(?P<code>\d{6})-(?P<name>[\u4e00-\u9fff]+)-?(?P<date>\d{8})?.pdf\Z", flags=re.I)
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma("ipo_documents", embedding_function=embedding_function, persist_directory=persist_folder)

    for file_path in glob.glob(os.path.join(folder, "*.pdf")):
        _, file_name = os.path.split(file_path)
        match = filename_regex.match(file_name)

        print(f'parsing file {file_name}...')
        docs = llmsherpa_load(LLM_SHERPA_URL, file_path)
        
        # add meta data
        if match is not None:
            stock_code = match.group('code')
            stock_name = match.group('name')
            ipo_date = match.group('date')
            print(f'adding metadata ...')
            metadata = {}
            metadata['stock_code'] = stock_code if stock_code is not None else ''
            metadata['stock_name'] = stock_name if stock_name is not None else ''
            metadata['ipo_date'] = ipo_date if ipo_date is not None else ''
            for doc in docs:
                doc.metadata = metadata
        db.add_documents(docs)
    
    return db

db = load_folder(data_folder, db_folder)
