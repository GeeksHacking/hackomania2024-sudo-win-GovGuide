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

GENERATE_DRAFT_SCRIPT = """You will be given two pieces of information: the business information and a list of explanations as detailing why the respective specific government scheme is relevant to the business.

This is the business information: \"\"\"{info}\"\"\"

Explaining some possible schemes for the business: \"\"\"{explanations}\"\"\"

Referring to the many schemes above, promote the scheme and convince the business to apply for it (30-45 talking seconds of content). Remember you are talking to them directly. Remember to consider all the above schemes mentioned. Generate enough content for 30 to 40 seconds of talking. Remember to include details and BE SPECIFIC. Make sure it is relevant to the business! Don't use placeholder numbers like X%. 
"""

ENHANCE_SCRIPT_CHECK = """Imagine you are a marketing professional. You will be given business information, a list of schemes and a draft script.

Your goal is to promote these schemes/grants to businesses.

This is the business information: \"\"\"{info}\"\"\"
This is a list of explanations as to why schemes are relevant: \"\"\"{explanations}\"\"\"
This is the draft script: \"\"\"{draft_script}\"\"\"

List out a list of considerations and changes you would make to further enhance the draft script.
"""

ENHANCE_SCRIPT_WRITE = """Imagine you are a marketing professional. You will be given a draft narrator's script and list of recommended potential improvements.

Your goal is to promote these schemes/grants to businesses.

This is the draft script: \"\"\"{draft_script}\"\"\"
This is the list of improvements: \"\"\"{improvements}\"\"\"

Modify the draft script into a final version that is better. Make sure the wording talks DIRECTLY to user.
"""

FORMAT_SCRIPT = """You will be given a script and need to parse into JSON format, and think of relevant scenes.

Follow this format specifically. Note that each scene is associated with several sentences:
```
{{"list_of_scenes":[{{"scene": "family trip skiing","subtitles": ["Are you ready for an unforgettable family ski trip to Japan? Ensure your adventure is worry-free with Singlife's travel insurance!"]}}]}}
```

This is the script: \"\"\"{script}\"\"\"

Parse the script to follow the JSON format above, as well as ensure visual generic image scenes such as "family trip skiing", NO ACRYONYMS KEEP IT SIMPLE. Remember to follow the script WORD FOR WORD. Scenes should be generic and only 3 words. Populate the list of scenes. Keep to ONE SENTENCE PER SCENE.
"""

GET_RESOURCES = """You will be given information about business, a list of explanations of why schemes are relevant to a business, a script that, and a list of URLs corresponding to the schemes in the list of explanations

Information about business: {info}
Explanations of scheme and business: {explanations}
Script: {script}
List of Title-URL pairs according to the schemes in explanations: {title_urls}

Your goal is to provide relevant citations/sources for the script.
Firstly, list any relevant Title-URL pairs. Then, summarize the script into bullet points and cite/associate each point with the sources using square bracket.
Here is the format you should follow:
```
### Sources
1. <relevant title> - <relevant url>
2. <relevant title 2> - <relevant url 2>
...

### Citation
- <summarized bullet point from script> [1][2]
- <summarized bullet point from script> [1]
```

Note how the citation refers to the number of the sources and cites it accurately. Only cite if it is relevant.

Output the formatted markdown directly:
"""