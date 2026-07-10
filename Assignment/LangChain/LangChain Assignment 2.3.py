from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# 1. Initialize Components (Using a dedicated embedding model)
embeddings = OllamaEmbeddings(model="nomic-embed-text") 
llm = Ollama(model="llama3", temperature=0)

# 2. Ingest contradictory fake text documents with metadata
documents = [
    Document(
        page_content="Company WFH Policy: Work from home is strictly banned.", 
        metadata={"year": 2022}
    ),
    Document(
        page_content="Company WFH Policy: Work from home is allowed 3 days a week.", 
        metadata={"year": 2024}
    )
]

# This line will now execute smoothly without the endpoint error
vector_store = FAISS.from_documents(documents, embeddings)

# 3. Custom Structured Retrieval Function with Metadata Filter
def custom_retriever_query(user_query: str, filter_year: int):
    # Enforce metadata restriction within FAISS
    search_results = vector_store.similarity_search(
        user_query, 
        k=1, 
        filter={"year": filter_year}
    )
    
    retrieved_context = search_results[0].page_content if search_results else "No context found."
    
    # LLM Security Execution Layer
    prompt_template = PromptTemplate.from_template(
        "Context: {context}\nQuestion: {question}\nAnswer the question strictly based on the context provided above."
    )
    chain = prompt_template | llm
    answer = chain.invoke({"context": retrieved_context, "question": user_query})
    
    # IV. Output Requirements Print out
    print(f"● User Query: \"{user_query}\"")
    print(f"● Active Filter: Year: {filter_year}")
    print(f"● Retrieved Context: \"{retrieved_context}\"")
    print(f"● LLM Final Answer: {answer.strip()}")

# Test the system
custom_retriever_query(user_query="What is the WFH policy?", filter_year=2024)