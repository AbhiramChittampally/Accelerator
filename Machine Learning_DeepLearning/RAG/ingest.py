from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# -------------------------------
# CONFIGURATION
# -------------------------------

DOCUMENTS_DIR = Path("documents")
DB_DIR = Path("chroma_db")

COLLECTION_NAME = "document_knowledge"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 120
CHUNK_OVERLAP = 30


# -------------------------------
# 1. LOAD DOCUMENTS
# -------------------------------

def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        if text.strip():
            documents.append({
                "text": text,
                "source": str(file_path)
            })

    if not documents:
        raise ValueError(
            "No non-empty .txt files found in the documents folder."
        )

    return documents


# -------------------------------
# 2. SPLIT TEXT INTO CHUNKS
# -------------------------------

def chunk_text(text, chunk_size=CHUNK_SIZE,
               overlap=CHUNK_OVERLAP):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and smaller than chunk_size."
        )

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end == len(words):
            break

        start = end - overlap

    return chunks


# -------------------------------
# 3. LOAD THE EMBEDDING MODEL
# -------------------------------

def load_embedding_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


# -------------------------------
# 4. BUILD THE VECTOR DATABASE
# -------------------------------

def main():
    documents = load_documents()
    embedding_model = load_embedding_model()

    client = chromadb.PersistentClient(path=str(DB_DIR))

    # Rebuild this collection from the current source files.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    all_chunks = []
    all_ids = []
    all_metadata = []

    for document_index, document in enumerate(documents):
        chunks = chunk_text(document["text"])

        for chunk_index, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(
                f"doc{document_index}_chunk{chunk_index}"
            )
            all_metadata.append({
                "source": document["source"],
                "chunk_index": chunk_index
            })

    if not all_chunks:
        raise ValueError("No text chunks were generated.")

    # Convert every chunk into a real embedding vector.
    embeddings = embedding_model.encode(
        all_chunks,
        normalize_embeddings=True
    ).tolist()

    # Store IDs, original text, metadata and vectors together.
    collection.add(
        ids=all_ids,
        documents=all_chunks,
        metadatas=all_metadata,
        embeddings=embeddings
    )

    print(f"Loaded {len(documents)} document(s).")
    print(f"Created {len(all_chunks)} chunks.")
    print(f"Stored vectors in: {DB_DIR.resolve()}")


if __name__ == "__main__":
    main()