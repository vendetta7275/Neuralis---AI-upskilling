from langchain_text_splitters import RecursiveCharacterTextSplitter

# I. Dense Input Text Document
document = (
    "Artificial Intelligence has rapidly progressed from rule-based automation systems to complex, deep learning frameworks. "
    "Large Language Models are trained on massive datasets containing terabytes of text to discover complex structural patterns. "
    "Retrieval-Augmented Generation bridges the operational gap between static model weights and dynamic, real-time external knowledge databases. "
    "Chunking acts as the foundation of any robust vector architecture by splitting vast corpora into distinct, semantically rich semantic snippets."
)

# II. Parameterized Splitter Configuration
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
    length_function=len
)

chunks = splitter.split_text(document)

# III. Custom Validation Function to Programmatically Prove Overlap
def find_exact_overlap(chunk1: str, chunk2: str) -> str:
    max_overlap = min(len(chunk1), len(chunk2))
    # Scan backward from max length to find where chunk1 ends and chunk2 begins
    for i in range(max_overlap, 0, -1):
        if chunk1.endswith(chunk2[:i]):
            return chunk2[:i]
    return ""

# IV. Print Execution Results
print("--- Smart Splitter Verification ---")
for idx in range(len(chunks) - 1):
    c1 = chunks[idx]
    c2 = chunks[idx+1]
    overlap_text = find_exact_overlap(c1, c2)
    
    print(f"\n[Pair {idx+1}]")
    print(f"● Chunk {idx+1}: \"{c1}\" (Length: {len(c1)})")
    print(f"● Chunk {idx+2}: \"{c2}\" (Length: {len(c2)})")
    print(f"● Extracted Overlap: \"{overlap_text}\" (Length: {len(overlap_text)})")