import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os


os.environ["OPENAI_API_KEY"] = "sk-proj-Iz5AMuBVBiVxTb7SXi4EylkSj39ijkwdTZGPG1LoMJt4mKRG5jUzhYFUT4apD1r9A8GaPITUZET3BlbkFJMBmPF17L4pUwUeBldaubJqeW5d9eBvCR5ecqiJ-zbUTZOEywZMOaQiX5PeymJiREmRXqauo"  # <-- PASTE KEY HERE

# MODERN LANGCHAIN IMPORTS
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS 
from langchain_community.callbacks.manager import get_openai_callback


# ASSIGNMENT 1: The "Messy Data" Cleaner

def run_assignment_1():
    print("\n--- Running Assignment 1 ---")
    template = """Analyze the following customer product review.
Extract the core information and output it in this exact format:
Sentiment: [Positive/Negative], Core Issue: [Brief summary of the problem]

Review: {messy_review}"""

    prompt = PromptTemplate.from_template(template)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | llm | StrOutputParser()

    messy_review_input = "I bought this blender yesterday and it's absolutely terrible! The lid flew off while I was making a smoothie and my whole kitchen is covered in spinach. I want a refund!"
    print(chain.invoke({"messy_review": messy_review_input}))


# ASSIGNMENT 2: The Marketing Assembly Line

def run_assignment_2():
    print("\n--- Running Assignment 2 ---")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    chain_slogan = ChatPromptTemplate.from_template("Generate a catchy, exactly 5-word English slogan for the product: {product_name}.") | llm | StrOutputParser()
    chain_translation = ChatPromptTemplate.from_template("Translate this English marketing slogan into French: {slogan}") | llm | StrOutputParser()
    combined_chain = {"slogan": chain_slogan} | chain_translation

    print(f"Final French Slogan: {combined_chain.invoke({'product_name': 'Eco-Friendly Wireless Earbuds'})}")


# ASSIGNMENT 3: Mini-RAG

def run_assignment_3():
    print("\n--- Running Assignment 3 ---")
    rules_content = (
        "The golden token is worth 50 points.\n"
        "Players cannot cross the river without a bridge card.\n"
        "If a player rolls a double six, they must draw a chaos card.\n"
        "The game immediately ends when the dragon tile is revealed."
    )
    documents = [Document(page_content=rules_content)]
    
    text_splitter = CharacterTextSplitter(chunk_size=150, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    
    prompt = ChatPromptTemplate.from_template("Answer the question based only on context:\n{context}\nQuestion: {question}")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    rag_chain = (
        {"context": lambda x: retriever.invoke(x["question"])[0].page_content, "question": lambda x: x["question"]}
        | prompt | llm | StrOutputParser()
    )

    query = "How many points is the golden token worth?"
    print(f"Answer: {rag_chain.invoke({'question': query})}")


# ASSIGNMENT 4: The Watchful Eye

def run_assignment_4():
    print("\n--- Running Assignment 4 ---")
    template = "Analyze review and output format:\nSentiment: [Positive/Negative], Core Issue: [Summary]\nReview: {messy_review}"
    chain = PromptTemplate.from_template(template) | ChatOpenAI(model="gpt-4o-mini", temperature=0) | StrOutputParser()

    messy_review_input = "I bought this blender yesterday and it's absolutely terrible! The lid flew off while I was making a smoothie and my whole kitchen is covered in spinach. I want a refund!"

    with get_openai_callback() as cb:
        result = chain.invoke({"messy_review": messy_review_input})
        print(f"Result: {result}\n")
        print("================ RECEIPT ================")
        print(f"Total Tokens Used:      {cb.total_tokens}")
        print(f"Prompt Tokens Used:     {cb.prompt_tokens}")
        print(f"Completion Tokens Used: {cb.completion_tokens}")
        print(f"Total Cost (USD):       ${cb.total_cost:.6f}")
        print("=========================================")

if __name__ == "__main__":
    if os.environ["OPENAI_API_KEY"] == "sk-proj-Iz5AMuBVBiVxTb7SXi4EylkSj39ijkwdTZGPG1LoMJt4mKRG5jUzhYFUT4apD1r9A8GaPITUZET3BlbkFJMBmPF17L4pUwUeBldaubJqeW5d9eBvCR5ecqiJ":
        print("[ERROR] Please paste your real OpenAI API key on line 7 before running.")
    else:
        run_assignment_1()
        run_assignment_2()
        run_assignment_3()
        run_assignment_4()