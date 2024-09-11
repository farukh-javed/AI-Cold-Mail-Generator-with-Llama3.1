import uuid
import chromadb
import pandas as pd

df = pd.read_csv("my_portfolio.csv")
client = chromadb.PersistentClient("vectorstore")

try:
    collection = client.get_or_create_collection("portfolio")
except AttributeError as e:
    print(f"Error occurred: {e}")

if not collection.count():
    for _, row in df.iterrows():
        collection.add(
            documents=[row["Techstack"]],
            metadatas={"links": row["Links"]},
            ids=[str(uuid.uuid4())]
        )
    print(collection.count())
else:
    print("Failed to create or retrieve the collection.")

# clickup metermost resource in