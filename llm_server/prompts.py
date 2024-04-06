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