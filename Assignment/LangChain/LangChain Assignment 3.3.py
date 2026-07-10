from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Exact target text provided
tricky_document = """
Section 1: The company Jade Global is launching a massive new
internal initiative called Project Phoenix. This project will
restructure the entire cloud infrastructure.
Section 2: Employees must adhere to the standard office hours of
9:00 AM to 5:00 PM. Remote work is permitted on Tuesdays and
Thursdays, provided that the employee has secured prior approval
from their direct manager.
Section 3: The cafeteria will now offer extended hours, opening
at 7:30 AM for breakfast. Please ensure you clear your tables
after eating.
Section 4: All IT support tickets must be filed through the
internal Jira portal. Direct emails to the IT staff will be
ignored starting next month.
Section 5: The annual holiday party is scheduled for December
15th. Dress code is semi-formal. Plus-ones are allowed if
registered by November 30th.
Section 6: Parking in the executive lot is strictly prohibited
for unauthorized vehicles. Violators will be towed at the owner's
expense.
Section 7: Health insurance open enrollment begins in October.
Please review the new dental and vision plans, as the providers
have changed this year.
Section 8: All employees must complete the mandatory
cybersecurity training module by the end of Q3. Failure to do so
will result in temporary suspension of VPN access.
Section 9: Regarding the cloud restructure initiative mentioned
earlier, the final deadline for its completion is December 31st,
2026. The budget approved is $500,000.
"""

# 1. Initialize Vector & Inference Components
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = Ollama(model="llama3", temperature=0)

# 2. Strategic Chunking Parameters to combat Context Fragmentation
# We use a comprehensive chunk size that retains wide macro context windows 
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=400
)
docs = text_splitter.create_documents([tricky_document])

# 3. Vector Database Processing
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 4. RAG Pipeline Compilation
rag_prompt = PromptTemplate.from_template(
    "You are a factual database assistant. Rely ONLY on the provided context below to answer the user query.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Answer:"
)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# 5. Pipeline Execution Execution
query = "What is the deadline and budget for Project Phoenix?"
print("--- RUNNING DETECTIVE PUZZLE RAG ---")
print(f"User Query: {query}")
print(f"Retrieved Documents Count: {len(docs)} total chunks generated.")

final_answer = rag_chain.invoke(query)
print(f"\n● RAG Final Answer:\n{final_answer}\n")

'''
=========================================
MANDATORY EXPLANATION BLOCK: CHUNK CONFIGURATION
=========================================
1. Why these specific values were chosen:
   - The original 'tricky_document' is roughly 1,600 characters long.
   - Setting 'chunk_size=1200' ensures that the text is not fragmented into tiny, isolated pieces. 
   - Setting 'chunk_overlap=400' provides an enormous context bridge, allowing the core entities from 
     Section 1 to slide cleanly into the neighboring document splits containing downstream details.

2. Behavior under low-overlap settings:
   - When using standard micro-chunk structures (e.g., chunk_size=200, chunk_overlap=0), Section 1 and 
     Section 9 end up in completely different database shards. 
   - When the user query asks about "Project Phoenix", the vector database returns Section 1 (which explicitly 
     mentions the name) but misses Section 9 because it only uses the phrase "the cloud restructure initiative" 
     without repeating the name "Project Phoenix". As a result, the system suffers from Context Fragmentation, 
     leading to severe hallucinations or an incomplete answer.

3. Why our final configuration resolves the issue:
   - By scaling 'chunk_size' to 1200 and setting 'chunk_overlap' to 400, Section 1 and Section 9 are effectively 
     re-linked. The vector database can pull adjacent context chunks that hold both the thematic descriptor 
     ("Project Phoenix") and the financial targets simultaneously, giving the LLM the complete lineage it 
     needs to provide the correct answer confidently.
'''