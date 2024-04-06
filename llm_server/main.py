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

		# wv_headers: Dict[str, str] = {
		# 	"X-OpenAI-Api-key": env["OPENAI_API_KEY"],
		# }
		# self.__wv_client: WeaviateClient = weaviate.connect_to_local(headers=wv_headers)
		# self.__scheme_chunk_collection: Collection = self.__wv_client.collections.get("Scheme Chunk")
		# self.__scheme_whole_collection: Collection = self.__wv_client.collections.get("Scheme Whole")

		# self.__relevant_doc_limit: int = 2
		# self.__relevant_doc_target_vec: str = "content_chunk"
		# self.__relevant_doc_certainty_thres: float = 0.85
		# self.__relevant_doc_distance_thres: float = 0.2


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
		# doc_names: List[str] = []
		# concern_chunks = self.__document_chunk_query(user_data.concern)
		# need_chunks = self.__document_chunk_query(user_data.need)
		# nature_chunks = self.__document_chunk_query(user_data.nature)
		# all_chunks = concern_chunks + need_chunks + nature_chunks
		# all_chunks = sorted(all_chunks, key=lambda x: x.metadata.certainty, reverse=True)
		# for chunk in all_chunks:
		# 	if len(doc_names) == 2: break
		# 	if chunk.properties["title"] in doc_names:
		# 		doc_names.append(chunk.properties["title"])

		# documents = self.__get_whole_document(doc_names)
		# documents = [doc.propeties["content"] for doc in documents]

		doc = """
		# The Energy Efficient Grant

		The Energy Efficient Grant (EEG) was launched in September 2022 and aims to help businesses within the Food and Service, Food Manufacturing or Retail sectors to cope with rising energy costs, through co-funding investments in more energy efficient equipment.

		It provides financial support for SMEs to adopt pre-approval energy efficient equipment in the following categories: LED lighting, air-conditioning, cooking hobs, refrigerators, water heaters and clothes dryers.

		## EEG Eligibility

		### Who can apply?
		A SME can apply for EEG if they meet all the following criteria:
		- Is a business entity registerd and operating in Singapore in the Food Service, Food Manufacturing or Retail sectors as defined below
			- Food Service companies must have valid Singapore Food Agency (SFA) licences and be classified under SSICs 56 or 68104.
			- Food Manufacturing companies must have valid SFA licences and be classified under SSIC 10 or 11
			- Retail companies that are classified under SSIC 47
		- Has a minimum of 30% local shareholding
		- Company's Group annual sales turnover should be not more than S$100 million, OR Company's Group employment size should be no more than 200 employees

		Equipment purchased must be used in Singapore

		### How to apply and submit EEG claims?
		4 steps:
		1. Access the list of pre-approved energy efficient equipment (brands & models) and identify relevant eqiupment that best suits your business needs.
		2. Source for the energy efficient equipment and get a quotation from the vendor.
		3. Submit an application on the Business Grants Portal (BGP). You will need to register for a Corppass account to transact on the portal
		4. After your application has been approved, submit your grant claim on the BGP before your claim due date.

		Note:
		- From 1 Sep 2022 to 31 Mar 2024, companies will be able to submit applications for the purchase of energy efficient equipment through the Business Grants Portal (BGP).
		- Companies will have up to 1 year from the time an application is approved to purchase and install the equipment and submit claims for reimbursement. Once an application has been submitted, companies may choose to proceed to purchase the equipment before the application outcome. However, companies will not be able to claim subsequently if the application is unsuccessful.
		- This pre-approved energy efficient equipment listing is not to be taken as a form of endorsement or recommendation by the participating government agencies. Companies are reminded to carry out due diligence when engaging vendors, and not to share their Corppass with the vendors to carry out submission of any grant applications or claims.

		## Types of EEG Equipment
		The following equipment categories are supported under the EEG:
		- Air-conditioner
		- Clothes Dryer
		- Cooking Hob
		- LED Lighting
		- Refrigerator
		- Water Heater
		"""

		doc2 = """
		# Enterprise Development Grant
		- For Singapore companies starting new projects to upgrade their business, explore new growth, or expand overseas
		- Funds individual projects tailored to your business

		## About this programme
		The Enterprise Development Grant (EDG) supports projects that help you upgrade, innovate, grow and transform your business. Submit your individual project proposals with details on your business plans and project outcomes to take your business further.

		EDG funds qualifying project costs namely third-party consultancy fees, software and equipment, and internal manpower cost.

		- Up to 50% of eligible costs for local SMEs
			- From 1 April 2023, SMEs can receive up to 50% support for EDG (sustainability-related projects may be supported at up to 70% from 1 April 2023 to 31 March 2026). Please refer to the Enterprise Sustainability Programme page for more details.

		## Eligibility
		- Business entity registered and operating in Singapore
		- Company has at least 30% local equity held directly or indirectly by Singaporean(s) and/or Singapore PR(s), determined by the ultimate individual ownership
		- Company is financially ready to start and complete the project. Commonly used financial indicators, such as the current ratio, will be used for assessment.

		## Project Categories
		Today and into the future, companies that thrive are the ones that have strong business foundations and strategies, adopt technology and innovative processes, and grow their overseas presence.  
		EDG helps Singapore companies grow and transform. This grant supports projects that help you upgrade your business, innovate or venture overseas, under three categories: Core Capabilities, Innovation & Productivity, and Market Access

		### Core Capabilities
		Projects under Core Capabilities help you prepare for growth and transformation by strengthening your business foundations. These include business strategy, financial management, human capital development, service excellence, strategic brand and marketing development.

		#### Business Strategy Development
		Formulate growth strategies and processes to improve your business development, better manage your intellectual property assets, optimise R&D operations, and implement sustainable practices.

		Projects Accepted
		- Diagnosis and gap analysis in your company
		- Assessment of internal and external factors, such as strengths and weaknesses, and competition
		- Development of a strategic roadmap, business frameworks, policies or processes
		- Recommendations and plans for implementation
		- Sustainability strategy projects that include one or more of the following components:
			- Assessment of sustainability risks and opportunities
			- Strategy development
			- Governance framework
			- Setting metrics and targets   
		What's not covered:
		- Stand-alone IP registration costs
		- Stand-alone reports/assurance
		- Stand-alone set-up of sustainability unit and/or hiring of Chief Sustainability Officer/Sustainability Lead

		#### Financial Management
		Optimise your company’s financial performance and equip your management team with better skills to steward your company’s assets and resources more effectively.

		Projects accepted:
		- Diagnosis and gap analysis in your company
		- Development of a strategic roadmap, business frameworks, policies or processes
		- Recommendations and plans for implementation
		- Development of plans to optimise financing, investment, and risk management
		- Identification of business risk exposure, and development of proper risk management processes and controls
		- Formation of international corporate structures to minimise tax liabilities

		What is not covered:
		- Regulatory compliance costs, such as preparation of consolidated financial statements, accounting/ tax filing services
		- Drafting of legal documents
		- Procurement of ICT solutions

		#### Human Capital Development
		Strengthen your teams with the right skills as you scale and support business growth.

		Projects accepted:
		- Diagnosis and gap analysis in your company
		- Development of a strategic roadmap, business frameworks, policies or processes
		- Recommendations and plans for implementation

		Areas covered:
		- Compensation & Benefits
		- Employee Engagement & Communication
		- Employee Value Proposition
		- HR Management
		- International Mobility
		- Job Redesign
		- Learning & Development
		- Manpower Planning
		- Organisation Culture
		- Performance Management
		- Recruitment & Selection
		- Talent Management & Succession Planning

		What is not covered:
		- Standalone training courses
		- Incentives, benefits and welfare subsidies for employees

		#### Service Excellence
		Improve the quality of your service and products by gaining a deeper understanding of your customers’ needs and understanding their decision-making processes.

		Projects accepted:
		- Diagnosis and gap analysis in your company
		- Assessment of internal and external factors, such as strengths and weaknesses, and competitors
		- Development of a strategic roadmap, business frameworks, policies or processes
		- Recommendations and plans for implementation
		- Customer Diagnostics: Diagnosis and gap analysis of customer needs to improve service levels and drive customer-centric behaviour
		- Service Innovation: Adoption of advanced customer research, analytics and service process redesign to enhance customer experience

		What is not covered:
		- Incentives for mystery shoppers and customer survey respondents

		#### Strategic Brand and Marketing Development
		Differentiate your brand and marketing offerings through strategies that better capture your target audience and extend your reach.

		Projects accepted:
		- Diagnosis and gap analysis in your company
		- Assessment of internal and external factors, such as strengths and weaknesses, and competitors
		- Primary or secondary research
		- Recommendations and plans for implementation
		- Development of effective brand strategy that appeals to targeted consumers and offers differentiated proposition from the competition
		- Assessment of a brand’s financial value and identification of brand levers
		- Development of a strategic plan to optimise marketing resources and improve customer communications

		What is not covered:
		- Production of corporate and/ or marketing collaterals, such as brochures, videos, websites, photography, stock pictures, and copywriting
		- Implementation of marketing or PR campaigns, including retainer fees of consultants, advertising and media buys, engagement of social media influencers, management of websites/ social media platforms, Search Engine Optimisation (SEO), and Search Engine Marketing (SEM)

		## How to apply
		1. Identify the project category you wish to apply for.
		2. There are no pre-approved vendors for the EDG
		"""
		return [doc, doc2]

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