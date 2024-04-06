from dotenv import load_dotenv, dotenv_values
load_dotenv()
env = dotenv_values()
from typing import List, Tuple, Dict

import weaviate
import weaviate.classes as wvc
from weaviate.collections.collections import Collection
from weaviate.client import WeaviateClient

from pydantic import BaseModel
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from .prompts import EXPLAIN_SCHEME_TO_USER, GENERATE_DRAFT_SCRIPT, ENHANCE_SCRIPT_CHECK, ENHANCE_SCRIPT_WRITE, FORMAT_SCRIPT

def split_text(text, max_ = 15, min_ = 5):
	new_content = []
	split_text = text.split(' ')
	for i in range(0, len(split_text), max_):
		upper_lim = min(len(split_text), i + max_)

		if len(split_text) - upper_lim < min_:
			new_content.append(
				" ".join(split_text[i:]) + " "
			)
			break
		else:
			new_content.append(
				" ".join(split_text[i:upper_lim]) + " "
			)

	return new_content

class UserData(BaseModel):
	# def __init__(self):
	# 	pass
	name: str
	industry: str
	concern: str
	need: str
	nature: str

class ScriptGenerator:
	def __init__(self):
		self.chat = ChatOpenAI(model = 'gpt-3.5-turbo-0125', api_key = env["OPENAI_API_KEY"])
		self.json_chat = ChatOpenAI(
			# model = "gpt-3.5-turbo-0125",
			model = "gpt-4-0125-preview",
			api_key = env["OPENAI_API_KEY"],
			model_kwargs = {"response_format": {"type": "json_object"}},
		)

		wv_headers: Dict[str, str] = {
			"X-OpenAI-Api-key": env["OPENAI_API_KEY"],
		}
		self.__wv_client: WeaviateClient = weaviate.connect_to_wcs(
			cluster_url=env["WEAVIATE_URL"],
			auth_credentials=weaviate.auth.AuthApiKey(env["WEAVIATE_API_KEY"]),
			headers=wv_headers,
		)
		self.__scheme_chunk_collection: Collection = self.__wv_client.collections.get("scheme_chunks")
		self.__scheme_whole_collection: Collection = self.__wv_client.collections.get("whole_scheme")

		self.__relevant_doc_limit: int = 2
		self.__relevant_doc_target_vec: str = "content_chunk"
		self.__relevant_doc_certainty_thres: float = 0.85
		self.__relevant_doc_distance_thres: float = 0.2


	def format_script(self, script: str) -> str:
		json_content = self.json_chat.invoke([
			HumanMessage(
				content = FORMAT_SCRIPT.format(
					script = script
				)
			)
		]).content

		print('formatted script:', json_content)

		json_content = json.loads(json_content)

		for i, scene in enumerate(json_content['list_of_scenes']):
			text = scene['subtitles'][0]
			json_content['list_of_scenes'][i]['subtitles'] = split_text(text)

		return json_content

	def enhance_script(self, user_data: UserData, explanations: List[str], draft_script: str) -> str:
		improvements = self.chat.invoke([
			HumanMessage(
				content = ENHANCE_SCRIPT_CHECK.format(
					info = user_data,
					explanations = explanations,
					draft_script = draft_script
				)
			)
		]).content
		print("improvements:", improvements)

		out = self.chat.invoke([
			HumanMessage(
				content = ENHANCE_SCRIPT_WRITE.format(
					draft_script = draft_script,
					improvements = improvements
				)
			)
		]).content

		out = out.replace('\n', ' ')
		print("enhanced:", out)
		return out

	def generate_script(self, user_data: UserData, relevant_docs: List[str]) -> str:
		explanations = []
		for doc in relevant_docs:
			explanations.append(self.__explain_scheme_to_user(user_data, doc))

		out = self.__generate_draft_script(user_data, explanations), explanations

		print("draft script:", out[0])
		return out

	def __generate_draft_script(self, user_data: UserData, explanations: List[str]) -> str:
		"""
		Takes in user data and a list of explanations of why the scheme is related, and forms a coherent script.
		"""

		return self.chat.invoke([
			HumanMessage(
				content = GENERATE_DRAFT_SCRIPT.format(
					info = user_data,
					explanations = explanations
				)
			)
		]).content

	def __document_chunk_query(self, text: str):
		return self.__scheme_chunk_collection.query.near_text(
			query=text,
			limit=self.__relevant_doc_limit,
			target_vector=self.__relevant_doc_target_vec,
			certainty=self.__relevant_doc_certainty_thres,
			# distance=self.__relevant_doc_distance_thres,
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
			if chunk.properties["title"] not in doc_names:
				doc_names.append(chunk.properties["title"])

		documents = self.__get_whole_document(doc_names)
		documents = [doc.properties["content"] for doc in documents]

		return documents

	def __explain_scheme_to_user(self, user_data: UserData, doc: str) -> str:
		"""
		Given a relevant document (scheme) and user data, return an explanation of why the scheme is relevant to the user.
		"""

		out = self.chat.invoke([
			HumanMessage(
				content = EXPLAIN_SCHEME_TO_USER.format(
					info = user_data,
					scheme = doc
				)
			)
		]).content
		print("explain:", out)
		return out

	def __call__(self, user_data) -> str:
		relevant_docs: List[str] = self.get_relevant_docs(user_data)
		script, explanations = self.generate_script(user_data, relevant_docs)
		script: str = self.enhance_script(user_data, script, explanations)

		script: str = self.format_script(script)

		return script