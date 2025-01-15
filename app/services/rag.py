from dotenv import load_dotenv
import os 
import time
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredCSVLoader, UnstructuredExcelLoader, UnstructuredPowerPointLoader
from langchain.chains import RetrievalQA
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.llms import DeepInfra
from langchain_community.embeddings import DeepInfraEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate, BaseChatPromptTemplate

load_dotenv()

template = """Try to answer the following question by carefully checking the context. Always say "thanks for asking! " at the end of the answer. If you dont know the answer, say "I dont know".

context:
{context}

Question:
{question}
"""


class RAG: 
    def __init__(self):
        self.DIRECTORY_PATH = os.getenv("UPLOAD_PATH")
        self.DEEP_INFRA_KEY = os.getenv("DEEP_INFRA_KEY")

        # langchain config
        self.llm = os.getenv("LLM")
        self.embedding_model_id= os.getenv("EMBEDDING_MODEL_ID")
        self.temperature = os.getenv("TEMPERATURE")
        self.repetition_penalty= os.getenv("REPETITION_PANALTY")
        self.max_new_tokens= os.getenv("MAX_NEW_TOKENS")
        self.top_p= os.getenv("TOP_P")


        os.environ["DEEPINFRA_API_TOKEN"] = self.DEEP_INFRA_KEY

     
        
    
    def load_file(self, file_name):

        file_extension = file_name.split(".")[-1].lower()

        if not file_extension:
            raise ValueError("Unsupported file type. Only PDF, DOC, DOCX, TXT, XLSX, PPTX and CSV files are allowed.")


        # Load the file in Langchain according to the file type

        file_path = os.path.join(self.DIRECTORY_PATH, file_name)

        if file_extension == "pdf":
            loader =  PyPDFLoader(file_path)
        elif file_extension == "doc" or file_extension == "docx":
            loader =  Docx2txtLoader(file_path)
        elif file_extension == "txt":
            loader =  TextLoader(file_path)
        elif file_extension == "xlsx":
            loader = UnstructuredExcelLoader(file_path) 
        elif file_extension == "pptx":
            loader =  UnstructuredPowerPointLoader(file_path)
        elif file_extension == "csv":
            loader = UnstructuredCSVLoader(file_path)
        else:
            raise ValueError("Unsupported file type. Only PDF, DOC, DOCX, TXT, XLSX, PPTX and CSV files are allowed.")

        return loader

    def process_file(self, file_name, session_data):

        # Load the file in Langchain according to the file type
        loader = self.load_file(file_name)

        # Process the file
        raw_documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0)
        documents = text_splitter.split_documents(raw_documents)

        # embedding the documents
        embeddings = DeepInfraEmbeddings(
            model_id=self.embedding_model_id,
            query_instruction="",
            embed_instruction="",
        )

        # create the vector store
        db = Chroma.from_documents(documents, embeddings)

        # create the retriever
        retriever = db.as_retriever(search_kwargs={"k": 4})

        # create the llm
        llm = DeepInfra(model_id=self.llm)

        llm.model_kwargs = {
            "temperature": self.temperature,
            "repetition_penalty": self.repetition_penalty,
            "max_new_tokens": self.max_new_tokens,
            "top_p": self.top_p,
        }

        # create the chain
        self.qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,  
            verbose=True,
            chain_type_kwargs={
                "verbose": True,
                "prompt": PromptTemplate(
                    template=template,
                    input_variables=["context", "question"],
                )
            }
        )
    
    def answer_question(self, question):
        return self.qa({"query": question,type: "question"})


        
        


