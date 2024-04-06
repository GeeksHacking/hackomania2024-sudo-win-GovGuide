from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
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
	company: str = "Singapore SME: GreenEats Food Service",
	work: str = "GreenEats operates large commercial kitchen, preparing large variety of dishes",
	industry: str = "Food Service",
	concerns: str = "Increasing cost of energy...",
	needs: str = "Need to upgrade kitchen",

class ScriptGenerator:
	def __init__(self, api_key):
		self.chat = ChatOpenAI(model = 'gpt-3.5-turbo', api_key = api_key)
		self.json_chat = ChatOpenAI(
			model = "gpt-3.5-turbo-0125",
			api_key = api_key,
			model_kwargs = {"response_format": {"type": "json_object"}},
		)

	def get_relevant_docs(self, user_data: UserData) -> str:
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

		return [doc]

	def format_script(self, script: str) -> str:
		json_content = self.json_chat.invoke([
			HumanMessage(
				content = FORMAT_SCRIPT.format(
					script = script
				)
			)
		]).content

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
		])

		return self.chat.invoke([
			HumanMessage(
				content = ENHANCE_SCRIPT_WRITE.format(
					draft_script = draft_script,
					improvements = improvements
				)
			)
		]).content

	def generate_script(self, user_data: UserData, relevant_docs: List[str]) -> str:
		explanations = []
		for doc in relevant_docs:
			explanations.append(self.__explain_scheme_to_user(user_data, doc))

		return self.__generate_draft_script(user_data, explanations), explanations

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

	def __explain_scheme_to_user(self, user_data: UserData, doc: str) -> str:
		"""
		Given a relevant document (scheme) and user data, return an explanation of why the scheme is relevant to the user.
		"""

		return self.chat.invoke([
			HumanMessage(
				content = EXPLAIN_SCHEME_TO_USER.format(
					info = user_data,
					scheme = doc
				)
			)
		]).content

	def __call__(self, user_data) -> str:
		relevant_docs: List[str] = self.get_relevant_docs(user_data)
		script, explanations = self.generate_script(user_data, relevant_docs)
		script: str = self.enhance_script(user_data, script, explanations)

		script: str = self.format_script(script)

		return script