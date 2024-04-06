from llm_server import UserData, ScriptGenerator

user_data = UserData(
	name = "Singapore SME: GreenEats Food Service",
	industry = "Food Service",
	concern = "Increasing cost of energy...",
	need = "Need to upgrade kitchen",
	nature = "GreenEats operates large commercial kitchen, preparing large variety of dishes",
)

script_gen = ScriptGenerator()
script_json = script_gen(user_data)

print(script_json)
```
{
  "list_of_scenes":[
    {
      "scene": "family trip skiing",
      "subtitles": [
        "Are you ready for an unforgettable family ski trip to Japan?",
        "Ensure your adventure is worry-free with Singlife's travel insurance!"
      ]
    },
    {
      "scene": "insurance policy document close up",
      "subtitles": [
        "Our comprehensive travel insurance plans cater to your needs.",
        "Peace of mind throughout your journey."
      ]
    },
    {
      "scene": "beach vacation",
      "subtitles": [
        "Escape to paradise with our beach vacation package.",
        "Experience the sun, sand, and surf like never before!"
      ]
    },
    {
      "scene": "exploring ancient ruins",
      "subtitles": [
        "Embark on a thrilling adventure to discover ancient ruins.",
        "Uncover the secrets of the past with Singlife as your travel companion."
      ]
    },
    {
      "scene": "city sightseeing",
      "subtitles": [
        "Immerse yourself in the vibrant energy of a bustling city.",
        "Explore iconic landmarks and create unforgettable memories."
      ]
    },
    {
      "scene": "wildlife safari",
      "subtitles": [
        "Embark on a wildlife safari and witness nature's wonders up close.",
        "Let Singlife protect you on your extraordinary journey."
      ]
    }
  ]
}
```