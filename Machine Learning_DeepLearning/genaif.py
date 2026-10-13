next_token_options = {
    "The capital of France is": ["Paris", "London", "Berlin"],
    "Python is a popular": ["programming", "cooking", "sleeping"]
}

def predict_next_token(prompt):
    options = next_token_options.get(prompt)

    if options is None:
        return "No example available"

    return options[0]


print(predict_next_token("The capital of France is"))
print(predict_next_token("Python is a popular"))












import numpy as np

def cosine_similarity(vector_a, vector_b):
    """Compute cosine similarity between two vectors."""
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)

    return dot_product / (magnitude_a * magnitude_b)


embedding_cat = np.array([0.9, 0.1, 0.2])
embedding_kitten = np.array([0.85, 0.15, 0.25])
embedding_spreadsheet = np.array([0.05, 0.9, 0.6])

similarity_cat_kitten = cosine_similarity(
    embedding_cat, embedding_kitten
)

similarity_cat_spreadsheet = cosine_similarity(
    embedding_cat, embedding_spreadsheet
)

print("Cat vs kitten:", round(similarity_cat_kitten, 3))
print("Cat vs spreadsheet:", round(similarity_cat_spreadsheet, 3))





import numpy as np

def cosine_similarity(vector_a, vector_b):
    denominator = (
        np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0.0

    return float(np.dot(vector_a, vector_b) / denominator)


documents = [
    {
        "text": "Train the neural network using gradient descent.",
        "embedding": np.array([0.9, 0.2, 0.1])
    },
    {
        "text": "Use validation data to evaluate model performance.",
        "embedding": np.array([0.8, 0.3, 0.2])
    },
    {
        "text": "Tokyo is the capital of Japan.",
        "embedding": np.array([0.1, 0.1, 0.95])
    }
]

query_embedding = np.array([0.85, 0.25, 0.15])

results = []

for document in documents:
    score = cosine_similarity(
        query_embedding,
        document["embedding"]
    )

    results.append((score, document["text"]))

results.sort(reverse=True)

for score, text in results:
    print(f"{score:.3f} | {text}")
    
    
    
    
    
    
    







# ---------------------------------
# PART A: BUILD THE KNOWLEDGE BASE
# ---------------------------------

documents = load_documents("knowledge_base/")

chunks = split_documents(
    documents,
    chunk_size=500,
    chunk_overlap=50
)

# Use one consistent embedding model.
chunk_vectors = embedding_model.embed_documents(chunks)

vector_database.add(
    vectors=chunk_vectors,
    texts=chunks
)


# ---------------------------------
# PART B: ANSWER A USER'S QUESTION
# ---------------------------------

def answer_question(question):
    # 1. Convert the question into a vector.
    query_vector = embedding_model.embed_query(question)

    # 2. Retrieve relevant passages.
    results = vector_database.similarity_search(
        query_vector,
        top_k=3
    )

    # 3. Prepare the context from retrieved passages.
    context = "\n\n".join(
        result.text for result in results
    )

    # 4. Construct a grounded prompt.
    prompt = build_rag_prompt(
        context=context,
        question=question
    )

    # 5. Ask the LLM to generate an answer.
    answer = llm.generate(prompt)

    # 6. Return the answer and source information.
    return {
        "answer": answer,
        "sources": [result.metadata for result in results]
    }