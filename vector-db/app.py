import os
import json
from typing import List, Dict
from dotenv import dotenv_values, load_dotenv
load_dotenv()
env = dotenv_values()

from fastapi import FastAPI
from langchain_text_splitters import MarkdownHeaderTextSplitter, MarkdownTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.vectorstores import VectorStore

import weaviate

app = FastAPI()
weaviate_client = weaviate.connect_to_local()

base_path = os.path.dirnamej(os.path.abspath(__file__))

# @app.route("/init_pinecone")
# def init_pinecone_vecdb():

def source_title_parser(source: str) -> str:
    return os.path.splitext(os.path.basename(source))[0]

def mdhsplitter_reformatter(doc: Document) -> str:
    headers = {
        "Header 3": "###",
        "Header 2": "##",
        "Header 1": "#",
    }
    text = doc.page_content
    for header, v in headers.items():
        if header not in doc.metadata.keys():
            continue
        text = f"{v} {doc.metadata[header]}\n" + text

    return text

@app.route("/init_weaviate")
def init_weaviate_vecdb():
    # initialise all the schemas in the weaviate vector database
    with open("schema.json", "r") as f:
        schemas: Dict = json.loads(f.read())
        
    weaviate_client.collections.delete_all()
    failed: List[str] = []
    for schema in schemas["classes"]: 
        try:
            weaviate_client.collections.create_from_dict(schema)
        except:
            print(f"Failed to create {schema['class']}")
            failed.append(schema["class"])
    weaviate_client.close()
    if not failed:
        return {"message": f"Successfully created {len(schemas["classes"])} schemas"}
    return {"message": f"Failed to create {len(failed)} schemas: {failed}"}

@app.route("/load_local_data")
def load_local_vecdb():
    dir_loader = DirectoryLoader(
        path=os.path.join(base_path, "data"),
        loader_cls=TextLoader,
    )
    mdhsplitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ],
        # strip_headers=False,
    )

    collection = weaviate_client.collections.get("Schemes")
    
    with collection.batch.dynamic() as batch:
        for doc in dir_loader.load():
            doc_chunks: List[Document] = mdhsplitter.split_text(doc.page_content)
            title = source_title_parser(doc.metadata["source"])
            for chunk in doc_chunks:
                text: str = mdhsplitter_reformatter(chunk)
                batch.add_object(
                    properties={
                        "content_chunks": text,
                        "title": title,
                        "source": doc.metadata["source"],
                    }
                )
