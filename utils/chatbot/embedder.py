import os
import tempfile
from langchain.document_loaders import CSVLoader, PyPDFLoader, TextLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


class Embedder:

    def __init__(self):
        self.PATH = "embeddings"
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)

    def storeDocEmbeds(self, file, original_filename):
        """
        Stores document embeddings using Langchain and Chroma DB
        """
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
            tmp_file.write(file)
            tmp_file_path = tmp_file.name

        def get_file_extension(uploaded_file):
            file_extension = os.path.splitext(uploaded_file)[1].lower()
            return file_extension

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100,
            length_function=len,
        )

        file_extension = get_file_extension(original_filename)

        if file_extension == ".csv":
            loader = CSVLoader(
                file_path=tmp_file_path, encoding="utf-8", csv_args={"delimiter": ","}
            )
            data = loader.load()

        elif file_extension == ".pdf":
            loader = PyPDFLoader(file_path=tmp_file_path)
            data = loader.load_and_split(text_splitter)

        elif file_extension == ".txt":
            loader = TextLoader(file_path=tmp_file_path, encoding="utf-8")
            data = loader.load_and_split(text_splitter)
        user_api_key = os.getenv("OPENAI_API_KEY")
        print("apikey", user_api_key)
        embeddings = OpenAIEmbeddings(openai_api_key=user_api_key)

        # Initialize Chroma DB
        chroma = Chroma(
            persist_directory=f"{self.PATH}/{original_filename}",
            embedding_function=embeddings,
        )
        vectors = chroma.add_documents(data)

        # Remove the temporary file
        os.remove(tmp_file_path)

    def getDocEmbeds(self, file, original_filename):
        """
        Retrieves document embeddings from Chroma DB
        """
        if not os.path.exists(f"{self.PATH}/{original_filename}"):
            self.storeDocEmbeds(file, original_filename)
        user_api_key = os.getenv("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings(openai_api_key=user_api_key)
        # Load the vectors from Chroma DB
        vectors = Chroma(
            embedding_function=embeddings,
            persist_directory=f"{self.PATH}/{original_filename}",
        )

        return vectors
