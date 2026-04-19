import os
import json
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="smartsupport_ai/db/chroma_db")
        
        # Fallback to local embeddings for better stability during development
        self.emb_fn = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self.client.get_or_create_collection(
            name="company_knowledge",
            embedding_function=self.emb_fn
        )

    def search(self, query: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return "\n".join(results['documents'][0])

def ingest_to_chroma():
    store = VectorStore()
    
    documents = []
    metadatas = []
    ids = []

    # Load FAQs
    faq_path = 'smartsupport_ai/datasets/faqs.json'
    if os.path.exists(faq_path):
        with open(faq_path, 'r') as f:
            faqs = json.load(f)
            for i, faq in enumerate(faqs):
                text = f"Question: {faq['question']}\nAnswer: {faq['answer']}"
                documents.append(text)
                metadatas.append({"source": "faq", "type": "qa"})
                ids.append(f"faq_{i}")

    # Load Policies
    policy_path = 'smartsupport_ai/datasets/policies.json'
    if os.path.exists(policy_path):
        with open(policy_path, 'r') as f:
            policies = json.load(f)
            for key, value in policies.items():
                documents.append(f"Policy: {key.replace('_', ' ').capitalize()}\nContent: {value}")
                metadatas.append({"source": "policy", "type": "text"})
                ids.append(f"policy_{key}")

    if documents:
        store.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"ChromaDB ingestion complete with local embeddings. Added {len(documents)} documents.")
    else:
        print("No documents found.")

if __name__ == "__main__":
    ingest_to_chroma()
