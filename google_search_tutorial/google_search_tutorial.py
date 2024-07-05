import warnings
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_community.retrievers.web_research import WebResearchRetriever
from langchain.chains import RetrievalQAWithSourcesChain


class QuestionAnsweringSystem:
    def __init__(self):
        # Set up environment variables for API keys
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        google_api_key = os.getenv("GOOGLE_API_KEY")
        google_cse_id = os.getenv("GOOGLE_CSE_ID")

        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["USER_AGENT"] = "MyApp/1.0"

        # Initialize components
        self.chat_model = ChatOpenAI(
            model_name="gpt-3.5-turbo-16k",
            temperature=0,
            streaming=True,
            openai_api_key=openai_api_key,
        )
        self.vector_store = Chroma(
            embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_db_oai"
        )
        self.conversation_memory = ConversationSummaryBufferMemory(
            llm=self.chat_model,
            input_key="question",
            output_key="answer",
            return_messages=True,
        )

        # Set up Google Custom Search
        self.google_search = GoogleSearchAPIWrapper(
            google_api_key=google_api_key, google_cse_id=google_cse_id
        )

        self.web_research_retriever = WebResearchRetriever.from_llm(
            vectorstore=self.vector_store,
            llm=self.chat_model,
            search=self.google_search,
        )
        self.qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
            self.chat_model, retriever=self.web_research_retriever
        )

    def answer_question(self, user_input_question):
        # Query the QA chain with the user input question
        result = self.qa_chain({"question": user_input_question})

        # Return the answer and sources
        return result["answer"], result["sources"]


if __name__ == "__main__":
    qa_system = QuestionAnsweringSystem()
    user_input_question = input("Ask a question: ")
    answer, sources = qa_system.answer_question(user_input_question)
    print("Answer:", answer)
    print("Sources:", sources)
