from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = QdrantClient(
    url=f"https://{os.getenv('QDRANT_HOST')}:{os.getenv('QDRANT_PORT')}",
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "employee_insights"

def upsert_documents(docs):
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(id=doc["id"], vector=doc["vector"], payload=doc["payload"])
            for doc in docs
        ]
    )

def search_qdrant(query: str):
    try:
        # Always vectorize the user query
        embedding = OpenAI(api_key=os.getenv("OPENAI_API_KEY")).embeddings.create(
            input=[query],
            model=os.getenv("EMBEDDING_MODEL")
        ).data[0].embedding

        # Perform semantic search in Qdrant
        hits = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=embedding
        )

        return [
            {
                "text": h.payload["text"],
                "metadata": h.payload.get("metadata")
            }
            for h in hits if h.payload.get("text")
        ]

    except Exception as e:
        print(f"Error searching in Qdrant: {e}")
        return []
