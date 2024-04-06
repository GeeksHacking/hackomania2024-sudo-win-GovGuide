from typing import List

class UserData:
	def __init__(self):
		pass

class ScriptGenerator:
	# user input -> extract docs -> repeat: [user input + doc[i] -> explain how the scheme applies to the problem] -> final script generate -> eval / enhance script pipeline -> ]
	def __init__(self):
		pass

	def get_relevant_docs(self, user_data: UserData):
		pass

	def generate_script(self, user_data: UserData):
		pass

	def __explain_scheme_to_user():
		pass

	def __call__(self, user_data):
		relevant_docs: List[str] = self.get_relevant_docs(user_data)
		script: str = self.generate_script(user_data, relevant_docs)
		script: str = self.enhance_script(user_data, script)

		return script