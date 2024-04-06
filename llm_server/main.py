from dotenv import load_dotenv, dotenv_values
load_dotenv()
env = dotenv_values()
from typing import List, Tuple, Dict

import weaviate
import weaviate.classes as wvc
from weaviate.collections.collections import Collection
from weaviate.client import WeaviateClient

class UserData:
	# def __init__(self):
	# 	pass
	name: str
	industry: str
	concern: str
	need: str
	nature: str

class ScriptGenerator:
	# user input -> extract docs -> repeat: [user input + doc[i] -> explain how the scheme applies to the problem] -> final script generate -> eval / enhance script pipeline -> ]
	def __init__(self):
		wv_headers: Dict[str, str] = {
			"X-OpenAI-Api-key": env["OPENAI_API_KEY"],
		}
		self.__wv_client: WeaviateClient = weaviate.connect_to_local(headers=wv_headers)
		self.__scheme_chunk_collection: Collection = self.__wv_client.collections.get("Scheme Chunk")
		self.__scheme_whole_collection: Collection = self.__wv_client.collections.get("Scheme Whole")

		self.__relevant_doc_limit: int = 2
		self.__relevant_doc_target_vec: str = "content_chunk"
		self.__relevant_doc_certainty_thres: float = 0.85
		self.__relevant_doc_distance_thres: float = 0.2

	def __document_chunk_query(self, text: str):
		return self.__scheme_chunk_collection.query.near_text(
			query=text,
			limit=self.__relevant_doc_limit,
			target_vector=self.__relevant_doc_target_vec,
			certainty=self.__relevant_doc_certainty_thres,
			distance=self.__relevant_doc_distance_thres,
			return_metadata=wvc.query.MetadataQuery(
				certainty=True,
				distance=True
			),
		).objects
	
	def __get_whole_document(self, names: List[str]):
		filter = wvc.query.Filter.by_property("title").contains_any(names)
		return self.__scheme_whole_collection.query.fetch_objects(
			filters=filter,
		).objects

	def get_relevant_docs(self, user_data: UserData):
		doc_names: List[str] = []
		concern_chunks = self.__document_chunk_query(user_data.concern)
		need_chunks = self.__document_chunk_query(user_data.need)
		nature_chunks = self.__document_chunk_query(user_data.nature)
		all_chunks = concern_chunks + need_chunks + nature_chunks
		all_chunks = sorted(all_chunks, key=lambda x: x.metadata.certainty, reverse=True)
		for chunk in all_chunks:
			if len(doc_names) == 2: break
			if chunk.properties["title"] in doc_names:
				doc_names.append(chunk.properties["title"])

		documents = self.__get_whole_document(doc_names)
		documents = [doc.propeties["content"] for doc in documents]
		return documents

	def generate_script(self, user_data: UserData):
		pass

	def __explain_scheme_to_user():
		pass

	def __call__(self, user_data):
		relevant_docs: List[str] = self.get_relevant_docs(user_data)
		script: str = self.generate_script(user_data, relevant_docs)
		script: str = self.enhance_script(user_data, script)

		return script