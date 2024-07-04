from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

# Define the repository ID for the Gemma 2b model
repo_id = "google/gemma-2b-it"

# Set up a Hugging Face Endpoint for Gemma 2b model
llm = HuggingFaceEndpoint(
    repo_id=repo_id, max_length=1024, temperature=0.1
)

# initialize a Chroma db from persistence folder
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma("ipo_documents", embedding_function=embedding_function, persist_directory=persist_folder)

# Create a conversation buffer memory
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

# Define a custom template for the question prompt
custom_template = """Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question, in its original English.
                        Chat History:
                        {chat_history}
                        Follow-Up Input: {question}
                        Standalone question:"""

# Create a PromptTemplate from the custom template
CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

# Create a ConversationalRetrievalChain from an LLM with the specified components
conversational_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(),
    memory=memory,
    condense_question_prompt=CUSTOM_QUESTION_PROMPT
)

answer = conversational_chain({"question":"who is gojo?"})

print(answer)