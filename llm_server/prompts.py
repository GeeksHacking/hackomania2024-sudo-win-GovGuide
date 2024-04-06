from langchain.prompts import PromptTemplate

gen_vid_script_template = """Goal:Generate a detailed 30-45sec video script to generate a video to engage with a customer needs.\n\n
RULES:
1. Video script must be based on the "Custom knowledge base:" and "User query"
2. Video Script must comprise of a) Video Script voice over text, b) Visual background video descriptions
3. Length of video script must be 30-45sec, 6 scenes or more, cannot be too short
4. Format the video script to JSON object with list_of_scenes, scenes and subtitles
5. Curate the POV to be watched from the perspective of the customer (1st person)
6. Style of video script should be funny and sarcastic but informative
7. Video Script must have a flow and make sense
8. The Video Script does not need to introduce the customer details at the start, just say "Hi <customer name>" and start the video script
9. "Scene" must be max 5words, cannot have specific names, must be generic. Example:family trip skiing | accident bike crash

Custom knowledge base:\n-------------------------{relevant_documents}\n---------------------------------\n\n

Strictly following the RULES: generate a video script to answer the User Query:"{query}".
"""
GEN_VID_SCRIPT_PROMPT = PromptTemplate(
    template=gen_vid_script_template,
    input_variables=[
        "relevant_documents",
        "query",
    ],
)

EXPLAIN_SCHEME_TO_USER = """You will be given two pieces of information, the business information and the government scheme/grant.
help me explain in detail, and convincingly break down how the government scheme/grant is relevant to the business. Make sure to refer to the business information, and also include the name of the scheme at the start.

This is the business information: \"\"\"{info}\"\"\"

This is the government scheme/grant: \"\"\"{scheme}\"\"\"
"""

GENERATE_DRAFT_SCRIPT = """Imagine you are a marketing professional that writes video scripts. You help promote schemes/grants to businesses in a convincing fashion.

You will be given two pieces of information: the business information and a list of explanations as detailing why the respective specific government scheme is relevant to the business.

This is the business information: \"\"\"{info}\"\"\"

Here is a list of explanations on why the scheme is relevant: \"\"\"{explanations}\"\"\"

Referring to the above, write the content of a script to share on the scheme and convince the business to apply for it (30-45 seconds of content). Remember you are talking to them directly. Remember to consider all the above schemes mentioned.
"""

ENHANCE_SCRIPT_CHECK = """Imagine you are a marketing professional. You will be given business information, a list of schemes and a draft script.

Your goal is to promote these schemes/grants to businesses.

This is the business information: \"\"\"{info}\"\"\"
This is a list of explanations as to why schemes are relevant: \"\"\"{explanations}\"\"\"
This is the draft script: \"\"\"{draft_script}\"\"\"

List out a list of considerations and changes you would make to further enhance the draft script.
"""

ENHANCE_SCRIPT_WRITE = """Imagine you are a marketing professional. You will be given a draft script and list of recommended potential improvements.

Your goal is to promote these schemes/grants to businesses.

This is the draft script: \"\"\"{draft_script}\"\"\"
This is the list of improvements: \"\"\"{improvements}\"\"\"

Modify the draft script into a final version that is better. Make sure the wording talks DIRECTLY to user.
"""

FORMAT_SCRIPT = """Imagine you are a marketing professional. You will be given a script and need to cut it into JSON format, and think of relevant scenes.

For instance, here is an example:
```
{{"list_of_scenes":[{{"scene": "family trip skiing","subtitles": ["Are you ready for an unforgettable family ski trip","to Japan? Ensure your adventure is worry-free with Singlife's travel insurance!"]}},{{"scene": "insurance policy document close up","subtitles": ["Our comprehensive travel insurance plans cater to your","needs. Peace of mind throughout your journey."]}},...}}
```

This is the script: \"\"\"{script}\"\"\"

Parse the script to follow the JSON format above, as well as ensure visual generic image scenes such as "family trip skiing". Remember to follow the script wording WORD FOR WORD. Don't miss out on any content. Scenes should be generic and only 3 words.
"""